# ocr_processing.py
import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

def perform_handwriting_ocr(image_path: str):
    """Call Azure's Read API to extract handwritten text from the given image."""

    # Azure OCR credentials and endpoint (from environment or config)
    OCR_ENDPOINT = os.environ["DOCAI_ENDPOINT"]
    OCR_KEY = os.environ["DOCAI_ENDPOINT_KEY"]

    # Initialize Azure Computer Vision client
    cv_client = ComputerVisionClient(OCR_ENDPOINT, CognitiveServicesCredentials(OCR_KEY))
    
    # Open image in binary mode
    with open(image_path, 'rb') as image_stream:
        # Async SDK call to read text (handwritten content will be recognized too)
        read_op = cv_client.read_in_stream(image_stream, language='en', raw=True)
        # Get operation ID so we can check results
        #operation_id = read_op.operation_id
        read_operation_location = read_op.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        # Poll for the result
        while True:
            result = cv_client.get_read_result(operation_id)
            if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                break
            time.sleep(1)  # wait a moment before polling again

        # Check if OCR was successful
        if result.status == OperationStatusCodes.succeeded:
            # Aggregate all text lines from the results
            text_lines = []
            for page in result.analyze_result.read_results:
                for line in page.lines:
                    text_lines.append(line.text)
            full_text = "\n".join(text_lines)
            return full_text, result.analyze_result.read_results  # return text and raw results (with coords)
        else:
            raise Exception(f"OCR failed: {result.status}")
