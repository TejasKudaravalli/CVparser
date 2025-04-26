import re
import spacy
import pandas as pd
import string

nlp = spacy.load("en_core_web_sm")


def extract_experience(cv_string: str) -> list:
    experience_details = []
    blocks = []
    current_block = []
    for line in cv_string.split("\n"):
        line = line.strip()
        if len(line) < 5:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    for block in blocks:
        organization = None
        dates = []
        is_current = False
        location = None
        doc = nlp(block)

        # Organization extraction
        for ent in doc.ents:
            if ent.label_ == "ORG":
                organization = ent.text
                break

        for ent in doc.ents:
            if ent.label_ == "GPE":
                location = ent.text
                break

        for ent in doc.ents:
            if ent.label_ == "DATE":
                dates.append(ent.text)

        lines = block.split("\n")
        job_titles = []
        used_lines = set()

        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean or line_clean in used_lines or line_clean.startswith(("•","-")):
                continue

            if organization.lower() in line_clean.lower():
                prev_line = lines[i-1].strip() if i > 0 else ""
                next_line = lines[i+1].strip() if i < len(lines) - 1 else ""
                if not prev_line.startswith(("•","-","▪")):
                    job_titles.append(prev_line)
                if not next_line.startswith(("•","-","▪")):
                    job_titles.append(next_line)
        job_titles = "\n".join(job_titles)
        job_titles = job_titles.replace(organization, "").replace(location, "")
        for d in dates:
            job_titles = job_titles.replace(d, "")
        job_titles = re.sub(rf"[{re.escape(string.punctuation)}]|\s{{2,}}|[\n\r]", " ", job_titles).strip()

        dates = pd.to_datetime(dates, errors="coerce").dropna()
        if len(dates) < 1:
            start_date, end_date = None, None
        if len(dates) == 1:
            start_date, end_date = dates[0].strftime("%b %Y"), None
            is_current = True
            duration = (pd.Timestamp.now() - dates[0]).days // 30
        if len(dates) > 1:
            start_date, end_date = (
                dates.min().strftime("%b %Y"),
                dates.max().strftime("%b %Y"),
            )
            duration = (dates.max() - dates.min()).days // 30

        experience_details.append(
            {
                "start_date": start_date,
                "is_current": is_current,
                "end_date": end_date,
                "duration_in_months": duration,
                "location": location,
                "title": job_titles,
                "organization": organization,
                "description": "\n".join([line for line in block.split("\n") if line.startswith(("•","-","▪"))]),
            }
        )

    return experience_details
