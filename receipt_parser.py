import re
import json


def parse_receipt(text):
    result = {
        "prices": [],
        "products": [],
        "total_amount": 0.0,
        "date": None,
        "time": None,
        "payment_method": None
    }

    # 1. Extract prices
    # Matches: 12.99, 1,250.50, 2500, 99,50
    price_pattern = r'\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})\b|\b\d+\b'
    found_prices = re.findall(price_pattern, text)

    prices = []
    for price in found_prices:
        clean_price = price.replace(",", ".")
        try:
            prices.append(float(clean_price))
        except ValueError:
            pass

    result["prices"] = prices

    # 2. 
    total_patterns = [
        r'(?:TOTAL|Total|total|AMOUNT|Amount|amount)\s*[:\-]?\s*(\d+(?:[.,]\d{2})?)',
        r'(?:SUM|Sum|sum)\s*[:\-]?\s*(\d+(?:[.,]\d{2})?)'
    ]

    total_found = None
    for pattern in total_patterns:
        match = re.search(pattern, text)
        if match:
            total_found = match.group(1).replace(",", ".")
            break

    if total_found:
        result["total_amount"] = float(total_found)
    elif prices:
       
        result["total_amount"] = max(prices)

    # 3. 
    date_patterns = [
        r'\b(\d{2}[/-]\d{2}[/-]\d{4})\b',
        r'\b(\d{4}[/-]\d{2}[/-]\d{2})\b',
        r'\b(\d{2}\.\d{2}\.\d{4})\b'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            result["date"] = match.group(1)
            break

    # 4. 
    time_pattern = r'\b(\d{2}:\d{2}(?::\d{2})?)\b'
    time_match = re.search(time_pattern, text)
    if time_match:
        result["time"] = time_match.group(1)

    # 5. 
    payment_patterns = [
        r'\b(CASH|Cash|cash)\b',
        r'\b(CARD|Card|card)\b',
        r'\b(VISA|Visa|visa)\b',
        r'\b(MASTERCARD|MasterCard|mastercard)\b',
        r'\b(BANK TRANSFER|bank transfer)\b',
        r'\b(APPLE PAY|Apple Pay|apple pay)\b',
        r'\b(GOOGLE PAY|Google Pay|google pay)\b'
    ]

    for pattern in payment_patterns:
        match = re.search(pattern, text)
        if match:
            result["payment_method"] = match.group(1)
            break

    # 6. 
    product_patterns = [
        r'^([A-Za-zА-Яа-я0-9\s\-\(\)]+?)\s+\d+(?:[.,]\d{2})\s*$',
        r'^([A-Za-zА-Яа-я0-9\s\-\(\)]+?)\s+\d+\s*x\s*\d+(?:[.,]\d{2})\s*$',
        r'^([A-Za-zА-Яа-я0-9\s\-\(\)]+?)\s*-\s*\d+(?:[.,]\d{2})\s*$'
    ]

    lines = text.splitlines()
    products = []

    ignored_words = {
        "total", "amount", "sum", "cash", "card", "visa",
        "mastercard", "date", "time", "receipt", "change"
    }

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        for pattern in product_patterns:
            match = re.match(pattern, clean_line, re.IGNORECASE)
            if match:
                product_name = match.group(1).strip()
                if product_name.lower() not in ignored_words and len(product_name) > 1:
                    products.append(product_name)
                break

    result["products"] = products

    return result


def main():
    try:
        with open("raw.txt", "r", encoding="utf-8") as file:
            text = file.read()

        parsed_data = parse_receipt(text)

        print("Parsed Receipt Data:")
        print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

    except FileNotFoundError:
        print("Error: raw.txt file not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()