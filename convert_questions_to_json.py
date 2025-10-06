import json
import re

INPUT_FILE = "questions.txt"
OUTPUT_FILE = "questions.json"


def parse_questions(filename):
    questions = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    while i < len(lines):
        if lines[i].startswith("Question "):
            # Extract question text
            question_text = (
                lines[i].split(":", 1)[1].strip() if ":" in lines[i] else lines[i]
            )
            i += 1
            options = []
            # Collect options (A-D)
            while i < len(lines) and re.match(r"^[A-D]\)", lines[i]):
                # Remove 'A) ' etc. from start
                opt_text = lines[i][3:].strip() if len(lines[i]) > 3 else lines[i]
                options.append(opt_text)
                i += 1
            # Get answer
            answer = None
            if i < len(lines) and lines[i].startswith("Answer:"):
                answer = lines[i].replace("Answer:", "").strip()
                i += 1
            if question_text and options and answer:
                questions.append(
                    {"question": question_text, "options": options, "answer": answer}
                )
        else:
            i += 1
    return questions


def main():
    questions = parse_questions(INPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Converted {len(questions)} questions to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
