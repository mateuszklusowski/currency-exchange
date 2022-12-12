import os
import json
import boto3
from botocore.errorfactory import ClientError


class Bucket:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
        )
        self.bucket_name = os.environ.get("AWS_BUCKET")

    def add_file(self, dictionary):
        """Add file to the s3 bucket"""
        file_name = "{0},{1}-{2}.json".format(
            dictionary["exchange_rate_date"],
            dictionary["from_currency"],
            dictionary["to_currency"],
        )
        try:
            # Overwriting an existing file
            self.s3.head_object(Bucket=self.bucket_name, Key=file_name)
            self.s3.download_file(
                self.bucket_name,
                file_name,
                os.path.join(f"files/{file_name}"),
            )
            with open(f"files/{file_name}", "r+") as file:
                data = json.load(file)
                data.append(dictionary)
                file.seek(0)
                file.write(json.dumps(data, indent=4))
            self.s3.upload_file(
                os.path.join(f"files/{file_name}"),
                self.bucket_name,
                file_name,
            )
            os.remove(os.path.join(f"files/{file_name}"))
        except ClientError:
            # Create a new file
            with open(f"files/{file_name}", "w") as file:
                data = []
                data.append((dictionary))
                file.write(json.dumps(data, indent=4))
            self.s3.upload_file(
                os.path.join(f"files/{file_name}"),
                self.bucket_name,
                file_name,
            )
            os.remove(os.path.join(f"files/{file_name}"))
