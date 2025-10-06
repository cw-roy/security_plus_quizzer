#!/usr/bin/env python3
"""
Security+ Quiz Application

A command-line quiz application for practicing CompTIA Security+ exam questions.
The application loads questions from a JSON file, presents them in random order,
and tracks user scores over time.

Usage:
    python main.py [-f FILE] [-n NUM] [-s SCORES]

Example:
    python main.py --file my_questions.json --num 20 --scores history.json
"""

import argparse
import json
import os
import random
from datetime import datetime


def load_data(filename: str) -> list[dict]:
    """
    Load questions from a JSON file into a list of question dictionaries.

    Args:
        filename (str): Path to the JSON file containing quiz questions.
            File must be a list of dicts with keys:
            - 'question': str
            - 'options': list[str]
            - 'answer': str

    Returns:
        list[dict]: List of question dictionaries.

    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file format is invalid
    """
    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)
    # Basic validation
    if not isinstance(questions, list):
        raise ValueError("JSON file must contain a list of questions.")
    for q in questions:
        if not all(k in q for k in ("question", "options", "answer")):
            raise ValueError(
                "Each question must have 'question', 'options', and 'answer' keys."
            )
    return questions


def run_quiz(questions: list[dict], num_questions: int) -> tuple[int, int]:
    """
    Present a randomized quiz to the user and track their score.

    Args:
        questions (list[dict]): List of question dictionaries, each containing
            'question', 'options', and 'answer' keys
        num_questions (int): Number of questions to present from the pool.
            Will be capped at the total number of available questions.

    Returns:
        tuple[int, int]: A tuple containing:
            - Number of correct answers (score)
            - Total number of questions asked

    Note:
        Prints each question with multiple choice options and provides
        immediate feedback on correctness. Displays final score as both
        raw numbers and percentage.
    """
    if num_questions > len(questions):
        num_questions = len(questions)
    selected = random.sample(questions, num_questions)
    score = 0
    for q in selected:
        print(f"\n{q['question']}")
        option_letters = ["A", "B", "C", "D"]
        options = q["options"][:]
        correct_index = (
            option_letters.index(q["answer"]) if q["answer"] in option_letters else 3
        )
        # Track the correct answer text before shuffling
        correct_text = options[correct_index]
        # Shuffle options
        shuffled = list(enumerate(options))
        random.shuffle(shuffled)
        # Find new index of correct answer
        new_correct_index = None
        for idx, (orig_idx, opt) in enumerate(shuffled):
            if opt == correct_text:
                new_correct_index = idx
        # Display shuffled options
        for idx, (orig_idx, opt) in enumerate(shuffled):
            print(f"{option_letters[idx]}. {opt}")
        user_ans = input("Your answer (A/B/C/D): ").upper().strip()
        if user_ans == option_letters[new_correct_index]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {option_letters[new_correct_index]}")
    percentage = (score / num_questions) * 100 if num_questions > 0 else 0
    print(f"\nScore: {score}/{num_questions} ({percentage:.1f}%)")
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
    if os.path.exists(scores_file):
        with open(scores_file, "r") as f:
            scores = json.load(f)
    else:
        scores = []
    scores.append(entry)
    with open(scores_file, "w") as f:
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
        "-f", "--file", default="questions.json", help="Questions JSON file"
    )
    parser.add_argument("-n", "--num", type=int, help="Number of questions")
    parser.add_argument("-s", "--scores", default="scores.json", help="Scores file")
    args = parser.parse_args()

    questions = load_data(args.file)
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
        args.num = min(args.num, len(questions))

    score, total = run_quiz(questions, args.num)
    save_score(args.scores, score, total)
    print(f"Score saved to {args.scores}")


if __name__ == "__main__":
    main()
