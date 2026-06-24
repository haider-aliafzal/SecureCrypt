
async function processText() {
    const text = document.getElementById('text').value;
    const key = document.getElementById('key').value;
    const mode = document.querySelector('input[name="mode"]:checked').value;
    
    const formData = new FormData();
    formData.append('text', text);
    formData.append('key', key);
    
    try {
        const response = await fetch(`/${mode}`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.error) {
            document.getElementById('result').textContent = `Error: ${data.error}`;
        } else {
            document.getElementById('result').textContent = data.result;
            document.getElementById('copyBtn').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('result').textContent = `Error: ${error}`;
    }
}

async function processImage() {
    const image = document.getElementById('image').files[0];
    const secret = document.getElementById('secret').value;
    const key = document.getElementById('imgKey').value;
    const mode = document.querySelector('input[name="imgMode"]:checked').value;
    
    const formData = new FormData();
    formData.append('image', image);
    formData.append('message', secret);
    formData.append('key', key);
    
    try {
        const response = await fetch(`/${mode}`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            if (mode === 'encode') {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                document.getElementById('imgResult').innerHTML = 
                    `<a href="${url}" download="encoded.png">Download Encoded Image</a>`;
            } else {
                const data = await response.json();
                document.getElementById('imgResult').textContent = data.result;
            }
        } else {
            const data = await response.json();
            document.getElementById('imgResult').textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        document.getElementById('imgResult').textContent = `Error: ${error}`;
    }
}

function copyResult() {
    const result = document.getElementById('result').textContent;
    navigator.clipboard.writeText(result);
    alert('Copied to clipboard!');
}
