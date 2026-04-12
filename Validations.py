import re

def validate_bookid(bookid: str) -> bool:
    return bool(re.fullmatch(r'[A-Z]{2}\d{2}', bookid))

def validate_isbn(isbn: str) -> bool:
    digits = isbn.replace('-', '').replace(' ', '')
    if not digits.isdigit() or len(digits) != 13:
        return False
    total = 0
    for i, d in enumerate(digits[:12]):
        weight = 1 if i  %2 == 0 else 3
        total += int(d) * weight
    check = (10 - (total % 10)) % 10
    return check == int(digits[12])

def validate_title(title: str) -> bool:
    title = title.replace(' ', '')
    return bool(re.fullmatch(r'[A-Za-z]{1,20}', title))

def validate_copies(copies: str) -> bool:
    if not copies.isdigit():
        return False
    return 1 <= int(copies) <= 2

def validate_price(price: str) -> bool:
    return bool(re.fullmatch(r'\d+\.\d{2}',price))


def validate_studentid(studentid: str) -> bool:
    return bool(re.fullmatch(r'\d{8}',studentid))

def validate_firstname(firstname: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z]{1,10}',firstname))

def validate_date(date: str) -> bool:
    from datetime import datetime
    try:
        datetime.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        return False