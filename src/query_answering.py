import os
import math
from datetime import datetime
from openai import AzureOpenAI
from env_vars import get_env

def answer_query_about_form(fields: dict, question: str):
    """Answer a user query about the form using GPT-4, providing the form data as context."""
    # Construct a context paragraph from the fields
    context_lines = []
    if fields.get("name"): 
        context_lines.append(f"Name: {fields['name']}")
    if fields.get("dob"):
        context_lines.append(f"Date of Birth: {fields['dob']}")
        # Optionally, calculate age if needed for answering
        try:
            dob = datetime.strptime(fields['dob'], "%Y-%m-%d")
        except:
            try:
                dob = datetime.strptime(fields['dob'], "%m/%d/%Y")
            except:
                dob = None
        if dob:
            age = math.floor((datetime.now() - dob).days/365.25)
            context_lines.append(f"Age: {age}")
    if fields.get("address"):
        context_lines.append(f"Address: {fields['address']}")
    context_text = "\n".join(context_lines)
    prompt = f"""Use the following information from a form to answer the question.
                Information:
                \"\"\"\n{context_text}\n\"\"\"
                Question: \"{question}\"
                Answer as a helpful assistant, using the information provided."""
    
    version, endpoint, api_key, model = get_env()

    client = AzureOpenAI(
        api_version=version,
        azure_endpoint=endpoint,
        api_key = api_key
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    answer = response.choices[0].message.content
    return answer
