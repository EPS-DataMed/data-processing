import os
import fitz  # PyMuPDF
import re
from datetime import datetime

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
    results = []
    for key, (pattern, unit) in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results.append({
                "tipo": key,
                "valor": f"{match.group(1)} {unit}"
            })
    return results

def extract_exam_date(text):
    pattern_date = r'Atendimento\s*:\s*(\d{2}/\d{2}/\d{4})'
    match = re.search(pattern_date, text)
    if match:
        return datetime.strptime(match.group(1), '%d/%m/%Y')
    return None

def extract_blood_values(pdf_path):
    # Define os padrões de expressões regulares e unidades correspondentes
    patterns = {
        "Hemoglobina": (r'HEMOGLOBINA(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)', "g/dL"),
        "Hematócrito": (r'HEMATÓCRITO(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)%?', "%"),
        "Eritrócitos (Hemácias)": (r'HEMÁCIAS(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)', "milhões/mm3"),
        "Hemoglobina Glicada (HbA1c)": (r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*%', "%"),
        "AST (TGO)": (r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "ALT (TGP)": (r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "Ureia": (r'UREIA\s*.*?RESULTADO:\s*(\d+|\d+,\d+|\d+\.\d+)\s*mg/dL', "mg/dL"),
        "Creatinina": (r'CREATININA\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*mg/dL', "mg/dL")
    }
    
    # Converte o PDF para texto
    pdf_text = pdf_to_text(pdf_path)
    
    # Extrai a data do exame
    exam_date = extract_exam_date(pdf_text)
    
    # Extrai os valores
    blood_values = extract_values_from_text(pdf_text, patterns)
    
    # Adiciona a data do exame a cada valor
    for value in blood_values:
        value["data_exame"] = exam_date

    return blood_values

# Obtém o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Especifica o caminho para o arquivo PDF
pdf_path = os.path.join(script_dir, 'hemograma.pdf')  # Caminho absoluto para o arquivo PDF

# Extrai os valores do PDF
blood_values = extract_blood_values(pdf_path)

# Imprime os valores extraídos
for value in blood_values:
    print(value)
