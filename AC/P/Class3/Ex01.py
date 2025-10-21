import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def newSection():
    print("\n" + "="*50 + "\n")


# Read plain text from file
with open("plainText.txt", "r") as f:
    pText = f.read()

newSection()
print("ORIGINAL TEXT:\n")
print(pText)

# Create Cipher parameters
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

# Pad plain text to AES block size (128 bits / 16 bytes)
padder = padding.PKCS7(algorithms.AES.block_size).padder()  # block_size is in bits
padded_data = padder.update(pText.encode()) + padder.finalize()

# Encrypt padded plain text
encryptor = cipher.encryptor()
cText = encryptor.update(padded_data) + encryptor.finalize()
newSection()
print("ENCRYPTED TEXT (bytes):\n")
print(cText)
newSection()
print("ENCRYPTED TEXT (readable as base64 encoded):\n")
print(base64.b64encode(cText).decode())

# Decrypt encrypted text
decryptor = cipher.decryptor()
dPadded = decryptor.update(cText) + decryptor.finalize()

# Unpad decrypted data and decode to string
unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
dText_bytes = unpadder.update(dPadded) + unpadder.finalize()
dText = dText_bytes.decode()

newSection()
print("DECRYPTED TEXT:\n")
print(dText)

# Check if the decryption was successeful
newSection()
if dText == pText:
    print("The Encryption and Decryption was successeful!")
else:
    print("There was an error on the Encryption or Decryption...")
newSection()