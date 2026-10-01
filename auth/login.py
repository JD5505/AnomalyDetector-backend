from auth.security import password_verify

def verify_password(email, password, cursor):
    try:
        cursor.execute("""
            SELECT * FROM users 
            WHERE email = %s
            """,
            (email,)
            )
    except:
        return False

    data = cursor.fetchone()
    password_hash = data['password_hash']
    is_verified = password_verify(password, password_hash)
    if is_verified == True:
        return True
    else:
        return False
    
        