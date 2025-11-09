import json
import sys
from pathlib import Path
import re
 
FILE_PATH = "users.json"
 
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
 
def validate_user(d: dict) -> dict:
    if "id" not in d or "name" not in d or "email" not in d:
        raise ValueError("Brak wymaganych pól")
    
    try:
        uid = int(d["id"])
        
    except Exception as e:
        raise ValueError(f"Nieprawidłowe ID użytkownika: {d.get('id')}") from e
    
    name = str(d["name"]).strip()
    email = str(d["email"]).strip()
    
    if not EMAIL_RE.match(email):
        raise ValueError(f"Nieprawidłowy adres email: {email}")
    
    
    age_val = d.get("age")
    
    if age_val is not None:
        try:
            age = int(age_val)
            if age < 0:
                raise ValueError("Wiek nie może być ujemny")
        except Exception as e:
            raise ValueError(f"Nieprawidłowy wiek: {age_val}") from e
        
    return {"id": uid, "name": name, "email": email, "age": age_val}
 
def load_users(file_path: str) -> list[dict]:    
    
    path = Path(file_path)
    
    if not path.exists():
        print(f"Plik {file_path} nie istnieje.", file=sys.stderr)
        return []
    
    with path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Błąd dekodowania JSON: {e}", file=sys.stderr)
            return []
 
    if not isinstance(data, list):
        print("Dane w pliku powinny być listą użytkowników.", file=sys.stderr)
        return []
    
    users: list[dict] = []

    for item in data:
        try:
            user = validate_user(item)
            users.append(user)
        except ValueError as e:
            print(f"Błąd walidacji użytkownika: {e}", file=sys.stderr)
    
        return users


def display_users_table(users: list[dict]) -> None:
    if not users:
        print("Brak użytkowników do wyświetlenia.")
        return
    
    # Calculate column widths
    id_width = max(len("ID"), max(len(str(u["id"])) for u in users))
    name_width = max(len("Name"), max(len(u["name"]) for u in users))
    email_width = max(len("Email"), max(len(u["email"]) for u in users))
    age_width = max(len("Age"), max(len(str(u["age"]) if u["age"] is not None else "") for u in users))
    
    # Print header
    print(f"{'ID':<{id_width}} | {'Name':<{name_width}} | {'Email':<{email_width}} | {'Age':<{age_width}}")
    
    # Print separator
    print(f"{'-' * id_width}-+-{'-' * name_width}-+-{'-' * email_width}-+-{'-' * age_width}")
    
    # Print user rows
    for user in users:
        age_str = str(user["age"]) if user["age"] is not None else ""
        print(f"{user['id']:<{id_width}} | {user['name']:<{name_width}} | {user['email']:<{email_width}} | {age_str:<{age_width}}")


if __name__ == "__main__":
    users = load_users(FILE_PATH)
    display_users_table(users)
