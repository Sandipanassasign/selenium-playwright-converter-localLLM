# Project Constitution (gemini.md)

## 📌 North Star
Develop a **Selenium Java to Playwright JS/TS Converter**. 
- **Input**: Selenium Java code snippets (TestNG) via a UI.
- **Output**: Playwright (JS/TS) code displayed in UI and saved to a new directory.
- **Core Value**: Prioritize readability and "modern" Playwright practices over strict 1:1 line mapping.

## 🧱 Data Schemas

### 1. ConversionRequest
The primary payload entering the system.
```json
{
  "sourceCode": "string (The raw Selenium Java code)",
  "languagePreference": "typescript | javascript",
  "outputDirectory": "string (Path to save the file, optional)"
}
```

### 2. ConversionResponse
The output payload returned to the UI.
```json
{
  "success": "boolean",
  "convertedCode": "string (The Playwright code)",
  "filesCreated": [
    "string (Absolute path to the saved file)"
  ],
  "logs": [
    "string (Any warnings or notes about the conversion)"
  ]
}
```

## ⚖️ Behavioral Rules
1.  **Readability First**: Do not just transliterate commands. Use Playwright's auto-waiting and locators effectively (e.g., prefer `getByRole` over `xpath` where possible/inferred).
2.  **Modern Syntax**: Use `async/await` patterns.
3.  **TestNG to Playwright**: Map TestNG annotations (`@Test`, `@BeforeMethod`) to Playwright test hooks (`test`, `test.beforeEach`).
4.  **Complete Conversion**: Attempt to convert the entire snippet, not just individual lines.

## 🏛️ Architectural Invariants
1.  **Data-First**: Define schema before coding tools.
2.  **3-Layer Architecture**: Separate SOPs (Architecture), Navigation (Reasoning), and Tools (Execution).
3.  **Self-Annealing**: Analyze, Patch, Test, Update Architecture on errors.
4.  **Local-First / Threaded**: All LLM operations must run in background threads (unblocked) to keep UI responsive.

## 🚀 Deployment Status
- **Environment**: Localhost (Port 8000).
- **Automation**: `start.sh` (Auto-install dependencies, venv, run).
- **Health Check**: `/api/status` endpoint for Ollama heartbeat.
- **Limits**: 4096 tokens, 120s timeout per request.
