import os
import fitz  # PyMuPDF
import re

def pdf_to_text(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Iterate through each page
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    return text

def extract_blood_values(text):
    # Regular expression patterns to find values of Hemoglobina, Hematócrito, and Eritrócitos
    pattern_hemoglobin = r'HEMOGLOBINA(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)'
    pattern_hematocrit = r'HEMATÓCRITO(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)%?'
    pattern_eritrocitos = r'HEMÁCIAS(?:\s*?:\s*?|.*?RESULTADO:\s*)(\d+,\d+|\d+\.\d+|\d+)'
    pattern_hba1c = r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*%'
    pattern_ast = r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L'
    pattern_alt = r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L'
    pattern_ureia = r'UREIA\s*.*?RESULTADO:\s*(\d+|\d+,\d+|\d+\.\d+)\s*mg/dL'
    pattern_creatinina = r'CREATININA\s*.*?RESULTADO:\s*(\d+,\d+|\d+\.\d+)\s*mg/dL'
    
    # Search for the patterns in the text
    match_hemoglobin = re.search(pattern_hemoglobin, text, re.DOTALL)
    match_hematocrit = re.search(pattern_hematocrit, text, re.DOTALL)
    match_eritrocitos = re.search(pattern_eritrocitos, text, re.DOTALL)
    match_hba1c = re.search(pattern_hba1c, text, re.DOTALL)
    match_ast = re.search(pattern_ast, text, re.DOTALL)
    match_alt = re.search(pattern_alt, text, re.DOTALL)
    match_ureia = re.search(pattern_ureia, text, re.DOTALL)
    match_creatinina = re.search(pattern_creatinina, text, re.DOTALL)
    
    # If matches are found, return the values, otherwise return None
    return {
        "hemoglobin": match_hemoglobin.group(1) if match_hemoglobin else None,
        "hematocrit": match_hematocrit.group(1) if match_hematocrit else None,
        "eritrocitos": match_eritrocitos.group(1) if match_eritrocitos else None,
        "hba1c": match_hba1c.group(1) if match_hba1c else None,
        "ast": match_ast.group(1) if match_ast else None,
        "alt": match_alt.group(1) if match_alt else None,
        "ureia": match_ureia.group(1) if match_ureia else None,
        "creatinina": match_creatinina.group(1) if match_creatinina else None
    }

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the PDF file
pdf_path = os.path.join(script_dir, 'hemograma.pdf')  # Caminho absoluto para o arquivo PDF

# Convert PDF to text
pdf_text = pdf_to_text(pdf_path)

# Extract values
blood_values = extract_blood_values(pdf_text)

# Print the extracted values
print("Valor da Hemoglobina:", blood_values["hemoglobin"])
print("Valor do Hematócrito:", blood_values["hematocrit"])
print("Valor dos Eritrócitos (Hemácias):", blood_values["eritrocitos"])
print("Valor da Hemoglobina Glicada (HbA1c):", blood_values["hba1c"])
print("Valor da AST (TGO):", blood_values["ast"])
print("Valor da ALT (TGP):", blood_values["alt"])
print("Valor da Ureia:", blood_values["ureia"])
print("Valor da Creatinina:", blood_values["creatinina"])
