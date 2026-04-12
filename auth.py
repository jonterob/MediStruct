import hashlib
from dataclasses import dataclass

USER_ROLES = [
    'Admin',
    'Doctor',
    'Nurse',
    'Receptionist',
    'Billing'
]

ROLE_PERMISSIONS = {
    'Admin': {
        'manage_users',
        'view_everything',
        'edit_settings',
        'backup_database',
        'manage_patients',
        'manage_appointments',
        'manage_treatments',
        'manage_billing'
    },
    'Doctor': {
        'manage_treatments',
        'view_patients',
        'view_appointments'
    },
    'Nurse': {
        'view_patients',
        'view_appointments',
        'update_triage'
    },
    'Receptionist': {
        'manage_patients',
        'manage_appointments',
        'view_billing'
    },
    'Billing': {
        'manage_billing',
        'view_patients'
    }
}

@dataclass
class UserAccount:
    username: str
    password_hash: str
    role: str
    display_name: str
    active: bool = True
    created_at: str = ''


def hash_password(password: str) -> str:
    hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def get_role_permissions(role: str):
    return ROLE_PERMISSIONS.get(role, set())
