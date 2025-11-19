import re
from pydantic import validator, BaseModel

class UserInput(BaseModel):
    username: str

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_.-]{3,20}$", v):
            raise ValueError("Invalid username: must be 3-20 chars, letters/numbers/._- only")
        return v
