# AI Log Analysis Agent - Version 1

A simple Windows desktop application for QA/SDET log analysis.

## What it does

1. Lets you select a folder.
2. Finds all `.log` files in that folder.
3. Lets you select a log file.
4. Opens the selected log in Windows Notepad.
5. Accepts a keyword.
6. Searches the complete file line-by-line.
7. Displays every complete line containing the keyword.
8. Displays the original line number and total match count.
9. Search is case-insensitive.
10. Handles malformed characters without stopping the search.

## Requirements

- Windows
- Python 3.9+ recommended
- No external Python packages are required.

## Run

Open Command Prompt in this project folder and run:

```text
python app.py
```

If `python` is not recognized, try:

```text
py app.py
```

## How to use

### Step 1
Click **Select Log Folder**.

Example:

```text
C:\Automation\Logs
```

### Step 2
Choose the required `.log` file from the dropdown.

### Step 3
Click **Open in Notepad** if you want to inspect the original log.

### Step 4
Enter a keyword such as:

```text
ERROR
```

or:

```text
timeout
```

or:

```text
Database
```

### Step 5
Click **Search Log**.

Example output:

```text
File: C:\Automation\Logs\execution.log
Keyword: timeout
Matches Found: 3

Line 124: 2026-09-29 10:21:34 ERROR Database connection timeout
Line 189: 2026-09-29 10:23:41 ERROR API request timeout
Line 245: 2026-09-29 10:26:18 WARN Connection timeout; retrying
```

## Architecture

```text
User
  |
  v
Select Folder
  |
  v
Find *.log
  |
  v
Select Log File
  |
  +------> Open in Notepad
  |
  v
Enter Keyword
  |
  v
Line-by-Line Search
  |
  v
Matching Complete Lines
  |
  v
Display Line Number + Match Count
```

## Important design choice

Version 1 uses deterministic text searching rather than an LLM.

This is intentional. For log search, the agent should return the actual source lines without hallucinating or omitting evidence.

An AI layer can be added in Version 2 for:
- error classification
- stack trace extraction
- grouping repeated failures
- context analysis
- root-cause hints
- natural-language questions
- summaries

## Project structure

```text
AI_Log_Analysis_Agent_v1/
|
|-- app.py
|-- README.md
|-- logs/
|-- tests/
```

## Suggested test cases

- Search an existing keyword.
- Search a keyword with different capitalization.
- Search a keyword that does not exist.
- Select a folder containing multiple `.log` files.
- Select a folder containing no `.log` files.
- Search a large log.
- Search a log containing Unicode characters.
- Open the log in Notepad.
- Press Enter after typing a keyword.
