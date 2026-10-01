from datetime import datetime, timedelta, timezone
from auth.security import generate_otp, hash_otp, otp_verify, hash_password, password_verify
from auth.email_message import send_otp_email

class Registrations():

    @staticmethod
    def clear_registrations(cursor):
        cursor.execute(
        """
        DELETE FROM temp_user
        WHERE valid_upto <= NOW()
        """
        )

    @staticmethod
    def register_user(email : str, password : str, role: str,  cursor) -> bool:
        
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
        password_hash = hash_password(password)
        otp = generate_otp()

        send_otp_email(email, otp)

        otp_hash = hash_otp(otp)
        cursor.execute("""
            INSERT INTO temp_user
            (temp_email, otp_hash, valid_upto, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
        """, 
            (email, otp_hash, expires_at, password_hash, role)
        )
        return True

    @staticmethod
    def verify_registration(email, otp, cursor) -> bool:
        cursor.execute("""
        SELECT * FROM temp_user
        WHERE temp_email = %s
        """,
        (email,)
        )
        registration = cursor.fetchone()
        
        if registration is None:
            return False
        else:
            otp_hash = registration['otp_hash']
            password_hash = registration['password_hash']
            role = registration['role']
            if otp_verify(otp, otp_hash) == True:
                try:
                    cursor.execute("""
                        INSERT INTO users
                        (email, password_hash, role)
                        VALUES
                        (%s, %s, %s)
                        """,
                        (email, password_hash, role))
                    return True
                except:
                    return False

    @staticmethod
    def remove_account(email, password, cursor):
        cursor.execute("""
        SELECT password_hash FROM users
        WHERE email = %s
        """, (email,))
        data = cursor.fetchone()
        password_hash = data['password_hash']
        is_verified = password_verify(password, password_hash)
        if is_verified == True:
            cursor.execute("""
            DELETE FROM users WHERE email = %s
            """, (email,))
            cursor.connection.commit()
            return True
        else:
            return False