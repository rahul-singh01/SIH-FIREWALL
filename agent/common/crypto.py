from cryptography.fernet import Fernet

print("Fernet")
class Crypto:
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.fernet = Fernet(key)

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode())

    def decrypt(self, data):
        return self.fernet.decrypt(data).decode()