# Quiz Application

A command-line quiz application I developed for practicing CompTIA Security+ exam questions.
This could be used for other multiple-choice quizzes as well. See below for details,
specifically the expected format of the questions JSON file. It loads questions from a JSON
file, presents them in random order, and tracks user scores over time.

## Features

- Loads questions from a JSON file (`questions_main.json`).
  - NOTE: The example question bank here is not guaranteed to be accurate, although I've made my best effort. Use at your own risk.
- Randomizes question order and answer options for varied practice.
- Displays the correct answer (`AnswerText`) for both correct and incorrect responses to reinforce learning.
- Saves quiz results to a JSON file, including:
  - Timestamp
  - Score and total questions
- Supports command-line arguments for customizing the quiz file, number of questions, and scores file.
- Interactive mode for selecting the number of questions if not specified.
- Error handling for file loading, JSON validation, and user input.

## Requirements

- Python 3.6+ (built and tested on 3.10)
- No external dependencies

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cw-roy/security_plus_quizzer.git
   cd security_plus_quizzer
   ```
2. Ensure `questions_main.json` is in the project directory or provide a path to your own question file.

## Usage

Run the script with default settings:

```bash
python3 main.py
```

### Command-Line Arguments

- `-f, --file`: Path to the questions JSON file (default: `questions.json`).
- `-n, --num`: Number of questions to ask (optional; prompts interactively if omitted).
- `-s, --scores`: Path to the scores JSON file (default: `scores.json`).

Example:

```bash
python3 main.py --file questions_master.json --num 20 --scores history.json
```

### Input JSON Format

The script expects a JSON file with the following structure (top-level list of question objects):

```json
[
  {
    "Question": "Question text?",
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D",
    "Answer": "A",           // Correct option letter
    "AnswerText": "Option A", // Text of the correct answer
    "Domain": "Domain name", // e.g. 'Security architecture'
    "ExplanationText": "Detailed explanation of why the answer is correct and others are not."
  },
  ...
]
```

### Output

- Questions are displayed with shuffled options (A, B, C, D).
- Immediate feedback is provided ("Correct!" or "Incorrect!").
- The correct answer and its text are shown after each question.
- If you answer incorrectly, a detailed explanation is displayed.
- Final score is displayed as `score/total (percentage%)`.
- Domain breakdown is shown at the end, with per-domain scores and advice on weak areas.
- Scores are saved to the specified scores file with metadata, including domain stats.

### Scores File Format

The scores file (`scores.json`) stores quiz results as a list of entries:

```json
[
  {
    "date": "2025-10-22T12:30:00.123456",
    "score": 18,
    "total": 20,
    "domain_stats": {
      "Security architecture": {"correct": 5, "total": 7},
      "General security concepts": {"correct": 4, "total": 5},
      // ...
    }
  },
  ...
]
```

## Example Interaction

```
How many questions? (1-90): 3

Question 1 of 3
Which core tenet requires all assets and workflows to be continuously verified before being granted or keeping access to data or applications?
A. Access Limitation
B. Limit the "Blast Radius"
C. Assume all network connections are insecure
D. Continuous Verification
Your answer (A/B/C/D): D
Correct!
The correct answer is D. Continuous Verification

Question 2 of 3
...etc...

Quiz Complete!
Overall Score: 2/3 (66.7%)
Domain Breakdown:
  • Security architecture: 1/2 (50.0%)
  • General security concepts: 1/1 (100.0%)
Lowest score: Security architecture (50.0%)
Advice: Focus more study on the domain(s) above.
Score saved to scores.json
```

## Development

- **Testing**: Test with `questions_main.json` to ensure compatibility. Verify score saving with multiple runs and check handling of corrupted scores files.
- **Extending**: Add features like question category filtering, retrying incorrect questions, or customizing domain breakdown by modifying the `run_quiz` function.
