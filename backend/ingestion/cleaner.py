def remove_page_numbers(text:str) -> str:
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if not line.strip().isdigit():  # Remove lines that are just page numbers
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def normalize_whitespace(text:str) -> str:
    return ' '.join(text.split())

def trim_text(text:str) -> str:
    return text.strip()

def clean_text(text:str) -> str:
    text = remove_page_numbers(text)
    text = normalize_whitespace(text)
    text = trim_text(text)
    return text
