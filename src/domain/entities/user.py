from datetime import datetime
from typing import Optional

class User:
    def __init__(self, id: str, username: str, email: str, password_hash: str, is_active: bool = True, created_at: Optional[datetime] = None):
        self.id = id
        self.username = username  # Added missing username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at: Optional[datetime] = None

    def update_email(self, new_email: str):
        if not new_email.strip():
            raise ValueError("Email cannot be empty.")
        
        self.email = new_email
        self.updated_at = datetime.utcnow()

    def update_username(self, new_username: str):
        if not new_username.strip():
            raise ValueError("Username cannot be empty.")
        
        self.username = new_username
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        if not self.is_active:
            raise ValueError("User is already deactivated.")

        self.is_active = False
        self.updated_at = datetime.utcnow()