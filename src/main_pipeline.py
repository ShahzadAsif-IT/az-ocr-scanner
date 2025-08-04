from dotenv import load_dotenv, find_dotenv
from src.ocr_processing import perform_handwriting_ocr
from src.field_extraction import get_structured_data
from src.gpt_enhancement import validate_and_correct_fields
from src.query_answering import answer_query_about_form

def process_form(image_path: str, user_questions: list[str] = None):
    load_dotenv(find_dotenv())

    # Step 1: OCR to get text
    full_text, ocr_details = perform_handwriting_ocr(image_path)
    print("OCR Text:\n", full_text)
    print("OCR Details:\n", ocr_details)

    # Step 2: Extract structured fields
    fields = get_structured_data(full_text)
    print("Extracted fields (pre-validation):", fields)

    # Step 3: GPT-4 enhancement for ambiguous fields
    fields = validate_and_correct_fields(fields)
    print("Fields after GPT validation:", fields)

    # Step 4: Handle user queries if any
    if user_questions:
        for q in user_questions:
            answer = answer_query_about_form(fields, q)
            print(f"Q: {q}\nA: {answer}\n")

    return fields

# Example usage:
if __name__ == "__main__":
    sample_form_path = "data/sample_handwritten_form_01.jpg"
    questions = [
        "What is the full name of the applicant?",
        "How old is this person?",
        "What is the listed address?"
    ]
    process_form(sample_form_path, questions)
