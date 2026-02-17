from cryptography.fernet import Fernet


class TelegramSecretCipher:
    def __init__(self, key: str) -> None:
        self._fernet = Fernet(key.encode())

    def encrypt_chat_id(self, chat_id: str) -> str:
        return self._fernet.encrypt(chat_id.encode()).decode()

    def decrypt_chat_id(self, payload: str) -> str:
        return self._fernet.decrypt(payload.encode()).decode()
