import secrets

# Generate a secure secret key
secret_key = secrets.token_hex(32)
print(f"Generated SECRET_KEY: {secret_key}") 