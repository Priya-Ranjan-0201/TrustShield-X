import re

# Comprehensive static set of common weak/popular passwords to reject
COMMON_PASSWORDS = {
    # Sequential & Repetitive Patterns
    "123456", "123456789", "12345678", "12345", "1234567", "1234", "1234567890", "0123456789",
    "111111", "000000", "123123", "654321", "987654321", "123321", "11111111", "00000000",
    "121212", "12341234", "7777777", "88888888", "9999999", "123456789!", "1234567890!",

    # Keyboard Walks
    "qwerty", "qwertyuiop", "asdfghjkl", "zxcvbnm", "qwertz", "azerty", "qwerty123",
    "qwertyuiop123", "asdfghjk", "zxcvbnm123", "qwer1234", "asdf1234", "zxcv1234",

    # Common System & Default Credentials
    "password", "password123", "password123!", "pass1234", "pass1234!", "password1!",
    "admin", "admin123", "admin1234", "admin1234!", "administrator", "root", "user",
    "default", "system", "service", "guest", "test", "testing", "master", "access",
    "secret", "supersecret", "secret123", "secret123!", "changeme", "letmein", "welcome",
    "welcome1", "welcome123", "welcome2026", "trustshield", "truthshield", "truthshield123",
    "truthshield#1", "truthshield2026",

    # Common Words & Popular Terms
    "football", "baseball", "basketball", "soccer", "monkey", "dragon", "pokemon",
    "superman", "batman", "spiderman", "avengers", "starwars", "matrix", "hacker",
    "shadow", "sunshine", "princess", "angel", "freedom", "charlie", "michael",
    "jordan", "daniel", "thomas", "robert", "jessica", "mustang", "harley", "ferrari",
    "iloveyou", "iloveyou123", "love1234", "forever", "godbless", "trustme"
}


def validate_password_strength(password: str) -> tuple[bool, str | None]:
    """Validate password according to enterprise policy rules:
    - Min 10 characters
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 digit
    - At least 1 special character
    - Not in comprehensive common password list
    """
    if len(password) < 10:
        return False, "Password must be at least 10 characters long."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/]", password):
        return False, "Password must contain at least one special character."

    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common and easily guessable. Please choose a stronger password."

    return True, None
