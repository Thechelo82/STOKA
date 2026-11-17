"""
Autenticación de STOKA.

# === AQUÍ SE USA: login seguro ===
# 1) Se busca el usuario en SQLite.
# 2) Se verifica el hash PBKDF2 + salt (utils.security).
# 3) Cuentas inactivas no pueden entrar.
# 4) La sesión en memoria NO guarda la contraseña.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from database import db
from utils.security import verify_password


@dataclass
class Session:
    user_id: int
    username: str
    full_name: str
    role: str  # admin | stock | vendedor


def authenticate(username: str, password: str) -> Optional[Session]:
    user = db.get_user_by_username(username.strip())
    if user is None:
        return None
    if not user["active"]:
        return None
    if not verify_password(password, user["password_hash"], user["salt"]):
        return None
    return Session(
        user_id=int(user["id"]),
        username=user["username"],
        full_name=user["full_name"],
        role=user["role"],
    )


def role_label(role: str) -> str:
    return {
        "admin": "Administrador",
        "stock": "Encargado de Stock",
        "vendedor": "Vendedor",
    }.get(role, role)
