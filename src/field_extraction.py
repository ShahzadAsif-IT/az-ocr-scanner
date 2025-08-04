import re
from src.gpt_enhancement import extract_fields_with_gpt

# Define expected field labels
FIELD_LABELS = {
    "name": ["name", "applicant name", "full name"],
    "dob": ["date of birth", "dob", "birthdate"],
    "address": ["address", "residential address", "mailing address"]
    # add other fields as needed
}

def extract_fields_from_text(full_text: str):
    """Extracts known fields from OCR text using simple keyword matching and regex."""
    fields = {"name": None, "dob": None, "address": None}
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
    for line in lines:
        lower = line.lower()
        # Check each field label keyword in this line
        for field, keywords in FIELD_LABELS.items():
            for kw in keywords:
                if kw in lower:
                    # If we find a label in the line, extract the part after the label
                    # e.g. "Name: Joe Blank" -> "Joe Blank"
                    value = line.split(":")[-1].strip()
                    if value:
                        fields[field] = value
    
    # Normalize DOB format if found in text
    if fields["dob"]:
        # simple regex to find a date pattern in dob field (if OCR combined text differently)
        match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', fields["dob"])
        if match:
            fields["dob"] = match.group(1)
    return fields

def get_structured_data(full_text: str):
    fields = extract_fields_from_text(full_text)
    # If any field is missing or we suspect errors, use GPT to parse
    if None in fields.values() or needs_validation(fields):
        gpt_fields = extract_fields_with_gpt(full_text)
        # Merge GPT results for missing fields or if GPT has higher confidence
        for key, val in gpt_fields.items():
            if val and is_low_confidence(fields.get(key)):
                fields[key] = val
    return fields

def needs_validation(fields: dict) -> bool:
    # Simple check: if any critical field missing, or maybe invalid format
    if fields["dob"] and not re.match(r'\d', fields["dob"]):  # DOB doesn't contain a digit (unlikely if missing)
        return True
    # Here we can add other heuristics as needed (e.g., name looks too short, address missing number, etc.)
    return None in fields.values()

def is_low_confidence(value: str) -> bool:
    # Here, we might use a heuristic, e.g., contains illegible character '?'
    return value is None or "?" in value
