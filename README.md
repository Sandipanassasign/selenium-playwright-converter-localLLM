# Selenium ➜ Playwright Converter (Local AI) 🚀

A secure, privacy-focused tool to modernize your legacy **Selenium Java** test automation by converting it to **Playwright TypeScript**. Powered by local Large Language Models (LLM) via **Ollama**.

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Python_FastAPI-blue?style=flat-square)
![AI](https://img.shields.io/badge/AI-Llama_3.2_%7C_Qwen_2.5-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🏗️ Architecture

The application follows a **3-Layer Architecture** (A.N.T.) ensuring separation of concerns:

```mermaid
graph TD
    User[User / QA Engineer] -->|Paste Java Code| UI[Web Interface (HTML/JS)]
    UI -->|POST /api/convert| API[FastAPI Server]
    
    subgraph "Local Execution Environment"
        API -->|1. Construct Prompt| Logic[Converter Logic]
        Logic -->|2. Inference Request| Ollama[Ollama LLM Server]
        Ollama -->|3. Streaming Response| Logic
        Logic -->|4. Extract Code Block| API
    end
    
    API -->|Return TypeScript| UI
    
    subgraph "Models"
        Ollama -.->|Option A| Llama[Llama 3.2]
        Ollama -.->|Option B| Qwen[Qwen 2.5 Coder]
    end
```

## ✨ Features

*   🔒 **100% Local & Secure**: Your code never leaves your machine. No API keys, no cloud data leaks.
*   🧠 **Context-Aware Conversion**: Uses AI to understand test logic, converting explicit waits to auto-waiting locators.
*   ⚡ **High Performance**: Optimized for speed with **Qwen 2.5 Coder** (1.5B) model support.
*   🎨 **Modern Interface**: Clean, glassmorphism UI with Dark Mode.
*   🚦 **Live Status**: Real-time health check for your local AI server.
*   📝 **Flexible Input**: Supports TestNG, JUnit, or raw Selenium main methods.

---

## 🛠️ Prerequisites

1.  **Ollama**: [Download & Install](https://ollama.com/)
2.  **Pull AI Models**:
    ```bash
    # Recommended (Fast & Accurate)
    ollama run qwen2.5-coder:1.5b
    
    # Optional (Balanced)
    ollama run llama3.2
    ```
3.  **Python 3.10+** (Recommended)

---

## 📦 Installation & Setup

Clone the repository and run the startup script. It handles everything:

```bash
# 1. Clone the repo
git clone https://github.com/Sandipanassasign/selenium-playwright-converter-localLLM.git
cd selenium-playwright-converter-localLLM

# 2. Make scripts executable
chmod +x start.sh stop.sh

# 3. Start the Application
./start.sh
```
> **What `start.sh` does:** Creates a Python virtual environment, installs dependencies (`fastapi`, `uvicorn`, `requests`), and launches the server on port `8000`.

---

## 🏃‍♂️ Usage Guide

1.  Open **http://localhost:8000** in your browser.
2.  **Select Model**: Choose "Qwen 2.5 Coder" for speed or "Llama 3.2" for complex logic.
3.  **Paste Code**: Input your Selenium Java code in the left panel.
    ```java
    @Test
    public void testLogin() {
        driver.findElement(By.id("user")).sendKeys("admin");
        driver.findElement(By.id("pass")).sendKeys("secret");
        driver.findElement(By.cssSelector("button.login")).click();
        Assert.assertEquals(driver.getTitle(), "Dashboard");
    }
    ```
4.  **Click Convert**: The AI will process it instantly.
5.  **Copy Result**: Get your clean Playwright TypeScript code.
    ```typescript
    test('testLogin', async ({ page }) => {
        await page.getByLabel('Username').fill('admin'); // Intelligent locator mapping
        await page.getByLabel('Password').fill('secret');
        await page.locator('button.login').click();
        await expect(page).toHaveTitle('Dashboard');
    });
    ```

---

## 🛑 Management

To stop the server and free up the port:
```bash
./stop.sh
```

## 🔧 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"Ollama Offline"** | Make sure Ollama is running (`ollama serve`). |
| **"Model not found"** | Run `ollama pull qwen2.5-coder:1.5b` in your terminal. |
| **Port 8000 in use** | Run `./stop.sh` then `./start.sh`. |
| **Conversion Hangs** | Refresh the page. If the file is massive (>500 lines), split it up. |

---

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
