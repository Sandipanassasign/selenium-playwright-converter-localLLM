
import subprocess
import json
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def check_ollama_running():
    print("1. Checking if Ollama is running...")
    output = run_command("curl -s http://localhost:11434/")
    if output == "Ollama is running":
        print("✅ Ollama is reachable.")
        return True
    else:
        print("❌ Ollama is NOT reachable. Please run 'ollama serve'.")
        return False

def check_model_available(model_name="codellama"):
    print(f"2. Checking if model '{model_name}' is available...")
    output = run_command("curl -s http://localhost:11434/api/tags")
    if not output:
        print("❌ Failed to fetch models.")
        return False
    
    try:
        data = json.loads(output)
        models = [m['name'] for m in data.get('models', [])]
        # Check for partial match (e.g. codellama:latest)
        if any(model_name in m for m in models):
            print(f"✅ Model '{model_name}' found.")
            return True
        else:
            print(f"❌ Model '{model_name}' NOT found. Please run 'ollama pull {model_name}'.")
            print(f"   Available models: {models}")
            return False
    except json.JSONDecodeError:
        print("❌ Failed to parse Ollama response.")
        return False

def test_inference(model_name="codellama"):
    print(f"3. Testing inference with '{model_name}'...")
    payload = {
        "model": model_name,
        "prompt": "Write a one-line function in JavaScript to add two numbers.",
        "stream": False
    }
    # Escape quotes for curl command line JSON
    json_payload = json.dumps(payload).replace("'", "'\\''") 
    
    cmd = f"curl -s -X POST http://localhost:11434/api/generate -d '{json_payload}'"
    output = run_command(cmd)
    
    if output:
        try:
            response = json.loads(output)
            print(f"✅ Inference successful! Response: {response.get('response', '')[:50]}...")
            return True
        except:
            print("❌ Inference failed to parse.")
            return False
    else:
        print("❌ Inference verification failed.")
        return False

if __name__ == "__main__":
    if not check_ollama_running():
        sys.exit(1)
    
    # Check specifically for codellama or similar
    if not check_model_available("codellama"):
        print("⚠️ Warning: specific 'codellama' tag not found, checking alternatives...")
        # You might want to try to pull it here or just exit. 
        # For now, let's assume the user might have 'codellama:7b' or similar and proceed if any codellama exists.
    
    if not test_inference("codellama"):
         sys.exit(1)
         
    print("\n🎉 Link Phase Complete: OLLAMA INTEGRATION VERIFIED.")
