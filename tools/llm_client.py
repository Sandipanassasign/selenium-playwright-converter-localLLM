
import urllib.request
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(prompt, model="codellama", stream=False):
    """
    Sends a prompt to Ollama and returns the generated text.
    Assumes standard Ollama API structure.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "options": {
            "temperature": 0.2,  # Low temperature for deterministic code
            "num_predict": 4096  # Limit output to prevent infinite loops on long files
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})

    try:
        if stream:
            # Simple streaming support (logs to stdout as it comes)
            # Not fully implemented for return value yet in this snippet
            full_response = ""
            with urllib.request.urlopen(req, timeout=120) as response:
                for line in response: 
                    try:
                        chunk = json.loads(line)
                        text = chunk.get("response", "")
                        print(text, end="", flush=True)
                        full_response += text
                        if chunk.get("done"):
                            break
                    except:
                        pass
            return full_response
        else:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "")
                
    except urllib.error.URLError as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def extract_code_block(text):
    """
    Extracts code from markdown code blocks if present.
    e.g. ```typescript ... ``` -> ...
    If no blocks, returns original text (assuming raw code output).
    """
    pattern = r"```(?:typescript|javascript|ts|js)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()
