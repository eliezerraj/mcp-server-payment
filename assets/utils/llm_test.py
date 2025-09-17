
import boto3
import json

from dotenv import load_dotenv

load_dotenv("../../.env")

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id_general = "amazon.nova-pro-v1:0"       # General

# vector procedure
message = {
    "messages": [
        {"role": "user", "content": [{"text": "hi, my name is Eliezer"}]}
    ],
    "inferenceConfig": {
        "maxTokens": 200,
        "temperature": 0.7,
        "topP": 0.9
    }
}

# invoke vector
try:
    response = client.invoke_model(
        body=json.dumps(message),
        modelId=model_id_general,
        contentType='application/json',
        accept='application/json'
    )

    # Parse the response and extract the embedding
    response_body = json.loads(response['body'].read())
    output_text = response_body["output"]["message"]["content"][0]["text"]
    print(f"Nova response: {output_text}")
    
except Exception as e:
    print(f"Error invoking the model: {e}")
