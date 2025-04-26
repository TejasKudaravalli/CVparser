import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_references(references_str: str):
    references_list = []
    possible_references = re.split(r"\n\s*\n|[-]{3,}", references_str)
    possible_references.append("")
    print(possible_references)

    for ref in possible_references:
        ref = ref.strip()
        doc = nlp(ref)
        if not ref:
            continue

        # Extract email
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", ref)
        email = email_match.group(0) if email_match else ""
        ref = ref.replace(email, "")

        # Extract phone number
        phone_pattern = re.compile(
            r"""
            (?:(?:\+?1\s*(?:[.-]\s*)?)?           
            (?:\(\s*\d{3}\s*\)|\d{3})\s*           
            (?:[.-]?\s*)?\d{3}\s*                 
            (?:[.-]?\s*)?\d{4})                    
            """,
            re.VERBOSE,
        )
        match = phone_pattern.search(ref)
        if match:
            phone_number = match.group()
        else:
            phone_number = ""
        ref = ref.replace(phone_number, "")

        # Extract full name (assuming the first line or something before email/phone)
        full_name = ""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                full_name = ent.text
                break
        if len(full_name) > 1:
            ref = ref.replace(full_name, "")

        # Extract Company
        company = ""
        for ent in doc.ents:
            if ent.label_ == "ORG":
                company = ent.text
                break
        if len(company) > 1:
            ref = ref.replace(company, "")

        name_lines = ref.splitlines()
        # Extract company and position - naive approach
        position = ""
        description = ""

        # Try to find company and position information
        for line in name_lines[1:]:
            line = line.strip()
            if " at " in line:
                parts = line.split(" at ")
                position = parts[0].strip()
            elif " - " in line:
                parts = line.split(" - ")
                if len(parts) == 2:
                    position = parts[0].strip()
            else:
                description += line + " "

        references_list.append(
            {
                "full_name": full_name,
                "phone_number": phone_number,
                "email": email,
                "company": company,
                "position": position,
                "description": description.strip(),
            }
        )

    return references_list
