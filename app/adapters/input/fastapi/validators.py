from datetime import date
from pydantic import EmailStr

def not_empty(value: str, field_name: str = "Campo"):
    if not value or not str(value).strip():
        raise ValueError(f'{field_name} no puede estar vacío')
    return value

def valid_email(value: str):
    # Lanza error si no es email válido
    return EmailStr.validate(value)

def not_in_future(value: date, field_name: str = "Fecha"):
    if value > date.today():
        raise ValueError(f'{field_name} no puede ser futura')
    return value

def end_date_bigger(start_date: date, end_date: date, field_name: str = "Fecha de fin"):
    if end_date and start_date and end_date <= start_date:
        raise ValueError(f'{field_name} debe ser posterior a la fecha de inicio')
    return end_date

def positive_int(value: int, field_name: str = "Campo"):
    if value is None or value <= 0:
        raise ValueError(f'{field_name} debe ser un entero positivo')
    return value

def in_range(value: int, min_value: int, max_value: int, field_name: str = "Campo"):
    if value < min_value or value > max_value:
        raise ValueError(f'{field_name} debe estar entre {min_value} y {max_value}')
    return value

def in_choices(value, choices, field_name: str = "Campo"):
    if value not in choices:
        raise ValueError(f'{field_name} debe ser uno de: {choices}')
    return value