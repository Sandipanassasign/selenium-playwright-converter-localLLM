
import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add current directory to path to import tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# We import tools like this to avoid import errors if run from root
try:
    from tools.llm_client import call_ollama, extract_code_block
except ImportError:
    # If run directly inside tools for some reason, handle gracefully
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
    from llm_client import call_ollama, extract_code_block

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConversionRequest(BaseModel):
    sourceCode: str
    model: str = "codellama"

@app.post("/api/convert")
def convert_code(request: ConversionRequest):
    # Validation: Removed strict TestNG check to allow generic Selenium code
    print(f"Received conversion request for model: {request.model}")
    
    # Construct Prompt (Sharing logic with converter.py, but optimized for API)
    prompt_sections = [
        "### System Context",
        "You are an expert Automation Engineer specializing in migrating legacy Selenium/Java tests to modern Playwright/Typescript.",
        "Your task: Convert the provided Selenium Java code to Playwright Typescript directly.",
        "",
        "### Rules",
        "1. STRICTLY OUTPUT CODE ONLY. Do not explain your reasoning. Do not add comments like 'Here is the code'.",
        "2. Use `async/await` pattern throughout.",
        "3. Use `@playwright/test` structure (`test`, `expect`).",
        "4. Replace `By.id` with `page.locator('#id')` or `page.getByLabel(...)` if context is clear.",
        "5. Remove explicit waits (`Thread.sleep`, `WebDriverWait`) unless critical logic requires them.",
        "",
        "### Input Code (Selenium Java)",
        "```java",
        request.sourceCode,
        "```",
        "",
        "### Output Code (Playwright Typescript)",
        "```typescript" 
    ]
    
    full_prompt = "\n".join(prompt_sections)
    
    # Call Ollama
    response_text = call_ollama(full_prompt, model=request.model, stream=False)
    
    if not response_text:
        raise HTTPException(status_code=500, detail="Failed to get response from LLM")
    
    final_code = extract_code_block(response_text)
    
    return {"convertedCode": final_code}

@app.get("/api/status")
def check_ollama_status():
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:11434/", timeout=2) as response:
            if response.status == 200:
                return {"status": "online", "message": "Ollama is running"}
    except Exception as e:
        print(f"Ollama check failed: {e}")
    
    return {"status": "offline", "message": "Ollama is not reachable"}

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
