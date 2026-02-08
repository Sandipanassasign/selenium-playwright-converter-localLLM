
import argparse
import sys
import os
import json

# Add parent directory to path to allow importing adjacent modules if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_client import call_ollama, extract_code_block
from file_ops import read_file, write_file

def main():
    parser = argparse.ArgumentParser(description="Convert Selenium Java to Playwright using local LLM.")
    parser.add_argument("--input", required=True, help="Path to input Selenium Java file")
    parser.add_argument("--output", required=True, help="Path to output Playwright TS file")
    parser.add_argument("--lang", default="typescript", choices=["typescript", "javascript"], help="Target language")
    parser.add_argument("--model", default="codellama", help="Ollama model name (default: codellama)")
    
    args = parser.parse_args()
    
    print(f"Reading input from: {args.input}")
    selenium_code = read_file(args.input)
    if not selenium_code:
        sys.exit(1)

    # 1. Construct Prompt
    # We follow the SOP structure here, baking it into the prompt.
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
        selenium_code,
        "```",
        "",
        "### Output Code (Playwright Typescript)",
        "```typescript" 
    ]
    
    full_prompt = "\n".join(prompt_sections)
    
    print(f"Generating conversion using {args.model}...")
    
    # Send request
    # Note: We stream=False for now to get full result at once, 
    # but for larger files streaming might be better in a real app.
    response_text = call_ollama(full_prompt, model=args.model, stream=False)
    
    if not response_text:
        print("Error: No response from LLM.")
        sys.exit(1)
        
    # 2. Extract Code
    final_code = extract_code_block(response_text)
    
    if not final_code:
        print("Error: Could not extract code block from response.")
        # Fallback dump
        print("Raw response saved to .tmp/debug_response.txt")
        write_file(".tmp/debug_response.txt", response_text)
        sys.exit(1)

    # 3. Save Output
    print(f"Saving to {args.output}...")
    success = write_file(args.output, final_code)
    
    if success:
        print("✅ Conversion successful!")
    else:
        print("❌ Failed to save file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
