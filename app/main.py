import os
import fitz  # PyMuPDF
import re

def pdf_to_text(pdf_path):
    # Abre o arquivo PDF
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Itera por cada página
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    return text

def extract_values_from_text(text, patterns):
    results = {}
    for key, (pattern, unit) in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results[key] = {
                "value": match.group(1),
                "unit": unit
            }
    return results

def extract_blood_values(pdf_path):
    # Define os padrões de expressões regulares e unidades correspondentes
    patterns = {
        "hemoglobin": (r'HEMOGLOBINA(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)', "g/dL"),
        "hematocrit": (r'HEMATÓCRITO(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)%?', "%"),
        "eritrocitos": (r'HEMÁCIAS(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)', "milhões/mm3"),
        "hba1c": (r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*%', "%"),
        "ast": (r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "alt": (r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "ureia": (r'UREIA\s*.*?RESULTADO:\s*(\d+|\d+,\d+|\d+\.\d+)\s*mg/dL', "mg/dL"),
        "creatinina": (r'CREATININA\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*mg/dL', "mg/dL")
    }
    
    # Converte o PDF para texto
    pdf_text = pdf_to_text(pdf_path)
    
    # Extrai os valores
    blood_values = extract_values_from_text(pdf_text, patterns)
    
    return blood_values

def print_blood_values(blood_values):
    # Define os campos e a ordem de impressão
    fields = [
        ("Hemoglobina", "hemoglobin"),
        ("Hematócrito", "hematocrit"),
        ("Eritrócitos (Hemácias)", "eritrocitos"),
        ("Hemoglobina Glicada (HbA1c)", "hba1c"),
        ("AST (TGO)", "ast"),
        ("ALT (TGP)", "alt"),
        ("Ureia", "ureia"),
        ("Creatinina", "creatinina")
    ]
    
    for label, key in fields:
        value = blood_values.get(key, {}).get("value", "")
        unit = blood_values.get(key, {}).get("unit", "")
        print(f"Valor {label}: {value} {unit}")

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Especifica o caminho para o arquivo PDF
pdf_path = os.path.join(script_dir, 'hemograma.pdf')  # Caminho absoluto para o arquivo PDF

# Extrai os valores do PDF
blood_values = extract_blood_values(pdf_path)

# Imprime os valores extraídos com unidades
print_blood_values(blood_values)
