import ollama
import os
import streamlit as st

INPUT_FOLDER = 'input'


@st.cache_data
def classify_file_content(file_path: str) -> str:
    content = open(file_path).read()
    prompt: str = f"""Classify the following text into one of these categories: public, confidential, or sensitive.
    Only respond with the category name, nothing else.
    Text to classify:
    {content}"""

    response = ollama.chat(model="qwen:4b", messages=[
        {"role": "system", "content":
         "You are a file classification assistant. Classify documents in these categories: public, confidential, or sensitive based on their content. Only respond with a single category name."
         },
        {"role": "user", "content": prompt}
    ])

    classification: str = response['message']['content'].strip().lower()
    valid_categories: list = ['public', 'confidential', 'sensitive']
    if classification not in valid_categories:
        raise Exception('Could not classify file', 400)
    return classification


def main() -> None:
    files = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(
        INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]

    for file in files:
        try:
            classification = classify_file_content(file)
            print(f"File: {file}, Classification: {classification}")
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")


if __name__ == "__main__":
    main()
