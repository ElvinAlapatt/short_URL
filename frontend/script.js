const urlInput = document.getElementById('url-input');
const shortenBtn = document.getElementById('shorten-btn');
const resultBox = document.getElementById('result-box');

const shortenUrl = async () => {
    const longUrl = urlInput.value;

    if (!longUrl) {
        resultBox.innerText = 'Please enter a URL first!';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },

            body: JSON.stringify({ long_url: urlInput.value }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to shorten URL.');
        }

        const data = await response.json();
        const shortUrl = data.short_url;

        resultBox.innerHTML = `<a href="${shortUrl}" target="_blank">${shortUrl}</a>`;

    } catch (error) {
        resultBox.innerText = `Error: ${error.message}`;
        console.error('Error:', error);
    }
};

shortenBtn.addEventListener('click', shortenUrl);