"""
The code provided reads and processes image files stored in an Amazon S3 bucket in parallel using the Dask library. Here's a breakdown of the code:
    
The necessary libraries are imported, including dask.bag and dask.distributed for parallel processing, s3fs for accessing S3 data, and numpy and cv2 for image processing.


The process_file function takes an S3 object key as input, opens the object as a file-like object, and reads the image data into a NumPy array using np.frombuffer(). The image data is then decoded using cv2.imdecode() into an OpenCV image. The image can then be processed using any necessary image processing code.

The code uses the argparse module to parse command-line arguments, including the S3 bucket name, prefix, and maximum number of threads. The Dask client and S3 file system are created, and a list of all S3 object keys with the specified prefix is obtained using s3.glob(). The list of keys is then processed in parallel using Dask's db.map() method, with process_file function called for each key. The compute() method is used to compute the results, and the Dask client is closed at the end of execution.

Note that the code currently does not save any processed image files, but this can be added as needed by replacing the commented out line in the process_file function with the desired code.
"""


import dask.bag as db
import dask.distributed as dd
import s3fs
# import os
import argparse

import numpy as np
import cv2


def process_file(key):
    """
    Calls the second script to process a single file from S3.

    Args:
        s3: An instance of s3fs.S3FileSystem.
        key: An S3 object key representing the file to be processed.
    """
    # Open the S3 object as a file-like object
    with s3.open(key, 'rb') as f:
        # Call the second script to process the file
        # Replace with your own processing code
        print(f"Processing {key}")
        img_bytes = np.frombuffer(f.read(), np.uint8)
        # Decode the image data using cv2.imdecode()
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        
        # cv2.imwrite(f"{key.split('/')[-1]}", img)  #Example




if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Copy files from S3 to EC2')
    parser.add_argument('-bucket', action='store', dest='bucket', required=True, help='bucket name')
    parser.add_argument('-prefix', action='store', dest='prefix', required=True, help='File prefix inside bucket')
    parser.add_argument('-max_workers', action='store', dest='max_workers', required=True, help='maximum number of threads')
    args = parser.parse_args()

    # Create a Dask client and S3 file system
    client = dd.Client()
    s3 = s3fs.S3FileSystem()

    # Get a list of all S3 object keys with the specified prefix
    bucket_name = args.bucket
    prefix = args.prefix
    keys = s3.glob(f"s3://{bucket_name}/{prefix}*")

    # Process all files in parallel using Dask
    dask_bag = db.from_sequence(keys, npartitions=4)
    dask_bag_filtered = dask_bag.map(process_file)
    results = dask_bag_filtered.compute()
    
    # Close the Dask client
    client.close()

