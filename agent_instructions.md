# 🧠 GitHub Copilot Agent Instructions

This file contains structured tasks for GitHub Copilot Agent to analyze, plan, and execute across the Flask web project. You can paste these one-by-one into the Agent Chat in VS Code or let the agent read this file if prompted.

---

## 📌 Objective

Enhance the existing Flask app by adding features, improving code structure, and introducing tests and documentation.

---

## ✅ TASK 1: Add Error Handling

**Goal:** Prevent empty name submissions and inform the user with a friendly message.

**Instructions:**
- Modify `app.py` to validate the input in the POST request.
- If the name is empty, re-render the form with an error message.
- Update the HTML template (`index.html`) to display the error message if provided.

---

## ✅ TASK 2: Log Submissions

**Goal:** Record submitted names into a text file for persistence.

**Instructions:**
- Create a file named `submissions.log`.
- Append each submitted name to the file.
- Make sure duplicate empty lines are not written.

---

## ✅ TASK 3: Add a Submissions Page

**Goal:** Display all names that have been submitted.

**Instructions:**
- Create a new route `/submissions`.
- Read from `submissions.log`.
- Render the list of names in a new HTML template.
- Link to this page from the homepage.

---

## ✅ TASK 4: Add Unit Tests

**Goal:** Improve test coverage and catch regressions.

**Instructions:**
- Add a test to verify that submitting an empty name does not render the greeting.
- Add a test to check the contents of `/submissions` after a name is posted.

---

## ✅ TASK 5: Improve Styling

**Goal:** Make the UI more user-friendly using Bootstrap.

**Instructions:**
- Include Bootstrap via CDN in `index.html` and the new submissions page.
- Use form groups, button styling, and spacing utilities to improve layout.

---

## ✅ TASK 6: Dockerize the Application (Optional)

**Goal:** Prepare the app for containerized deployment.

**Instructions:**
- Create a `Dockerfile` to build the app.
- Add a `.dockerignore` file.
- Optionally create a `docker-compose.yml` for development use.

---

## 🧪 Bonus: Create REST API Endpoints

**Goal:** Extend the app with API routes.

**Instructions:**
- Add a `/api/submissions` route that returns all names as JSON.
- Add a `/api/submit` POST route that accepts a JSON payload with `name`.

---

## 💬 Notes for Copilot Agent

- If any files don’t exist yet, create them.
- If templates are needed, create them in the `templates/` folder.
- Only apply changes after reviewing with the user.
