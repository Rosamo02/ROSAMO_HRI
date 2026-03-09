# login_manager.py

class LoginManager:
    def __init__(self):
        # Faulty logic, change to some sort of config or db
        self.valid_username = "admin"
        self.valid_password = "1234"

    def validate(self, username: str, password: str) -> bool:
        """Return True if credentials are correct."""
        return username == self.valid_username and password == self.valid_password
