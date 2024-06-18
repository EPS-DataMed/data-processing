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
    
    # Define units
    units = {
        "hemoglobin": "g/dL",
        "hematocrit": "%",
        "eritrocitos": "milhões/mm3",
        "hba1c": "%",
        "ast": "U/L",
        "alt": "U/L",
        "ureia": "mg/dL",
        "creatinina": "mg/dL"
    }
    
    # Prepare results dictionary
    results = {}
    
    # Populate results dictionary with extracted values and units
    if match_hemoglobin:
        results["hemoglobin"] = {
            "value": match_hemoglobin.group(1),
            "unit": units["hemoglobin"]
        }
    if match_hematocrit:
        results["hematocrit"] = {
            "value": match_hematocrit.group(1),
            "unit": units["hematocrit"]
        }
    if match_eritrocitos:
        results["eritrocitos"] = {
            "value": match_eritrocitos.group(1),
            "unit": units["eritrocitos"]
        }
    if match_hba1c:
        results["hba1c"] = {
            "value": match_hba1c.group(1),
            "unit": units["hba1c"]
        }
    if match_ast:
        results["ast"] = {
            "value": match_ast.group(1),
            "unit": units["ast"]
        }
    if match_alt:
        results["alt"] = {
            "value": match_alt.group(1),
            "unit": units["alt"]
        }
    if match_ureia:
        results["ureia"] = {
            "value": match_ureia.group(1),
            "unit": units["ureia"]
        }
    if match_creatinina:
        results["creatinina"] = {
            "value": match_creatinina.group(1),
            "unit": units["creatinina"]
        }
    
    return results

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path to the PDF file
pdf_path = os.path.join(script_dir, 'hemograma.pdf')  # Caminho absoluto para o arquivo PDF

# Convert PDF to text
pdf_text = pdf_to_text(pdf_path)

# Extract values
blood_values = extract_blood_values(pdf_text)

# Print the extracted values with units
print("Valor da Hemoglobina:", blood_values.get("hemoglobin", {}).get("value"), blood_values.get("hemoglobin", {}).get("unit", ""))
print("Valor do Hematócrito:", blood_values.get("hematocrit", {}).get("value"), blood_values.get("hematocrit", {}).get("unit", ""))
print("Valor dos Eritrócitos (Hemácias):", blood_values.get("eritrocitos", {}).get("value"), blood_values.get("eritrocitos", {}).get("unit", ""))
print("Valor da Hemoglobina Glicada (HbA1c):", blood_values.get("hba1c", {}).get("value"), blood_values.get("hba1c", {}).get("unit", ""))
print("Valor da AST (TGO):", blood_values.get("ast", {}).get("value"), blood_values.get("ast", {}).get("unit", ""))
print("Valor da ALT (TGP):", blood_values.get("alt", {}).get("value"), blood_values.get("alt", {}).get("unit", ""))
print("Valor da Ureia:", blood_values.get("ureia", {}).get("value"), blood_values.get("ureia", {}).get("unit", ""))
print("Valor da Creatinina:", blood_values.get("creatinina", {}).get("value"), blood_values.get("creatinina", {}).get("unit", ""))
