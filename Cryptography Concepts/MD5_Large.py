import hashlib

def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read the file in 4KB chunks
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Example usage:
# print(get_file_md5("path/to/your/file.zip"))