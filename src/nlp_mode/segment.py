import re 

def segment_resume_sections(cv_string: str) -> list[dict[str, str]]:
    lines = cv_string.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            cleaned_lines.append((stripped_line, False))
        else:
            cleaned_lines.append(("", True))

    potential_headers = []
    for i, (line, is_empty) in enumerate(cleaned_lines):
        if is_empty or len(line) > 30 or line.islower():
            continue

        # Upper case or ends with :
        if line.isupper() or line.endswith(":"):
            potential_headers.append(i)
            continue
        elif (
            line.startswith("•")
            or line.startswith("-")
            or bool(re.search(r"\d", line))
            or len(line) < 5
        ):
            continue
        elif (i > 0 and cleaned_lines[i - 1][1]) or (
            i < len(cleaned_lines) - 1 and cleaned_lines[i + 1][1]
        ):
            potential_headers.append(i)

    sections = []
    content_lines = []
    for j in range(0, potential_headers[0]):
        content_lines.append(cleaned_lines[j][0])
    content = "\n".join(content_lines).strip()
    sections.append({"header": "Personal Details", "content": content})
    for i in range(len(potential_headers)):
        start_idx = potential_headers[i]
        end_idx = len(cleaned_lines)
        if i < len(potential_headers) - 1:
            end_idx = potential_headers[i + 1]

        header = cleaned_lines[start_idx][0]
        content_lines = []
        for j in range(start_idx + 1, end_idx):
            content_lines.append(cleaned_lines[j][0])

        content = "\n".join(content_lines).strip()

        if content.strip():
            sections.append({"header": header, "content": content})

    return sections
