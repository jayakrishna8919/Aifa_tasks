from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    
   
    if isinstance(password, bytes):
     
        try:
            password = password.decode("utf-8")
        except Exception:
          
            password = password.decode("latin1")
   
    if len(password.encode("utf-8")) > 10000:
        raise ValueError("password too large")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(plain_password, bytes):
        try:
            plain_password = plain_password.decode("utf-8")
        except Exception:
            plain_password = plain_password.decode("latin1")
    return pwd_context.verify(plain_password, hashed_password)
