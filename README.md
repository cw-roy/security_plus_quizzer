# Security+ Quiz Application

An interactive command-line quiz application designed to help users practice for the CompTIA Security+ certification exam.

## Features

- Load custom question sets from JSON files
- Randomized question and answer order
- Score tracking and history
- Customizable number of questions per quiz session (up to 90)
- Progress saving in JSON format

## Disclaimer

**Important Note**: While this application is designed to help you practice for the CompTIA Security+ exam, the questions provided are not officially endorsed by CompTIA. The accuracy of the questions and answers cannot be guaranteed. Users should:

- Verify information from official CompTIA study materials
- Use this tool as supplementary practice only
- Consult current exam objectives and official study guides
- Do their own research to validate technical concepts

CompTIA Security+ certification requirements and exam content may change. Always refer to [CompTIA's official website](https://www.comptia.org) for the most up-to-date information.

## Installation

1. Ensure you have Python 3.6 or higher installed
2. Clone this repository:

```bash
git clone [repository-url]
cd security_plus_quizzer
```

### Platform-Specific Instructions

#### Linux/Unix/MacOS

1. Make the script executable:

```bash
chmod +x main.py
```

2. Run directly using:

```bash
./main.py
```

Or use Python explicitly:

```bash
python3 main.py
```

Note: On some systems, you may need to use `python3` instead of `python` to ensure you're using Python 3.x.

## Usage

### Basic Usage

Run the quiz with default settings:

```bash
python main.py
```

This will:

- Load questions from `questions.json`
- Prompt for the number of questions you want to answer
- Save scores to `scores.json`

### Command Line Options

```bash
python main.py [-h] [-f FILE] [-n NUM] [-s SCORES]
```

Options:

- `-h, --help`: Show help message
- `-f FILE, --file FILE`: Specify custom questions JSON file (default: "questions.json")
- `-n NUM, --num NUM`: Set number of questions for the quiz
- `-s SCORES, --scores SCORES`: Specify custom score file location (default: "scores.json")

### Question File Format (JSON)

Questions must be formatted in the following way (JSON):

```json
[
  {
    "question": "What is a firewall?",
    "options": [
      "A security device that monitors network traffic",
      "A type of computer virus",
      "A backup system",
      "A password manager"
    ],
    "answer": "A"
  },
  {
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "answer": "B"
  }
]
```

Each question must have:

1. A "question" field (string)
2. An "options" field (list of 4 strings)
3. An "answer" field (correct option letter: "A", "B", "C", or "D")

## Score Tracking

Scores are saved in JSON format with:

- Date and time of the quiz
- Number of correct answers
- Total number of questions

Example scores.json:

```json
[
  {
    "date": "2025-10-04T14:30:00.000000",
    "score": 8,
    "total": 10
  }
]
```

## Requirements

- Python 3.6+ (Tested in 3.10)
- Standard library modules only:
  - argparse
  - json
  - random
  - datetime
  - os

## Error Handling

The application includes error handling for:

- Invalid input files
- Malformed questions
- Invalid user input
- Missing score files
