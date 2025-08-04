from src.main_pipeline import process_form

def main():
    print("Hello from az-ocr-scanner!")
    sample_form_path = "data/sample_handwritten_form_01.jpg"
    questions = [
        "What is the full name of the applicant?",
        "How old is this person?",
        "What is the listed address?"
    ]
    
    process_form(sample_form_path, questions)


if __name__ == "__main__":
    main()
