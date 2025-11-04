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
The script expects a JSON file with the following structure:
```json
[
  {
    "Question": "Question?",
    "A": "Answer A",
    "B": "Answer B",
    "C": "Answer C",
    "D": "Answer D",
    "Answer": "A",
    "AnswerText": "Answer A",
    "Domain": "Comptia Security+ domain",
    "ExplanationText": "Conversational description of why Answer A is correct, and why the other options are incorrect."
  },
  ...
]
```

### Output
- Questions are displayed with shuffled options (A, B, C, D).
- Immediate feedback is provided ("Correct!" or "Incorrect. Correct answer: X").
- Final score is displayed as `score/total (percentage%)`.
- Scores are saved to the specified scores file with metadata.

### Scores File Format
The scores file (`scores.json`) stores quiz results as a list of entries:
```json
[
  {
    "date": "2025-10-22T12:30:00.123456",
    "score": 18,
    "total": 20,
  },
  ...
]
```
- I will probably add functionality for reviewing incorrect answers at some point. 

## Example Interaction
```
How many questions? (1-90): 3

An organization is designing its network infrastructure using Zero Trust principles. Which core tenet requires all assets and workflows to be continuously verified before being granted or keeping access to data or applications?
A. Access Limitation
B. Limit the "Blast Radius"
C. Assume all network connections are insecure
D. Continuous Verification
Your answer (A/B/C/D): D
Correct!
Explanation: Continuous Verification

[... more questions ...]

Score: 2/3 (66.7%)
Score saved to scores.json
```

## Development
- **Testing**: Test with `questions_main.json` to ensure compatibility. Verify score saving with multiple runs and check handling of corrupted scores files.
- **Extending**: Add features like question category filtering or retrying incorrect questions by modifying the `run_quiz` function.