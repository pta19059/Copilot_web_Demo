# 🚀 Copilot Demo Prompts

This file contains ready-to-use prompt examples for GitHub Copilot across its three main modes: Ask, Edits, and Agent Mode.

---

## 🎯 ASK Mode

> Select a line or function → `Cmd/Ctrl + I` → Type your question

### Recommended prompts:
- "What does this route do?"
- "How does Flask handle form submissions here?"
- "Are there any edge cases missing in this function?"
- "Explain what would happen if name is None"
- "Can you refactor this function to be cleaner?"

---

## 🔧 EDIT Mode

> Select a block of code → `Cmd/Ctrl + I` → Type your instruction (inline modification)

### Suggested prompts:
- "Add input validation: show an error if the name is empty"
- "Refactor to use separate templates for GET and POST"
- "Add logging for each form submission"
- "Sanitize input to prevent script injection"
- "Add comments to explain the logic"

---

## 🤖 AGENT MODE

> Open Copilot Chat → Select "Agent" → Enter one of the following prompts:

### Advanced prompts:
- "Create a new page that lists all submitted names and add navigation"
- "Add a form with email input and validate it using regex"
- "Save submitted names to a file and read them on reload"
- "Add Bootstrap for styling and improve layout"
- "Add unit tests for empty input and invalid characters"
- "Convert the Flask app into a FastAPI app"
- "Dockerize the application with a Dockerfile and docker-compose.yml"
- "Create a REST API that returns the list of names as JSON"

---

## 🧪 Test Suggestions (`test_app.py`)

### Prompts:
- "Add test to check that submitting an empty name does not show greeting"
- "Add test to simulate a POST request with missing data"
- "Add performance benchmark test for 1000 requests"

---

## ✅ Demo Tips

- In **Agent Mode**, review the plan before accepting.
- In **Edit Mode**, review the diff before applying.
- In **Ask Mode**, highlight how Copilot explains the context of the code.

---

👍 Use these examples to demonstrate how Copilot can:
- Generate new features
- Improve existing code
- Perform intelligent refactoring
