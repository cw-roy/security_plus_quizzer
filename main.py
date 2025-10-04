#!/usr/bin/env python3
"""
Security+ Quiz Application

A command-line quiz application for practicing CompTIA Security+ exam questions.
The application loads questions from a text file, presents them in random order,
and tracks user scores over time.

Usage:
    python main.py [-f FILE] [-n NUM] [-s SCORES]

Example:
    python main.py --file my_questions.txt --num 20 --scores history.json
"""

import argparse
import json
import os
import random
from datetime import datetime


def load_data(filename: str) -> list[dict]:
    """
    Parse a formatted text file into a list of question dictionaries.

    Args:
        filename (str): Path to the text file containing quiz questions.
            File must follow the format:
            Question N: text
            A) option1
            B) option2
            C) option3
            D) option4
            Answer: correct_letter

    Returns:
        list[dict]: List of question dictionaries, each containing:
            - 'question': str - The question text
            - 'options': list[str] - List of 4 answer options
            - 'answer': str - Correct answer letter (A/B/C/D)

    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file format is invalid
    """
    questions = []
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    i = 0
    while i < len(lines):
        if lines[i].startswith("Question "):  # Assume format: Question N: text
            question = (
                lines[i].split(":", 1)[1].strip()
                if ":" in lines[i]
                else lines[i].strip()
            )
            i += 1
            options = []
            while i < len(lines) and any(
                lines[i].startswith(prefix) for prefix in ("A)", "B)", "C)", "D)")
            ):
                options.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].startswith("Answer:"):
                answer = lines[i].replace("Answer:", "").strip()
                questions.append(
                    {"question": question, "options": options, "answer": answer}
                )
                i += 1
            else:
                i += 1  # Skip malformed
        else:
            i += 1
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
        for opt in q["options"]:
            print(opt)
        user_ans = input("Your answer (A/B/C/D): ").upper().strip()
        if user_ans == q["answer"].upper():
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {q['answer']}")
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
        -f, --file: Path to questions file (default: questions.txt)
        -n, --num: Number of questions to ask (optional)
        -s, --scores: Path to scores file (default: scores.json)
    """
    parser = argparse.ArgumentParser(description="CompTIA Security+ Quiz")
    parser.add_argument("-f", "--file", default="questions.txt", help="Questions file")
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
