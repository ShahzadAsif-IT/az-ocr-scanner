from openai import AzureOpenAI
from env_vars import get_env
import json

def extract_fields_with_gpt(full_text: str):
    """Use GPT-4 to extract and label form fields from the text."""
    system_msg = {"role": "system", "content": "You are an expert data entry assistant. Extract key fields from the form text."}
    user_msg = {"role": "user", "content": f"""The following is text extracted from a form.
                Identify and label the following fields if present: Name, Date of Birth, Address.
                Provide the output in JSON format with keys name, dob, address.
                Form Text: \"\"\"{full_text}\"\"\""""}
    
    version, endpoint, api_key, model = get_env()

    client = AzureOpenAI(
        api_version=version,
        azure_endpoint=endpoint,
        api_key = api_key
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[system_msg, user_msg],
        temperature=0
    )

    answer = response.choices[0].message.content
    # We expect 'answer' to be a JSON string like {"name": "...", "dob": "...", "address": "..."}
    try:
        extracted = json.loads(answer)
    except:
        # If GPT output isn't valid JSON, we could do some string parsing or re-prompt.
        extracted = {}
    return extracted

# gpt_enhancement.py (continued)
def validate_and_correct_fields(fields: dict):
    """Use GPT-4 to validate and correct field values (e.g., dates, names)."""

    version, endpoint, api_key, model = get_env()

    client = AzureOpenAI(
        api_version = version,
        azure_endpoint = endpoint,
        api_key = api_key
    )

    # Construct a prompt describing the fields and asking for corrections
    field_descriptions = "\n".join(f"{k}: {v}" for k,v in fields.items())
    user_prompt = f"""You are a data validation assistant.
                    The following are extracted form fields with values:
                    {field_descriptions}

                    Identify if any values are likely incorrect or ill-formatted, and provide corrected values in JSON.
                    If a value is valid, return it unchanged. If a value is missing or uncertain, you may infer a likely value or mark it null."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content": user_prompt}],
        temperature=0
    )
    try:
        corrections = json.loads(response.choices[0].message.content)
    except:
        corrections = {}

    # Merge corrections back
    for field, new_val in corrections.items():
        if new_val and new_val.lower() != "null":
            fields[field] = new_val
    return fields
