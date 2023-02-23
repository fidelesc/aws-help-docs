"""
This script uploads files from a local folder on an EC2 instance to an S3 bucket. The script takes the following command-line arguments:

-bucket: The name of the S3 bucket to upload files to. This argument is required.
-prefix: The prefix to use for the S3 object keys for the uploaded files. This argument is required.
-path: The local path to the folder containing the files to upload. This argument is required.
-max_workers: The maximum number of threads to use for uploading the files. This argument is required.

The script uses the boto3 library to interact with the S3 bucket and create a client object for the S3 service. It also uses the concurrent.futures.ThreadPoolExecutor class to upload the files in parallel using multiple threads.

The upload_file function is used to upload a single file to S3. It takes two arguments:

local_file_path: The path to the file on the EC2 instance.
s3_key: The key to use for the S3 object.

The function uploads the file to S3 using the S3 client object.

The main code block of the script uses the argparse library to parse the command-line arguments. It then creates an S3 client object and sets the name of the S3 bucket to upload to, the local path of the folder containing the files to upload, the S3 prefix for uploaded files, and the maximum number of threads to use for uploading the files. It also uses a ThreadPoolExecutor to upload the files in parallel and waits for all uploads to complete.

Using threads allows the script to upload multiple files at the same time, which can improve performance when uploading a large number of files or large files.
"""

import boto3
import os
from concurrent.futures import ThreadPoolExecutor
import argparse


# Define a function to upload a single file to the S3 bucket
def upload_file(s3, bucket_name, local_file_path, s3_key):
    """
    Uploads a single file to the S3 bucket.

    Args:
        s3: The S3 client object.
        bucket_name: The name of the S3 bucket to upload the file to.
        local_file_path: The local path of the file to upload.
        s3_key: The key to use for the S3 object of the uploaded file.
    """
    try:
        # Upload the file to S3
        # s3.Bucket(bucket_name).upload_file(local_path, s3_key)
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"Uploaded: {local_file_path}")
        return True
    except:
        print(f"Failed upload: {local_file_path}")
        return False
    



if __name__ == '__main__':
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description ='Copy files from EC2 to S3') 
    parser.add_argument('-bucket', action = 'store', dest = 'bucket', required = True, help = 'bucket name')
    parser.add_argument('-prefix', action = 'store', dest = 'prefix', required = True, help = 'S3 prefix for uploaded files')
    parser.add_argument('-path', action = 'store', dest = 'path', required = True, help = 'local path to files for upload')
    parser.add_argument('-max_workers', action = 'store', dest = 'max_workers', required = True, help = 'maximum number of threads to copy files')
    args = parser.parse_args()
    
   
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Set the name of the S3 bucket you want to upload to
    bucket_name = args.bucket

    # Set the local path of the folder containing the files to upload
    local_path = args.path

    # Set the maximum number of threads to use for uploading files
    max_workers = int(args.max_workers)
    
    # Set S3 prefix for uploaded files
    prefix = args.prefix
    
    # Use a ThreadPoolExecutor to upload the files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for path, subdirs, file_list in os.walk(local_path):
            for filename in file_list:
                local_file_path = os.path.join(path, filename)
                s3_key = os.path.join(prefix, filename)
                # Skip over any directories
                if os.path.isfile(local_file_path):
                    futures.append(executor.submit(upload_file, s3, bucket_name, local_file_path, s3_key))

        # Wait for all uploads to complete
        for future in futures:
            future.result()
