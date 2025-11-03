#!/usr/bin/env python3
"""
Quiz Application
A command-line quiz application for practicing CompTIA Security+ exam questions.
Supports JSON question banks with the new structure (top-level list, Domain, ExplanationText).

Usage:
    python main.py [-f FILE] [-n NUM] [-s SCORES]

Example:
    python main.py --file questions.json --num 20 --scores history.json
"""

import argparse
import json
import os
import random
import shutil
import textwrap
from collections import defaultdict
from datetime import datetime

# Constants

WIDTH = 80

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear" if os.name == "posix" else "cls")


def wrap_text(text: str, initial_indent: str = "", subsequent_indent: str = "") -> str:
    """Wrap text to WIDTH characters, preserving words and handling indentation."""
    try:
        terminal_width = shutil.get_terminal_size(fallback=(WIDTH, 24)).columns
        wrap_width = min(WIDTH, terminal_width)
    except Exception:
        wrap_width = WIDTH
    
    return textwrap.fill(
        text,
        width=wrap_width,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        break_on_hyphens=False
    )


def load_data(filename: str) -> list[dict]:
    """
    Load questions from a JSON file (top-level list of question objects).
    Args:
        filename (str): Path to the JSON file.
    Returns:
        list[dict]: List of processed question dicts.
    Raises:
        FileNotFoundError, ValueError: On invalid file or format.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file must be a list of question objects.")

    questions = []
    option_letters = ["A", "B", "C", "D"]
    required_keys = ["Question", "A", "B", "C", "D", "Answer", "AnswerText", "Domain", "ExplanationText"]

    for q in data:
        missing = [k for k in required_keys if k not in q]
        if missing:
            raise ValueError(f"Missing keys in question '{q.get('Question', 'Unknown')}': {', '.join(missing)}")

        if q["Answer"] not in option_letters:
            raise ValueError(f"Invalid Answer in question '{q['Question']}'")

        # Verify AnswerText matches the correct option
        correct_option_key = q["Answer"]
        if q["AnswerText"] != q[correct_option_key]:
            print(f"Warning: AnswerText mismatch in question '{q['Question']}'")

        question = {
            "question": q["Question"],
            "options": [q["A"], q["B"], q["C"], q["D"]],
            "answer_letter": q["Answer"],
            "answer_text": q["AnswerText"],
            "domain": q["Domain"],
            "explanation_text": q["ExplanationText"],
        }
        questions.append(question)

    return questions


def run_quiz(questions: list[dict], num_questions: int) -> tuple[int, int, dict]:
    """
    Run the quiz with shuffled options and domain tracking.
    Returns:
        tuple: (score, total_questions, domain_stats dict)
    """
    if num_questions > len(questions):
        num_questions = len(questions)

    selected = random.sample(questions, num_questions)
    score = 0
    domain_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    option_letters = ["A", "B", "C", "D"]

    for i, q in enumerate(selected, 1):
        domain = q["domain"]
        domain_stats[domain]["total"] += 1

        clear_screen()
        print(wrap_text(f"Question {i} of {num_questions}") + "\n")
        print(wrap_text(q['question']) + "\n")

        correct_text = q["answer_text"]
        shuffled_options = q["options"][:]
        random.shuffle(shuffled_options)
        letter_to_opt = {letter: opt for letter, opt in zip(option_letters, shuffled_options)}

        # Find shuffled correct letter
        correct_shuffled_letter = next(
            letter for letter, opt in letter_to_opt.items() if opt == correct_text
        )

        for letter in option_letters:
            print(wrap_text(letter_to_opt[letter], 
                          initial_indent=f"{letter}. ",
                          subsequent_indent="   "))

        print()
        while True:
            user_ans = input("Your answer (A/B/C/D): ").upper().strip()
            if user_ans in option_letters:
                break
            print(wrap_text("Invalid input. Please enter A, B, C, or D."))

        correct = user_ans == correct_shuffled_letter
        if correct:
            score += 1
            domain_stats[domain]["correct"] += 1

        print()
        if correct:
            print(wrap_text("Correct!"))
        else:
            print(wrap_text("Incorrect!"))

        print(wrap_text(f"The correct answer is {correct_shuffled_letter}. {correct_text}"))

        if not correct:
            print("\nDetailed Explanation:")
            print(wrap_text(q["explanation_text"]))

        print()
        if i < num_questions:
            input(wrap_text("Press Enter for the next question..."))
        else:
            input(wrap_text("Press Enter to view your score..."))

    return score, num_questions, dict(domain_stats)


def save_score(scores_file: str, score: int, total: int, domain_stats: dict) -> None:
    """
    Save quiz results (including domain stats) to JSON.
    """
    entry = {
        "date": datetime.now().isoformat(),
        "score": score,
        "total": total,
        "domain_stats": domain_stats,
    }
    scores = []
    if os.path.exists(scores_file):
        try:
            with open(scores_file, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {scores_file} corrupted. Starting new file.")

    if not isinstance(scores, list):
        scores = []

    scores.append(entry)
    with open(scores_file, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4)


def main() -> None:
    parser = argparse.ArgumentParser(description="CompTIA Security+ Quiz")
    parser.add_argument("-f", "--file", default="questions_main.json", help="Questions JSON file")
    parser.add_argument("-n", "--num", type=int, help="Number of questions")
    parser.add_argument("-s", "--scores", default="scores.json", help="Scores file")
    args = parser.parse_args()

    try:
        questions = load_data(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading questions: {e}")
        return

    if not questions:
        print("No questions found.")
        return

    max_questions = min(90, len(questions))
    if args.num is None:
        while True:
            try:
                num = int(input(f"How many questions? (1-{max_questions}): "))
                if 1 <= num <= max_questions:
                    args.num = num
                    break
                print(f"Please enter 1-{max_questions}.")
            except ValueError:
                print("Enter a valid number.")
    else:
        args.num = min(args.num, max_questions)
        if args.num < 1:
            print("Number of questions must be positive.")
            return

    score, total, domain_stats = run_quiz(questions, args.num)

    clear_screen()
    print(wrap_text("Quiz Complete!") + "\n")
    percentage = (score / total * 100) if total > 0 else 0
    print(wrap_text(f"Overall Score: {score}/{total} ({percentage:.1f}%)") + "\n")

    if domain_stats:
        print(wrap_text("Domain Breakdown:"))
        sorted_domains = sorted(domain_stats.keys())
        percs = {}
        for d in sorted_domains:
            c = domain_stats[d]["correct"]
            t = domain_stats[d]["total"]
            p = (c / t * 100) if t > 0 else 0
            percs[d] = p
            print(wrap_text(f"  • {d}: {c}/{t} ({p:.1f}%)", subsequent_indent="    "))

        if percs:
            min_p = min(percs.values())
            poor_domains = [d for d, p in percs.items() if p == min_p]
            if len(set(percs.values())) == 1:
                print("\n" + wrap_text("Balanced performance across domains."))
            else:
                poor_str = ", ".join(poor_domains)
                print("\n" + wrap_text(f"Lowest score: {poor_str} ({min_p:.1f}%)"))
                print(wrap_text("Advice: Focus more study on the domain(s) above."))

        if score == total:
            print("\nPerfect overall score! Excellent work.")
    else:
        print("No domain data available.")

    try:
        save_score(args.scores, score, total, domain_stats)
        print(f"\nScore saved to {args.scores}")
    except Exception as e:
        print(f"Error saving score: {e}")


if __name__ == "__main__":
    main()