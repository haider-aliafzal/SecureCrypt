from flask import Flask, render_template, request, jsonify, send_file
import os
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import struct

app = Flask(__name__)
app.secret_key = os.urandom(24)


class RC4:

    def __init__(self, key):
        self.key = key
        self.S = list(range(256))
        self.initialize()

    def initialize(self):
        j = 0
        for i in range(256):
            j = (j + self.S[i] + ord(self.key[i % len(self.key)])) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def keystream(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            yield K

    def encrypt_text(self, text):
        keystream = self.keystream()
        return bytes([ord(c) ^ next(keystream) for c in text])

    def decrypt_bytes(self, data):
        keystream = self.keystream()
        return bytes([b ^ next(keystream) for b in data])


def encode_image(image, message, key):
    try:
        # Encrypt message
        rc4 = RC4(key)
        encrypted = rc4.encrypt_text(message)

        # Convert to binary
        data = struct.pack('>I', len(encrypted)) + encrypted
        binary = ''.join([format(byte, '08b') for byte in data])

        # Embed in image
        if image.mode not in ['RGB', 'RGBA']:
            image = image.convert('RGB')

        pixels = image.load()
        max_bits = image.width * image.height * 3
        required_bits = len(binary) + 32  # 32 bits for length header

        if required_bits > max_bits:
            raise ValueError("Image too small for message")

        idx = 0
        for row in range(image.height):
            for col in range(image.width):
                pixel = list(pixels[col, row])
                for i in range(3):
                    if idx < len(binary):
                        pixel[i] = pixel[i] & ~1 | int(binary[idx])
                        idx += 1
                pixels[col, row] = tuple(pixel)
                if idx >= len(binary):
                    break
            if idx >= len(binary):
                break

        return image
    except Exception as e:
        raise Exception(f"Encoding error: {str(e)}")


def decode_image(image, key):
    try:
        pixels = image.load()
        binary = []
        idx = 0

        # Read 32-bit length header
        for row in range(image.height):
            for col in range(image.width):
                for channel in pixels[col, row][:3]:
                    binary.append(str(channel & 1))
                    idx += 1
                    if idx == 32:
                        break
                if idx == 32:
                    break
            if idx == 32:
                break

        # Get message length
        length_bits = ''.join(binary[:32])
        length = struct.unpack(
            '>I',
            bytes(int(length_bits[i:i + 8], 2) for i in range(0, 32, 8)))[0]

        # Read encrypted data
        binary = []
        idx = 0
        total_bits = length * 8

        for row in range(image.height):
            for col in range(image.width):
                for channel in pixels[col, row][:3]:
                    if idx >= 32 and idx - 32 < total_bits:
                        binary.append(str(channel & 1))
                    idx += 1

        encrypted = bytes(
            int(''.join(binary[i:i + 8]), 2) for i in range(0, len(binary), 8))
        rc4 = RC4(key)
        return rc4.decrypt_bytes(encrypted).decode('utf-8')
    except Exception as e:
        raise Exception(f"Decoding error: {str(e)}")


# Text encryption/decryption routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form['text']
    key = request.form['key']
    try:
        rc4 = RC4(key)
        encrypted = base64.b64encode(rc4.encrypt_text(text)).decode()
        return jsonify({'result': encrypted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        encoded_text = request.form['text']
        key = request.form['key']
        rc4 = RC4(key)
        decoded = base64.b64decode(encoded_text)
        result = rc4.decrypt_bytes(decoded).decode()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/encode', methods=['POST'])
def encode():
    try:
        image = Image.open(request.files['image'])
        message = request.form['message']
        key = request.form['key']

        encoded = encode_image(image, message, key)

        img_io = BytesIO()
        encoded.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io,
                         mimetype='image/png',
                         download_name="encoded.png")
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/decode', methods=['POST'])
def decode():
    try:
        image = Image.open(request.files['image'])
        key = request.form['key']
        message = decode_image(image, key)
        return jsonify({'result': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
