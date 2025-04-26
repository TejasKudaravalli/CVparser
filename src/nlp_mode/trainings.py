import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_trainings_certifications(trainings_str, cv_string):
    training_details = []
    date_pattern = r"(?:(?:19|20)\d{2}|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{4})"
    if len(trainings_str) > 5:
        training_list = trainings_str.split("\n")
    else:
        cert_keywords = [
            "certified",
            "certification",
            "certificate",
            "training",
            "course",
            "workshop",
            "bootcamp",
            "seminar",
            "accreditation",
        ]

        training_list = []

        for line in cv_string.split("\n"):
            if any(keyword in line.lower() for keyword in cert_keywords):
                training_list.append(line.strip())

    for line in training_list:
        match = re.search(date_pattern, line, re.IGNORECASE)
        date = None
        if match:
            date = match.group()
        doc = nlp(line)
        organization = None
        for ent in doc.ents:
            if ent.label_ == "ORG":
                organization = ent.text

        training_details.append(
            {"date": date, "issuing_organization": organization, "description": line}
        )

    return training_details
