from werkzeug.security import generate_password_hash

password = "admin123"  # Replace with your desired admin password
hashed_password = generate_password_hash(password)
print(f"Original password: {password}")
print(f"Hashed password: {hashed_password}")
