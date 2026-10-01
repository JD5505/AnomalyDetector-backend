from pwdlib import PasswordHash
import secrets
import hashlib

password_hash = PasswordHash.recommended()

def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def hash_otp(otp) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def otp_verify(otp, hashed_otp) -> bool:
    return hash_otp(otp) == hashed_otp

def hash_password(password: str) -> str:
    return password_hash.hash(password)    

def password_verify(password, hashed_password) -> bool:
    return password_hash.verify(
        password,
        hashed_password
    )


