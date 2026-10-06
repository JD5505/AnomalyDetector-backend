from auth.security import password_verify, generate_otp, hash_otp, otp_verify, hash_password
from auth.email_message import send_otp_email 
from datetime import datetime, timedelta, timezone

def check_password(email, password, cursor):
    cursor.execute(
        """ SELECT * FROM users
            WHERE email = %s
            """,
            (email,)
    )

    data = cursor.fetchone()

    if password_verify(password, data['password_hash']) == True:
        return True
    else:
        return False

def send_email(email, cursor):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    otp = generate_otp()
    send_otp_email(email, otp)
    otp_hash = hash_otp(otp)
    cursor.execute(
            """
            DELETE FROM temp_user
            WHERE valid_upto <= NOW()
            """
            )
    cursor.connection.commit()

    cursor.execute(
        """
        INSERT INTO temp_user
        (temp_email, otp_hash, valid_upto)
        VALUES (%s, %s, %s)
        """,
        (email, otp_hash, expires_at)
    )


def check_otp(email, otp, cursor):

    cursor.execute(
        """
        SELECT otp_hash FROM temp_user
        WHERE temp_email = %s
        """,
        (email,)
    )

    data = cursor.fetchone()
    return otp_verify(otp, data['otp_hash'])

def enter_data(email, password, cursor):
    try:
        password_hash = hash_password(password)
        cursor.execute(
            """
        UPDATE users
        SET password_hash = %s
        WHERE email = %s
            """,
            (password_hash, email)
        )
        cursor.connection.commit()
        return True
    except Exception:
        return False
