import os
import shutil
import argparse
import time
import logging
import hashlib

def setup_logging(log_file):
    """
    Set up logging to write log messages both to a file and the console.

    Args:
        log_file (str): The path to the log file.
    """
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    root_logger = logging.getLogger('')
    root_logger.addHandler(console_handler)

def calculate_hash(file_path, hash_algorithm='md5'):
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path (str): The path to the file.
        hash_algorithm (str): The hash algorithm to use (e.g., 'md5', 'sha256').

    Returns:
        str: The hash value.
    """
    hasher = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def are_files_different(source_file, replica_file, hash_algorithm='md5'):
    """
    Check if two files are different based on their content hash.

    Args:
        source_file (str): The path to the source file.
        replica_file (str): The path to the replica file.
        hash_algorithm (str): The hash algorithm to use (e.g., 'md5', 'sha256').

    Returns:
        bool: True if the files are different, False otherwise.
    """
    source_hash = calculate_hash(source_file, hash_algorithm)
    replica_hash = calculate_hash(replica_file, hash_algorithm)
    return source_hash != replica_hash

def copy_files(source_folder, replica_folder, hash_algorithm='md5'):
    """
    Copy files from the source folder to the replica folder.

    Args:
        source_folder (str): The path to the source folder.
        replica_folder (str): The path to the replica folder.
        hash_algorithm (str): The hash algorithm to use for file comparison (default is 'md5').
    """
    try:
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_folder)
                replica_path = os.path.join(replica_folder, relative_path)

                # Ensure the parent directory in the replica folder exists
                os.makedirs(os.path.dirname(replica_path), exist_ok=True)

                # Check if the file already exists in the replica folder and if it's different
                if not os.path.exists(replica_path) or are_files_different(source_path, replica_path, hash_algorithm):
                    # Copy the file from the source to the replica folder
                    shutil.copy2(source_path, replica_path)

                    # Log file copying operation
                    logging.info(f"File copied: {relative_path}")
    except Exception as e:
        print(f"An error occurred while copying files: {str(e)}")
        logging.error(f"An error occurred while copying files: {str(e)}")

def remove_files(replica_folder, source_folder):
    """
    Remove files from the replica folder that do not exist in the source folder.

    Args:
        replica_folder (str): The path to the replica folder.
        source_folder (str): The path to the source folder.
    """
    try:
        for root, _, files in os.walk(replica_folder):
            for file in files:
                replica_path = os.path.join(root, file)
                relative_path = os.path.relpath(replica_path, replica_folder)
                source_path = os.path.join(source_folder, relative_path)

                # If the file does not exist in the source folder, remove it from the replica folder
                if not os.path.exists(source_path):
                    os.remove(replica_path)
                    
                    # Log file deletion operation
                    logging.info(f"File deleted: {relative_path}")
    except Exception as e:
        print(f"An error occurred while removing files: {str(e)}")
        logging.error(f"An error occurred while removing files: {str(e)}")

def synchronize_folders(source_folder, replica_folder):
    """
    Synchronize the content of the replica folder to match the source folder.

    Args:
        source_folder (str): The path to the source folder.
        replica_folder (str): The path to the replica folder.
    """
    try:
        # First, copy files from the source to the replica folder
        copy_files(source_folder, replica_folder)

        # Then, remove files from the replica folder that aren't in the source folder
        remove_files(replica_folder, source_folder)
        
        logging.info("Synchronization completed successfully.")
    except Exception as e:
        print(f"An error occurred during synchronization: {str(e)}")
        logging.error(f"An error occurred during synchronization: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("log", help="Log file path")
    parser.add_argument("interval", type=int, help="Synchronization interval in minutes")

    args = parser.parse_args()

    # Ensure that source and replica folders exist before starting synchronization
    if not os.path.exists(args.source):
        print(f"Source folder '{args.source}' does not exist.")
        return

    if not os.path.exists(args.replica):
        print(f"Replica folder '{args.replica}' does not exist.")
        return

    setup_logging(args.log)

    while True:
        synchronize_folders(args.source, args.replica)
        time.sleep(args.interval * 60)  # Sleep for the specified interval in minutes

if __name__ == "__main__":
    main()
