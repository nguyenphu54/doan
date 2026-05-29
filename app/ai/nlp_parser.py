import re
from datetime import date

# Regex để bắt số tiền: "45k", "45.000", "1 triệu", "2.5tr"
AMOUNT_PATTERN = r'(\d+(?:[.,]\d+)*)\s*(k|nghìn|triệu|tr|đ|đồng)?'


def _looks_like_thousand_group(raw_amount: str) -> bool:
    return bool(re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", raw_amount))


def _parse_amount(raw_amount: str, unit: str) -> float | None:
    if _looks_like_thousand_group(raw_amount):
        amount_str = re.sub(r"[.,]", "", raw_amount)
    else:
        amount_str = raw_amount.replace(",", ".")

    try:
        amount = float(amount_str)
    except ValueError:
        return None

    if unit in ("k", "nghìn"):
        amount *= 1000
    elif unit in ("triệu", "tr"):
        amount *= 1000000

    return int(amount) if amount.is_integer() else amount

def parse_quick_add(text: str) -> dict | None:
    """
    Input:  "ăn phở 45k"
    Output: {amount:45000, description:"ăn phở", type:"expense", date:today}
    """
    m = re.search(AMOUNT_PATTERN, text, re.IGNORECASE)
    if not m:
        return None
        
    raw_amount, unit = m.group(1), (m.group(2) or "").lower()
    
    amount = _parse_amount(raw_amount, unit)
    if amount is None:
        return None
        
    # Lấy description bằng cách loại bỏ phần tiền
    description = re.sub(AMOUNT_PATTERN, "", text, flags=re.IGNORECASE).strip()
    
    # Nếu description trống, có thể dùng mặc định hoặc gợi ý
    if not description:
        description = "Giao dịch mới"

    return {
        "amount": amount,
        "description": description,
        "type": "expense",  # Mặc định là chi phí
        "date": str(date.today())
    }
