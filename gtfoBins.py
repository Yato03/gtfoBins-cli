#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from pwn import *
import sys

def def_handler(sig, frame):
    log.warning("Exiting...")
    sys.exit(1)

# Ctrl+c
signal.signal(signal.SIGINT, def_handler)

# Ayuda por si el comando se ha ejecutado mal
def help():
    log.info("Uso: gtfoBins.py <modo> \nModos: \n\t- all \n\t- command \n\t- shell \n\t- suid \n\t- sudo \n\t- capabilities")
    sys.exit(0)

if __name__ == '__main__':
    
    # Comprobación de los argumentos
    if(len(sys.argv) != 2) or (sys.argv[1] not in ["all", "command", "shell", "suid", "sudo", "capabilities"]):
        help()

    # Ajuste de la URL
    modo = "#+" + sys.argv[1] if sys.argv[1] != "all" else ""
    url = "https://gtfobins.github.io/" + modo

    p = log.progress("Progreso")
    p.status("Abriendo navegador...")

    # Configuración del servicio de GeckoDriver
    service = Service(GeckoDriverManager().install())

    # Configuración headless para que no aparezca el navegador
    options = Options()
    options.add_argument("--headless")

    # Inicialización del navegador Firefox
    driver = webdriver.Firefox(service=service, options=options)

    # Cargar la página
    p.status("Cargando página...")
    driver.get(url)

    # Espera un momento para que la página cargue completamente
    driver.implicitly_wait(1)

    # Obtiene el contenido HTML de la página
    data = driver.page_source

    # Cierra el navegador
    driver.quit()

    p.status("Procesando datos...")

    # Uso de BeautifulSoup para el análisis el HTML
    soup = BeautifulSoup(data, 'html.parser')

    # Encontrar y eliminar los <tr> con style="display:none"
    for tr in soup.find_all('tr'):
        if tr.get('style') and 'display:none' in tr.get('style').replace(' ', ''):
            tr.decompose()

    # Encontrar los binarios
    p.status("Comparando resultados")
    with open("binaries.txt", "r", encoding="utf-8") as file:
        binaries = file.read()
        binaries = binaries.split("\n")
        alguno = False # Variable para comprobar si se ha encontrado algún binario vulnerable
        for binary in binaries:
            # Coger solo el nombre del binario. Ej: /usr/bin/whoami -> whoami
            directories = binary.split("/")
            b = directories[-1]

            if b == "":
                continue

            # Ej: <a>whoami</a>
            el = soup.find("a", string=b)
            
            if el is not None:
                # Encontrar vulnerabilidades del binario
                tr = el.find_parent("tr")
                ul = tr.find("ul", attrs={"class": "function-list"})
                a = ul.find_all("a")

                problems = ",".join([a.text for a in a])

                log.success("Binario Vulnerable: " + binary + "->" + problems)
                alguno = True

    if not alguno:
        log.failure("No se encontraron binarios vulnerables")

    p.success("GG!")
