import re


def extract_awards(awards_section_str, cv_string: str):
    awards_details = []
    date_pattern = r'(?:(?:19|20)\d{2}|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{4})'
    if len(awards_section_str) > 5:
        awards_list = awards_section_str.split("\n")
    else:
        award_keywords = [
            "award",
            "honor",
            "scholarship",
            "fellowship",
            "recognition",
            "prize",
            "distinction",
            "achievement",
            "recipient",
            "winner",
            "nominated",
            "granted",
        ]
        awards_list = [] 

        for line in cv_string.split("\n"):
            if any(keyword in line.lower() for keyword in award_keywords):
                awards_list.append(line.strip())  
    for line in awards_list:
        match = re.search(date_pattern, line, re.IGNORECASE)
        date = None
        if match:
            date = match.group() 
        awards_details.append({"date": date, "description": line})
    return awards_details

