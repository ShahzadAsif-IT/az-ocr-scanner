import os

def get_env():
    openai_endpoint = os.environ["OPENAI_ENDPOINT"]
    openai_api_key = os.environ["OPENAI_ENDPOINT_KEY"]
    openai_version = os.environ["OPENAI_API_VERSION"]
    openai_model = os.environ["OPENAI_MODEL"]
    return openai_version, openai_endpoint, openai_api_key, openai_model