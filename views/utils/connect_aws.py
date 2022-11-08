from ..utils.env_var import aws_access_key, aws_secret_key
import boto3

def s3_connection():
	s3 = boto3.client('s3',aws_access_key_id = aws_access_key,aws_secret_access_key = aws_secret_key)
	
	return s3