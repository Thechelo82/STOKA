"""
Seguridad de STOKA: hash de contraseñas con salt.

# === AQUÍ SE USA: hashlib + salt ===
# hashlib.pbkdf2_hmac deriva una clave a partir de la contraseña.
# El SALT (bytes aleatorios) evita que dos usuarios con la misma
# contraseña tengan el mismo hash y dificulta ataques de diccionario.
"""
from __future__ import annotations

import hashlib
import os
from typing import Tuple


def hash_password(password: str) -> Tuple[str, str]:
    """Devuelve (hash_hex, salt_hex)."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return dk.hex(), salt.hex()


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    salt_b = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_b, 100_000)
    return dk.hex() == password_hash
