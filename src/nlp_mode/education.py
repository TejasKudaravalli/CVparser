import re 
import spacy
import pandas as pd 

nlp = spacy.load("en_core_web_sm")

def extract_education(cv_string: str) -> list:
    degree_pattern = r"\b(Bachelor|Master|PhD|Doctorate|Associate|Diploma|Certificate|B\.?Tech|B\.?S\.?|M\.?S\.?|M\.?Sc\.?|Ph\.?D\.?)\b"
    institution_pattern = r"((?:University|College|Institute)[A-Za-z\s]*|[A-Za-z\s]*(?:University|College|Institute))"
    year_pattern = r"(\d{4})"
    education_details = []
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
        blocks.append('\n'.join(current_block))
    
    for block in blocks:
        doc = nlp(block)
        lines = block.split("\n")
        degree = None
        university = None
        for line in lines:
            if re.search(degree_pattern, line, re.IGNORECASE):
                cleaned_line = re.sub(r'\s{2,}', '\n', line.strip()).split("\n")[0]
                degree = cleaned_line
                break
        for ent in doc.ents:
            if ent.label_ == "ORG":
                university = ent.text 
                break 
        else:
            for line in lines:
                if re.search(institution_pattern, line, re.IGNORECASE):
                    cleaned_line = re.sub(r'\s{2,}', '\n', line.strip())
                    university = cleaned_line
        
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        start_date, end_date = None, None
        if len(dates) < 1:
            date_match = re.search(year_pattern, block)
            start_date, end_date = min(date_match), max(date_match)
        elif len(dates) == 1:
            end_date = dates[0]
        elif len(dates) > 1:
            start_date, end_date = min(dates), max(dates)
        
        education_details.append({
            "description": degree,
            "issuing_organization": university,
            "start_date": start_date,
            "end_date": end_date
        })
    return education_details