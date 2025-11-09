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
