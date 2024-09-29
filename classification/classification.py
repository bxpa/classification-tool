import ollama
import os
import random

input_folder = 'input'


def classify_file_content(file_path: str) -> str:
    content = open(file_path).read()
    prompt = f"""Classify the following text into one of these categories: public, confidential, or sensitive.
    Only respond with the category name, nothing else.
    Text to classify:
    {content}"""

    response = ollama.chat(model="qwen:4b", messages=[
        {"role": "system", "content": "You are a document classification assistant. Classify documents as public, confidential, or sensitive based on their content. Only respond with the category name."},
        {"role": "user", "content": prompt}
    ])

    classification = response['message']['content'].strip().lower()
    valid_categories = ['public', 'confidential', 'sensitive']

    if classification not in valid_categories:
        classification = random.choice(valid_categories)

    return classification


def main() -> None:
    files = [os.path.join(input_folder, f) for f in os.listdir(
        input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for file in files:
        try:
            classification = classify_file_content(file)
            print(f"File: {file}, Classification: {classification}")
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")


if __name__ == "__main__":
    main()
