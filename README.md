# FSS
## Folder Synchronization Script Documentation

### Overview

The Folder Synchronization Script is a Python program designed to synchronize the contents of two folders: a source folder and a replica folder. The script ensures that the replica folder maintains an identical copy of the source folder. This synchronization process is one-way, where changes in the source folder are replicated to the replica folder.
### Features

  ***Content Synchronization*** : The script copies files from the source folder to the replica folder, ensuring that the replica folder's content matches the source folder.

  ***Periodic Synchronization***: Synchronization can be scheduled to occur at regular intervals, allowing for automated and continuous synchronization.

  ***Logging***: File creation, copying, and deletion operations are logged to both a file and the console, providing visibility into the synchronization process.

  ***Command-Line Interface (CLI)***: Users can provide folder paths, synchronization intervals, and log file paths via command-line arguments, making it easy to configure and execute the script.

  ***Hash-Based Comparison***: File content is compared using hash values (MD5 by default, but customizable) to detect changes accurately.

### Usage
Command-Line Arguments

The script accepts the following command-line arguments:

  - ***source***: The path to the source folder.
  - ***replica***: The path to the replica folder.
  - ***log***: The path to the log file where synchronization activities are recorded.
  - ***interval***: The synchronization interval in minutes.

Example usage:

    python sync_folders.py /path/to/source /path/to/replica sync_log.txt 60

### Folder Synchronization

The script operates as follows:

  - Files in the source folder that do not exist in the replica folder are copied to the replica folder.

  - Files in the replica folder that do not exist in the source folder are deleted from the replica folder.

  - Files with the same name but different content are updated in the replica folder.

  - File content comparisons are performed using the specified hash algorithm (default is MD5).

### Logging

Synchronization activities, including file creation, copying, and deletion, are logged to the specified log file and displayed on the console.
### Error Handling

The script includes error handling to handle exceptions gracefully. Any errors encountered during file copying or removal are logged, providing detailed error messages for troubleshooting.
### Compatibility

This script is designed for compatibility with Python 3 and should work on various platforms, including Windows, macOS, and Linux. It is tested and verified on Python 3.7 and later.
### Dependencies

The script uses standard Python libraries and does not rely on third-party libraries for folder synchronization. The hashlib library is used for hash-based file content comparison.
### Security

Security considerations include validating and sanitizing folder paths to prevent potential security risks, especially when running the script with elevated privileges.
### Performance

The script efficiently synchronizes folders by comparing files based on their content hashes, minimizing unnecessary file copying. However, performance may vary depending on the number and size of files.
### Future Enhancements

Potential enhancements for future versions of the script may include improved error reporting, support for additional hash algorithms, and optimization for large-scale synchronization tasks.
### Conclusion

The Folder Synchronization Script offers a reliable and customizable solution for maintaining synchronized folders. It is designed for ease of use, flexibility, and accuracy in detecting and replicating changes between folders.
