import sqlite3
import bcrypt

from database import get_connection


def hash_password(password):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def register_user(
    name,
    email,
    password,
    phone,
    role,
    address
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users
            (name, email, password, phone, role, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            phone,
            role,
            address
        ))

        connection.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Email already registered."

    finally:

        connection.close()


def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    if verify_password(password, user["password"]):

        return dict(user)

    return None
