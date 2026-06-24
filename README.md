# Code Refactoring Advisor Agent

A LangChain-powered AI agent that analyzes source code, detects common code smells, and suggests cleaner, more maintainable refactored versions while preserving the original functionality.

Built using:

* Python
* LangChain
* OpenAI GPT Models
* LangChain Tools
* Agent Tool Calling

---

# Features

The agent performs two major tasks:

### 1. Detect Code Smells

Identifies common software engineering issues such as:

* Code duplication
* Long functions
* Poor naming conventions
* Deep nesting
* Magic numbers
* Missing error handling
* High complexity
* Poor maintainability

### 2. Suggest Refactoring

Generates an improved version of the code that:

* Preserves original behavior
* Improves readability
* Improves maintainability
* Reduces complexity
* Improves naming conventions
* Removes duplication
* Adds error handling where appropriate

---

# Architecture

```text
User Code
    |
    v
LangChain Agent
    |
    +---------------------+
    |                     |
    v                     v
detect_code_smells   suggest_refactor
    |                     |
    +----------+----------+
               |
               v
      Refactoring Report
```

---

# Project Structure

```text
Code_Refactoring_Advisor_Agent.py
.env
README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -U langchain
pip install -U langchain-openai
pip install -U python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Example:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Running the Application

Execute:

```bash
python Code_Refactoring_Advisor_Agent.py
```

You will see:

```text
============================================================
CODE REFACTORING ADVISOR AGENT
Powered by LangChain + OpenAI
============================================================
```

Paste your code and finish with:

```text
EOF
```

---

# Example Input

```python
def calc(a,b,c):
    x=10

    if a>10:
        if b>5:
            if c>2:
                return a*b*c*x
            else:
                return 0
        else:
            return 0
    else:
        return 0
```

Type:

```text
EOF
```

---

# Example Output

## Detected Code Smells

```text
HIGH
- Deep nesting
- Magic number (10)
- Poor variable naming (x)

MEDIUM
- Repeated return statements
- Readability issues
```

## Suggested Refactoring

```python
MULTIPLIER = 10

def calc(a, b, c):
    if a <= 10 or b <= 5 or c <= 2:
        return 0

    return a * b * c * MULTIPLIER
```

---

# Agent Workflow

The agent follows the workflow below:

1. User submits source code.
2. Agent calls `detect_code_smells`.
3. Tool analyzes the code and identifies issues.
4. Agent calls `suggest_refactor`.
5. Tool generates a cleaner implementation.
6. Agent returns a structured refactoring report.

---

# Tools

## detect_code_smells

### Purpose

Analyze source code and identify maintainability issues.

### Input

```text
Source Code
```

### Output

```text
Prioritized Code Smell Report
```

---

## suggest_refactor

### Purpose

Generate a cleaner and more maintainable version of the code.

### Input

```text
Original Source Code
```

### Output

```text
Refactored Code
Improvement Summary
```

---

# Technologies Used

* Python 3.10+
* LangChain
* LangChain OpenAI
* OpenAI GPT Models
* Python Dotenv
* Logging

---

# Sample Use Cases

* Code Review Automation
* Technical Interview Preparation
* Developer Productivity Tools
* AI Coding Assistants
* Software Quality Analysis
* Refactoring Recommendations

---

# Future Enhancements

* AST-based code analysis
* Support for multiple programming languages
* Unit test generation
* Security vulnerability detection
* Code complexity scoring
* GitHub integration
* Export reports as PDF or Markdown

---

# Author

Code Refactoring Advisor Agent

Built using LangChain and OpenAI.
