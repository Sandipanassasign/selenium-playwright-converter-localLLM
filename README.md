# Selenium ➜ Playwright Converter (Local AI)

A secure, local-first tool to convert legacy **Selenium Java (TestNG)** code into modern **Playwright TypeScript**. Powered by **Ollama** and **Llama 3.2**.

![Status](https://img.shields.io/badge/Status-Active-success)
![AI](https://img.shields.io/badge/AI-Local_Ollama-orange)

## 🚀 Features

*   **Zero Data Leakage**: Runs 100% locally. Your code never leaves your machine.
*   **Smart Conversion**: Uses Llama 3.2 to understand logic, not just regex.
*   **Modern UI**: Glassmorphism design with Dark Mode.
*   **Real-time Status**: Live indicator for Ollama connectivity.
*   **Flexible Input**: Converts any Java Selenium code (TestNG, JUnit, or main methods).

## 🛠️ Prerequisites

1.  **Ollama**: [Download Ollama](https://ollama.com/)
2.  **Models**:
    ```bash
    # For fastest performance (Recommended)
    ollama run qwen2.5-coder:1.5b
    
    # Optional: Balanced model
    ollama run llama3.2
    ```
3.  **Python 3.10+**

## 📦 Installation

Clone this repository and run the setup script:

```bash
# 1. give permission to scripts
chmod +x start.sh stop.sh

# 2. Run the start script (Installs dependencies automatically)
./start.sh
```

## 🏃‍♂️ Usage

1.  Open **http://localhost:8000** in your browser.
2.  **Source Box (Left)**: Paste your Selenium Java method (must include `@Test`).
3.  Click **Generic Convert**.
4.  **Output Box (Right)**: Copy the generated Playwright code.

### Example Input
```java
@Test
public void loginTest() {
    driver.findElement(By.id("user")).sendKeys("admin");
    driver.findElement(By.id("login")).click();
}
```

### Example Output
```typescript
test('loginTest', async ({ page }) => {
    await page.getByLabel('user').fill('admin');
    await page.locator('#login').click();
});
```

## 🛑 Stopping the Server

To stop the server and free up port 8000:

```bash
./stop.sh
```

## 🔧 Troubleshooting

*   **"Ollama Offline"**: Ensure Ollama is running (`ollama serve`).
*   **"Processing..." hangs**: Try refreshing. If your file is huge (>500 lines), split it into smaller chunks.
*   **"Address already in use"**: Run `./stop.sh` then `./start.sh`.

## 📂 Project Structure

*   `server.py`: FastAPI backend.
*   `tools/`: Core AI logic & file operations.
*   `static/`: Frontend (HTML/CSS/JS).
*   `architecture/`: System prompts & SOPs.
