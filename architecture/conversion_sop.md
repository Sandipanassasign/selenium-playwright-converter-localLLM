# SOP: Selenium Java to Playwright Conversion

## 1. Objective
Convert Selenium Java (TestNG) code to Playwright TypeScript/JavaScript with high readability and modern practices.

## 2. Prompt Engineering Strategy
The prompt sent to the LLM must follow this structure:

### System / Context
"You are an expert Automation Engineer. Convert the following Selenium Java code to Playwright TypeScript. 
- Use `async/await`.
- Use `test` and `expect` from `@playwright/test`.
- Prefer `page.getBy...` locators where semantic.
- Do NOT include conversational text. Output ONLY the code."

### Input Format
```java
// Selenium Code
@Test
public void login() {
    driver.findElement(By.id("user")).sendKeys("admin");
    driver.findElement(By.id("pass")).click();
}
```

### Expected Output Format
```typescript
import { test, expect } from '@playwright/test';

test('login', async ({ page }) => {
  await page.getByLabel('User').fill('admin'); // inferred or exact locator
  await page.locator('#pass').click();
});
```

## 3. Heuristics & Rules
- **Waits**: Remove `Thread.sleep` and explicit `WebDriverWait` unless necessary (Playwright auto-waits).
- **Assertions**: Convert `Assert.assertEquals` -> `await expect(...).toHaveText(...)` or similar.
- **Page Objects**: If the input uses Page Factory, attempt to convert to a class-based POM in JS/TS.

## 4. Error Handling
- If the model returns markdown code blocks (```typescript ... ```), the tool must strip them.
- If the model returns conversational filler ("Here is the code:"), the tool must strip it or extract the code block.
