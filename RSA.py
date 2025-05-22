import argparse
import os


# python RSA.py -file image.png -public "" -private ""


def encrypt_file(file_path, public_key):
    n, e = map(int, public_key.split(':'))
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    byte_length = (n.bit_length() + 7) // 8
    chunk_size = byte_length - 1
    encrypted_data = bytearray()
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        m = int.from_bytes(chunk, 'big')
        c = pow(m, e, n)
        encrypted_data += c.to_bytes(byte_length, 'big')
    
    # Overwrite original file
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"File encrypted: {file_path}.rsa256")

    os.rename(file_path, file_path + ".rsa256")

def decrypt_file(file_path, private_key):
    n, d = map(int, private_key.split(':'))
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    byte_length = (n.bit_length() + 7) // 8
    chunk_size = byte_length
    decrypted_data = bytearray()
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        c = int.from_bytes(chunk, 'big')
        m = pow(c, d, n)
        decrypted_data += m.to_bytes(byte_length - 1, 'big')
    
    # Overwrite encrypted file
    with open(file_path, 'wb') as f:
        f.write(decrypted_data)
    print(f"File decrypted: {file_path}")

    os.rename(file_path, file_path.replace(".rsa256", ""))

def main():
    parser = argparse.ArgumentParser(description="Encrypt/Decrypt files using RSA.")
    parser.add_argument("-file", required=True, help="File to process")
    parser.add_argument("-private", help="Private key (n:d)")
    parser.add_argument("-public", help="Public key (n:e)")
    args = parser.parse_args()

    if args.file.endswith('.rsa256'):
        if not args.private:
            print("Error: Private key required for decryption.")
            return
        decrypt_file(args.file, args.private)
    else:
        if not args.public:
            print("Error: Public key required for encryption.")
            return
        encrypt_file(args.file, args.public)

if __name__ == "__main__":
    main()
