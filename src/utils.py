import json
import os
import random
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
import glob
from webdriver_manager.chrome import ChromeDriverManager

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&display=swap" rel="stylesheet" /> 
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" /> 
    <link rel="stylesheet" href="$style_path">
</head>
$markdown
</body>
</html>
"""
def create_driver_selenium():
    chrome_options = webdriver.ChromeOptions()
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def HTML_to_PDF(FilePath):
    # Validate and prepare file paths
    if not os.path.isfile(FilePath):
        raise FileNotFoundError(f"The specified file does not exist: {FilePath}")
    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"
    driver = create_driver_selenium()
    try:
        driver.get(FilePath)
        time.sleep(3)
        start_time = time.time()
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,         # Include lo sfondo nella stampa
            "landscape": False,              # Stampa in verticale (False per ritratto)
            "paperWidth": 8.27,              # Larghezza del foglio in pollici (A4)
            "paperHeight": 11.69,            # Altezza del foglio in pollici (A4)
            "marginTop": 0.8,                # Margine superiore in pollici (circa 2 cm)
            "marginBottom": 0.8,             # Margine inferiore in pollici (circa 2 cm)
            "marginLeft": 0.8,               # Margine sinistro in pollici (circa 2 cm)
            "marginRight": 0.8,              # Margine destro in pollici (circa 2 cm)
            "displayHeaderFooter": False,   # Non visualizzare intestazioni e piè di pagina
            "preferCSSPageSize": True,       # Preferire le dimensioni della pagina CSS
            "generateDocumentOutline": False, # Non generare un sommario del documento
            "generateTaggedPDF": False,      # Non generare PDF taggato
            "transferMode": "ReturnAsBase64" # Restituire il PDF come stringa base64
        })
        if time.time() - start_time > 120:
            raise TimeoutError("PDF generation exceeded the specified timeout limit.")
        return pdf_base64['data']
    except WebDriverException as e:
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        driver.quit()

def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1200x800")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--incognito")
    return options

def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")