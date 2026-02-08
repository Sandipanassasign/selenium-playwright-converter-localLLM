# Findings

## Research
- **Local LLM**: User selected **Ollama** running **codellama**.
- **Endpoint**: Standard Ollama API is usually `http://localhost:11434`.
- **Model**: `codellama` is optimized for code but can be strict. We need to ensure the system prompt discourages conversational filler ("Here is your code...") and outputs raw code or markdown blocks.

## Discoveries
- **Protocol**: B.L.A.S.T. is active.
- **Input**: Selenium Java (TestNG).
- **Core Value**: Readability > 1:1 mapping.

## Constraints
- **Model**: strictly `codellama`.
- **Environment**: Local execution.
