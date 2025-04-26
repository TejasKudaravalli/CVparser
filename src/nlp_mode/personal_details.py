import re 
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_phone_number(cv_string: str) -> str:
    phone_pattern = re.compile(
        r"""
        (?:(?:\+?1\s*(?:[.-]\s*)?)?            # optional country code
        (?:\(\s*\d{3}\s*\)|\d{3})\s*           # area code
        (?:[.-]?\s*)?\d{3}\s*                  # first 3 digits
        (?:[.-]?\s*)?\d{4})                    # last 4 digits
    """,
        re.VERBOSE,
    )
    match = phone_pattern.search(cv_string)
    if match:
        phone_number = match.group()
    else:
        phone_number = None
    return phone_number

def extract_email(cv_string: str) -> str:
    email_pattern = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )
    match = email_pattern.search(cv_string)
    if match:
        email = match.group()
    else:
        email = None
    return email

def extract_urls(cv_string: str) -> list:
    url_pattern = r'((?:https?://|www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)'
    urls = re.findall(url_pattern, cv_string)
    return urls

def extract_personal_details(cv_string: str) -> dict:
    personal_details = {}
    phone_number = extract_phone_number(cv_string)
    if phone_number:
        cv_string = cv_string.replace(phone_number, ". \n")
    email = extract_email(cv_string)
    if email:
        cv_string = cv_string.replace(email, ". \n")
    url_list = extract_urls(cv_string)
    if len(url_list) > 0:
        for url in url_list:
            cv_string = cv_string.replace(url, ". \n")
    doc = nlp(cv_string)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            location = ent.text
            break
    else:
        location = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            first_name, last_name = name.split(" ", 1)
            break
    else:
        first_name = None
        last_name = None
    personal_details["first_name"] = first_name
    personal_details["last_name"] = last_name
    personal_details["phone_number"] = phone_number
    personal_details["email"] = email
    personal_details["address"] = location
    personal_details["urls"] = url_list
    return personal_details