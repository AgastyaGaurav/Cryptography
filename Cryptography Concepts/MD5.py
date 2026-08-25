import hashlib

# 1. Define the text
text = "Hello, World!"

# 2. Encode the string to bytes, then hash it using md5()
md5_hash = hashlib.md5(text.encode('utf-8'))

# 3. Get the hexadecimal representation
hex_digest = md5_hash.hexdigest()

print(f"MD5 Hash: {hex_digest}")
# Output: fc3ff98e8c6a0d3087d515c0473f8677