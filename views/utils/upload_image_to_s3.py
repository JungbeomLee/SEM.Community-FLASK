from .connect_aws import s3_connection
from .env_var import bucket_name

def s3_put_object(s3, file, filename) :
    try :
        s3 = s3_connection()
        s3.delete_object(Bucket=bucket_name, Key=f'images/{filename}.jpg')
        s3.put_object(
            Body = file,
            Bucket = bucket_name,
            Key = f'images/{filename}.jpg',
            ACL = 'public-read-write'
        )
    except Exception as e :
        return False
    return True