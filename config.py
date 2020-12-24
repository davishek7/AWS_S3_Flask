import os

SECRET_KEY=os.environ.get("SECRET_KEY")

S3_BUCKET=os.environ.get("AWS_STORAGE_BUCKET_NAME")

S3_KEY=os.environ.get("AWS_ACCESS_KEY_ID")

S3_SECRET=os.environ.get("AWS_SECRET_ACCESS_KEY")