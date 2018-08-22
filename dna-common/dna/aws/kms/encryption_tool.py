from base64 import b64encode, b64decode
import boto3 as boto3


def encrpyt_text(to_encrypt: str):
    kms = boto3.client('kms')
    key_id = 'alias/reporting'
    print(to_encrypt)
    stuff = kms.encrypt(KeyId=key_id, Plaintext=to_encrypt)
    binary_encrypted = stuff[u'CiphertextBlob']
    encrypted_password = b64encode(binary_encrypted)
    print(encrypted_password.decode())
    decode = b64decode(encrypted_password)
    decrypted = kms.decrypt(CiphertextBlob=decode)['Plaintext'].decode("utf-8")
    print(decrypted)


if __name__ == '__main__':
    encrpyt_text('xxx')
