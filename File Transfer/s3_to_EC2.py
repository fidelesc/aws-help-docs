"""
This script downloads all files with a given prefix from an S3 bucket and saves them to a local directory on an EC2 instance. It then calls a second script to process all of the downloaded files. The script takes the following command-line arguments:

-bucket: The name of the S3 bucket to download files from. This argument is required.
-prefix: The prefix of the S3 object keys for the files to download. Only files with keys that start with this prefix will be downloaded. This argument is required.
-path: The local path where the downloaded files will be saved. This argument is required.
-max_workers: The maximum number of threads to use for downloading the files. This argument is required.
The script uses the boto3 library to interact with the S3 bucket, and the concurrent.futures.ThreadPoolExecutor class to download the files in parallel using multiple threads. It also uses the subprocess module to call a second script to process the downloaded files.

The download_file function is used to download a single file from S3 and call the second script to process it. It takes two arguments:

obj: An S3 object representing the file to be downloaded.
index: An integer index used to create a unique filename for the downloaded file.
The function splits the S3 object key into a filename and extension, creates a new filename with the format "file_{index}{extension}", and downloads the file from S3 to the local directory. It then calls the second script to process the downloaded file.

The main code block of the script uses the argparse library to parse the command-line arguments. It then creates an S3 resource and a Bucket object for the specified bucket, creates the destination directory if it doesn't already exist, and downloads all files with the specified prefix from the bucket using a ThreadPoolExecutor. It also calls the second script to process all downloaded files together.
"""


import boto3
import os
from concurrent.futures import ThreadPoolExecutor
import argparse



def download_file(obj, index):
    """
    Downloads a single file from S3 and calls the second script to process it.

    Args:
        obj: An S3 Object representing the file to be downloaded.
        index: An integer index used to create a unique filename for the downloaded file.
    """
    # Split the S3 object key into a filename and extension
    filename, extension = os.path.splitext(obj.key)

    # Create a new filename with the format "file_{index}{extension}"
    new_filename = f"file_{index}{extension}"

    # Construct the full path to the new file on the EC2 instance
    new_path = os.path.join(local_path, new_filename)

    # Download the file from S3 to the new path on the EC2 instance
    print(f"Downloading {obj.key} to {new_filename}")
    bucket.download_file(obj.key, new_path)



if __name__ == '__main__':
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description ='Copy files from S3 to EC2') 
    parser.add_argument('-bucket', action = 'store', dest = 'bucket', required = True, help = 'bucket name')
    parser.add_argument('-prefix', action = 'store', dest = 'prefix', required = True, help = 'File prefix inside bucket')
    parser.add_argument('-path', action = 'store', dest = 'path', required = True, help = 'local path to save files')
    parser.add_argument('-max_workers', action = 'store', dest = 'max_workers', required = True, help = 'maximum number of threads to copy')
    args = parser.parse_args()
    
    # Create an S3 resource and a Bucket object for the specified bucket
    s3 = boto3.resource('s3')
    bucket_name = args.bucket
    prefix = args.prefix
    local_path = args.path
    max_workers = int(args.max_workers)
    
    # Create the destination folder if it doesn't already exist
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # Create a Bucket object for the specified bucket
    bucket = s3.Bucket(bucket_name)

    # Download all files with the specified prefix from the bucket
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for index, obj in enumerate(bucket.objects.filter(Prefix=prefix)):
            # Submit a download_file task to the ThreadPoolExecutor for each S3 object
            executor.submit(download_file, obj, index)

