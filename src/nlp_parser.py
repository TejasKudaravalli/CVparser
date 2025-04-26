import pymupdf
import re
from rich import print
import spacy
import docx
import striprtf
from src.nlp_mode import (
    segment_resume_sections,
    extract_personal_details,
    extract_education,
    extract_experience,
    extract_languages,
    extract_awards,
    extract_trainings_certifications,
    extract_references
)

nlp = spacy.load("en_core_web_md")


def read_file(cv_file: str) -> str:
    if cv_file.endswith(".pdf"):
        doc = pymupdf.open(cv_file)
        text = ""
        for page in doc:
            page_content = page.get_text()
            page_content = re.sub(r"[\u200b\u200c\u200d\uFEFF]\n?", "", page_content)
            text += page_content
        doc.close()
        return text.strip()
    elif cv_file.endswith(".docx"):
        doc = docx.Document(cv_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    elif cv_file.endswith(".rtf"):
        with open(cv_file, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
            text = striprtf.rtf_to_text(rtf_content)
        return text.strip()
    elif cv_file.endswith(".txt"):
        with open(cv_file, 'r', encoding='utf-8') as file:
            text = file.read()
        return text.strip()
    else:
        raise ValueError("Unsupported file format. Only PDF files are supported.")
    

def match_section(sections, target_labels, threshold=0.75):
    best_match = {}
    best_score = 0 
    for section in sections:
        header = section.get("header","").lower()
        if not header:
            continue

        header_doc = nlp(header)
        for label in target_labels:
            similarity = header_doc.similarity(nlp(label.lower()))
            if similarity > best_score and similarity >= threshold:
                best_match = section
                best_score = similarity
    return best_match


def extract_json_from_resume_nlp(file_path: str):
    resume_json = {}
    content = read_file(file_path)
    cv_sections = segment_resume_sections(content)
    personal_info_section = [
        section
        for section in cv_sections
        if section.get("header") == "Personal Details"
    ]
    personal_info_str = (
        personal_info_section[0]["content"] if len(personal_info_section) > 0 else ""
    )
    if len(personal_info_str) > 10:
        personal_info_str = personal_info_str.strip()
    else:
        personal_info_str = content
    personal_details = extract_personal_details(personal_info_str)

    education_section = match_section(cv_sections, ["Education", "Academic Background"])
    education_str = education_section.get("content","")
    education_details = extract_education(education_str)

    language_list = extract_languages(content)

    experience_section = match_section(cv_sections, ["Related Experience", "Employment History", "Work Experience"])
    experience_str = experience_section.get("content","")
    experience_details = extract_experience(experience_str)

    awards_section = match_section(cv_sections, ["Honors & Involvement", "Awards", "Achievements"])
    awards_str = awards_section.get("content","")
    awards_details = extract_awards(awards_str, content)

    trainings_section = match_section(cv_sections, ["Trainings", "Certifications", "Courses", "Professional Development"])
    trainings_str = trainings_section.get("content","")
    trainings_details = extract_trainings_certifications(trainings_str, content)

    references_section = match_section(cv_sections, ["References", "Referees", "Recommendation Letters"])
    references_str = references_section.get("content","")
    references_details = extract_references(references_str)


    resume_json["basic"] = personal_details
    resume_json["education"] = education_details
    resume_json["languages"] = language_list
    resume_json["professional_experiences"] = experience_details
    resume_json["awards"] = awards_details
    resume_json["trainings_and_certifications"] = trainings_details
    resume_json["references"] = references_details
    return resume_json

if __name__ == "__main__":
    cv_file = r"D:\Projects\cv-parser\data\CS_CV.pdf"
    # cv_file = r"D:\Projects\cv-parser\data\functionalsample.pdf"
    # cv_file = r"D:\Projects\cv-parser\data\Business_CV.pdf"
    result = extract_json_from_resume_nlp(cv_file)
    print(result)