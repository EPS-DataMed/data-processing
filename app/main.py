import re
from datetime import datetime

class DataScraped:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def extract_values_from_text(text, patterns):
    results = []
    for key, (pattern, unit) in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            name = key
            # value = f"{match.group(1)} {unit}"
            value = f"{match.group(1)}"
            value = value.replace(',', '.')
            results.append(
                DataScraped(name, value)
            )
    return results

def extract_test_date(text):
    pattern_date = r'Atendimento\s*:\s*(\d{2}/\d{2}/\d{4})'
    match = re.search(pattern_date, text)
    if match:
        return datetime.strptime(match.group(1), '%d/%m/%Y')
    return None

def extract_data_and_date(text):
    patterns = {
        "hemoglobin": (r'HEMOGLOBINA\s*([\d,\.]+)\s*g/dL', "g/dL"),
        "hematocrit": (r'HEMATÓCRITO\s*([\d,\.]+)\s*%', "%"),
        "red_blood_cell": (r'HEMÁCIAS\s*([\d,\.]+)\s*milhões/mm3', "milhões/mm3"),
        "glycated_hemoglobin": (r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*([\d,\.]+)\s*%', "%"),
        "ast": (r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "alt": (r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "urea": (r'UREIA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL"),
        "creatinine": (r'CREATININA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL")
    }
    
    test_date = extract_test_date(text)
    
    data_values = extract_values_from_text(text, patterns)
    
    return data_values, test_date

def text_processing(text):
    data_values, test_date = extract_data_and_date(text)
    return data_values, test_date
