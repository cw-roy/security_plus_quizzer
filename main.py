#!/usr/bin/env python3

import argparse
import json
import os
import random
from datetime import datetime


def load_data(filename):
    """Parse text file into list of dicts: {'question': str, 'options': list, 'answer': str}"""
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


def run_quiz(questions, num_questions):
    """Run randomized quiz and return score."""
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


def save_score(scores_file, score, total):
    """Append score to JSON file."""
    entry = {"date": datetime.now().isoformat(), "score": score, "total": total}
    if os.path.exists(scores_file):
        with open(scores_file, "r") as f:
            scores = json.load(f)
    else:
        scores = []
    scores.append(entry)
    with open(scores_file, "w") as f:
        json.dump(scores, f, indent=4)


def main():
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
