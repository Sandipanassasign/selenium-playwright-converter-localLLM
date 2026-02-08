
document.addEventListener('DOMContentLoaded', () => {
    const sourceCode = document.getElementById('source-code');
    const outputCode = document.getElementById('output-code');
    const convertBtn = document.getElementById('convert-btn');
    const loader = document.getElementById('loader');
    const pasteBtn = document.getElementById('paste-btn');
    const copyBtn = document.getElementById('copy-btn');

    // Paste handling
    pasteBtn.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            sourceCode.value = text;
        } catch (err) {
            console.error('Failed to read clipboard', err);
        }
    });

    // Copy handling
    copyBtn.addEventListener('click', () => {
        if (!outputCode.value) return;
        navigator.clipboard.writeText(outputCode.value);
        const originalText = copyBtn.innerText;
        copyBtn.innerText = '✅ Copied!';
        setTimeout(() => copyBtn.innerText = originalText, 2000);
    });

    // Conversion Logic
    convertBtn.addEventListener('click', async () => {
        const code = sourceCode.value.trim();
        if (!code) {
            alert('Please paste some Java code first!');
            return;
        }

        // GUI State: Loading
        convertBtn.classList.add('hidden');
        loader.classList.remove('hidden');
        outputCode.value = ''; // clear previous

        const selectedModel = document.getElementById('model-select').value;

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sourceCode: code,
                    model: selectedModel
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Server Error: ${response.status}`);
            }

            const data = await response.json();

            if (data.convertedCode) {
                outputCode.value = data.convertedCode;
            } else {
                outputCode.value = "// Error: No code returned from model.";
            }

        } catch (error) {
            console.error(error);
            outputCode.value = `// Error during conversion:\n// ${error.message}\n// Check if Ollama is running!`;
        } finally {
            // GUI State: Ready
            loader.classList.add('hidden');
            convertBtn.classList.remove('hidden');
        }
    });

    // Ollama Status Check
    const statusIndicator = document.getElementById('ollama-status');
    const statusText = statusIndicator.querySelector('.status-text');

    async function checkStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();

            if (data.status === 'online') {
                statusIndicator.classList.add('online');
                statusIndicator.classList.remove('offline');
                statusText.innerText = 'Ollama Online';
            } else {
                statusIndicator.classList.add('offline');
                statusIndicator.classList.remove('online');
                statusText.innerText = 'Ollama Offline';
            }
        } catch (e) {
            statusIndicator.classList.add('offline');
            statusIndicator.classList.remove('online');
            statusText.innerText = 'Server Offline';
        }
    }

    // Check immediately and then every 10 seconds
    checkStatus();
    setInterval(checkStatus, 10000);
});
