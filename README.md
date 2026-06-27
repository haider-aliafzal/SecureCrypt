# SecureCrypt

A web-based application for secure encryption and decryption of text and images. SecureCrypt uses the RC4 stream cipher for text and image steganography for hiding secret messages inside image files, all wrapped in a responsive, dark-themed interface.

## Features

- **Text Encryption & Decryption** — Encrypts text using the RC4 algorithm and encodes the result in Base64 for easy copying and sharing.
- **Image Steganography** — Hides text messages inside PNG or BMP images, with the ability to decode and extract them later.
- **Dark Mode UI** — Clean, modern interface built with HTML, CSS, and JavaScript.
- **Downloadable Output** — Download the encoded image directly from the browser once a message is embedded.

## Tech Stack

| Category           | Technologies              |
|---------------------|----------------------------|
| Frontend            | HTML, CSS, JavaScript     |
| Backend             | Flask (Python)            |
| Image Processing    | Pillow, NumPy             |
| Encryption          | RC4 (Stream Cipher)       |

## Project Structure

```
SecureCrypt/
│
├── main.py              # Flask backend logic
├── requirements.txt     # Python dependencies
├── static/
│   ├── style.css         # Dark theme stylesheet
│   └── script.js         # Frontend interactivity
└── templates/
    └── index.html        # Main webpage template
```

## Installation & Usage

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. Open your browser and navigate to the local address shown in the terminal.

## Author

**Haider Ali**
