import dask.bag as db
import dask.distributed as dd
import s3fs
import os
import argparse


def process_file(key):
    """
    Calls the second script to process a single file from S3.

    Args:
        key: An S3 object key representing the file to be processed.
    """
    # Get the file extension from the object key
    _, extension = os.path.splitext(key)

    # Call the second script to process the file
    # Replace with your own processing code
    print(f"Processing {key}")


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Copy files from S3 to EC2')
    parser.add_argument('-bucket', action='store', dest='bucket', required=True, help='bucket name')
    parser.add_argument('-prefix', action='store', dest='prefix', required=True, help='File prefix inside bucket')
    parser.add_argument('-max_workers', action='store', dest='max_workers', required=True, help='maximum number of threads to copy')
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
    dask_bag.map(process_file).compute()

    # Close the Dask client
    client.close()

