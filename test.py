import numpy as np

# Example byte string representing a 2x2 RGB image
file_content = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F' \
                b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F' \
                b'\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F' \
                b'\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F'

# Convert the byte string to a NumPy array
nparr = np.frombuffer(file_content, dtype=np.uint8)

# Print the original shape
print("Original shape:", nparr.shape)

# Ensure that the length of nparr is divisible by 3
if nparr.size % 3 != 0:
    raise ValueError("Array size must be a multiple of 3 for reshaping into (1, -1, 3)")

# Reshape the array to have shape (1, -1, 3)
reshaped_nparr = nparr.reshape((1, -1, 3))

# Print the reshaped shape
print("Reshaped shape:", reshaped_nparr.shape)
