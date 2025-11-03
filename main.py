#!/usr/bin/env python3
"""
Quiz Application
A command-line quiz application I built for practicing CompTIA Security+ exam
questions. This could be used for other multiple-choice quizzes as well. See the
README for details, specifically the expected format of the questions JSON file.

The application loads questions from a JSON file, presents them one at a time,
and tracks user scores over time.

Usage:
    python main.py [-f FILE] [-n NUM] [-s SCORES]

Example:
    python main.py --file questions_main.json --num 20 --scores history.json
"""

import argparse
import json
import os
import random
from datetime import datetime


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def load_data(filename: str) -> list[dict]:
    """
    Load questions from a JSON file into a list of question dictionaries.
    Args:
        filename (str): Path to the JSON file containing quiz questions.
            File must have a 'questions' key with a list of dicts, each with:
            - 'Question': str
            - 'A', 'B', 'C', 'D': str (options)
            - 'Answer': str (letter A, B, C, or D)
            - 'AnswerText': str
    Returns:
        list[dict]: List of question dictionaries with keys:
            - 'question': str
            - 'options': list[str]
            - 'answer': str
            - 'answer_text': str
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file format is invalid
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file must be a list of question objects.")

    questions = []
    for q in data:
        required_keys = ["Question", "A", "B", "C", "D", "Answer", "AnswerText"]
        if not all(k in q for k in required_keys):
            raise ValueError(
                "Each question must have 'Question', 'A', 'B', 'C', 'D', 'Answer', and 'AnswerText' keys."
            )
        if q["Answer"] not in ["A", "B", "C", "D"]:
            raise ValueError("Answer must be one of 'A', 'B', 'C', 'D'.")

        question = {
            "question": q["Question"],
            "options": [q["A"], q["B"], q["C"], q["D"]],
            "answer": q["Answer"],
            "answer_text": q["AnswerText"],
        }
        questions.append(question)

    return questions


def run_quiz(questions: list[dict], num_questions: int) -> tuple[int, int]:
    """
    Present a randomized quiz to the user and track their score.
    Args:
        questions (list[dict]): List of question dictionaries, each containing
            'question', 'options', 'answer', and 'answer_text' keys
        num_questions (int): Number of questions to present from the pool.
            Will be capped at the total number of available questions.
    Returns:
        tuple[int, int]: A tuple containing:
            - Number of correct answers (score)
            - Total number of questions asked
    Note:
        Prints each question with multiple choice options, provides
        immediate feedback on correctness, and displays the correct answer
        explanation for both correct and incorrect answers.
    """
    if num_questions > len(questions):
        num_questions = len(questions)
    selected = random.sample(questions, num_questions)
    score = 0
    option_letters = ["A", "B", "C", "D"]
    question_num = 1

    for q in selected:
        clear_screen()
        print(f"Question {question_num} of {num_questions}\n")
        print(f"{q['question']}")
        correct_index = option_letters.index(q["answer"])
        correct_text = q["options"][correct_index]

        shuffled = list(enumerate(q["options"]))
        random.shuffle(shuffled)

        new_correct_index = next(
            idx for idx, (orig_idx, opt) in enumerate(shuffled) if opt == correct_text
        )

        for idx, (orig_idx, opt) in enumerate(shuffled):
            print(f"{option_letters[idx]}. {opt}")

        while True:
            user_ans = input("Your answer (A/B/C/D): ").upper().strip()
            if user_ans in option_letters:
                break
            print("Invalid input. Please enter A, B, C, or D.")

        if user_ans == option_letters[new_correct_index]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {option_letters[new_correct_index]}")
        print(f"Explanation: {q['answer_text']}\n")

        if question_num < num_questions:
            input("Press Enter for next question...")
        else:
            input("Press Enter to see your final score...")
        question_num += 1

    clear_screen()
    percentage = (score / num_questions) * 100 if num_questions > 0 else 0
    print(f"\nFinal Score: {score}/{num_questions} ({percentage:.1f}%)")
    return score, num_questions


def save_score(scores_file: str, score: int, total: int) -> None:
    """
    Save quiz results to a JSON file for tracking progress over time.
    Args:
        scores_file (str): Path to the JSON file for storing scores
        score (int): Number of correct answers from the quiz
        total (int): Total number of questions asked
    Note:
        Creates a new file if it doesn't exist, or appends to existing file.
        Each entry includes timestamp, score, and total questions.
    """
    entry = {"date": datetime.now().isoformat(), "score": score, "total": total}
    scores = []
    if os.path.exists(scores_file):
        try:
            with open(scores_file, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {scores_file} is corrupted. Starting a new scores file.")

    if not isinstance(scores, list):
        scores = []

    scores.append(entry)
    with open(scores_file, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4)


def main() -> None:
    """Main entry point for the Security+ Quiz application.
    Handles command-line argument parsing, question loading, quiz execution,
    and score saving. Supports interactive mode for selecting number of
    questions when not specified via command line.
    Command-line Arguments:
        -f, --file: Path to questions JSON file (default: questions.json)
        -n, --num: Number of questions to ask (optional)
        -s, --scores: Path to scores file (default: scores.json)
    """
    parser = argparse.ArgumentParser(description="CompTIA Security+ Quiz")
    parser.add_argument(
        "-f", "--file", default="questions_main.json", help="Questions JSON file"
    )
    parser.add_argument("-n", "--num", type=int, help="Number of questions")
    parser.add_argument("-s", "--scores", default="scores.json", help="Scores file")
    args = parser.parse_args()

    try:
        questions = load_data(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    if not questions:
        print("No questions loaded.")
        return

    if args.num is None:
        while True:
            try:
                num = int(input(f"How many questions? (1-{min(90, len(questions))}): "))
                if 1 <= num <= min(90, len(questions)):
                    args.num = num
                    break
                else:
                    print(
                        f"Please enter a number between 1 and {min(90, len(questions))}."
                    )
            except ValueError:
                print("Please enter a valid integer.")
    else:
        if args.num <= 0:
            print("Number of questions must be positive.")
            return
        args.num = min(args.num, len(questions))

    score, total = run_quiz(questions, args.num)
    try:
        save_score(args.scores, score, total)
        print(f"Score saved to {args.scores}")
    except Exception as e:
        print(f"Error saving score: {e}")


if __name__ == "__main__":
    main()
