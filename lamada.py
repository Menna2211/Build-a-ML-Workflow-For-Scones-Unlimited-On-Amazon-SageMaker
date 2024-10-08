""" 
The Lambda function 1 : serializeImageData
"""

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"] ## TODO: fill in
    bucket = event["s3_bucket"]  ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "s3_bucket": bucket,
            "s3_key": key,
            "image_data": image_data,
            "inferences": []
        }
    }


"""
Lambda Function 2: imageClassification

"""


import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2024-08-10-14-56-33-695' ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(ENDPOINT) ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    inferences = predictor.predict(image).decode('utf-8') ## TODO: fill in
    
    # We return the data back to the Step Function    
    event["body"]["inferences"] = json.loads(inferences)
    return {
        'statusCode': 200,
        'body': event["body"]
    }



"""
Lambda Function 3: filter-low-confidence-inferences
"""

import json

THRESHOLD = .9


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event["body"]["inferences"]  ## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold =(max(inferences) > THRESHOLD) ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise(Exception("THRESHOLD_CONFIDENCE_NOT_MET"))

    return {
        'statusCode': 200,
        'body': event["body"]
    }