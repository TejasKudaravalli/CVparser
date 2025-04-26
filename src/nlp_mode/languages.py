import spacy

nlp = spacy.load("en_core_web_sm")

def extract_languages(cv_string) -> list:
    doc = nlp(cv_string)
    language_list = [ent.text.title() for ent in doc.ents if ent.label_ == "LANGUAGE"]
    language_list.append("English")
    return list(set(language_list))