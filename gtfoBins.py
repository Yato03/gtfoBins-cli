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

def help():
    log.info("Uso: gtfoBins.py <modo> \nModos: \n\t- all \n\t- command \n\t- shell \n\t- suid \n\t- sudo \n\t- capabilities")
    sys.exit(0)


if(len(sys.argv) != 2) or (sys.argv[1] not in ["all", "command", "shell", "suid", "sudo", "capabilities"]):
    help()

modo = "#+" + sys.argv[1] if sys.argv[1] != "all" else ""


p = log.progress("Progreso")
p.status("Abriendo navegador...")
# Configura el servicio de ChromeDriver
service = Service(GeckoDriverManager().install())

options = Options()
options.headless = True

# Inicializa el navegador
driver = webdriver.Firefox(service=service, options=options)

url = "https://gtfobins.github.io/" + modo

p.status("Cargando página...")
driver.get(url)
# Espera un momento para que la página cargue completamente
driver.implicitly_wait(1)

# Obtiene el contenido HTML de la página
data = driver.page_source

#print(data)

# Cierra el navegador
driver.quit()

p.status("Procesando datos...")

# Usar BeautifulSoup para analizar el HTML
soup = BeautifulSoup(data, 'html.parser')

# Encontrar y eliminar los <tr> con style="display:none"
for tr in soup.find_all('tr'):
    if tr.get('style') and 'display:none' in tr.get('style').replace(' ', ''):
        tr.decompose()

p.status("Comparando resultados")
# Guardar el resultado en un archivo HTML
with open("binaries.txt", "r", encoding="utf-8") as file:
    binaries = file.read()
    binaries = binaries.split("\n")
    alguno = False
    for binary in binaries:
        directories = binary.split("/")
        b = directories[-1]
        el = soup.find("a", string=b)
        
        if el is not None:
            tr = el.find_parent("tr")
            ul = tr.find("ul", attrs={"class": "function-list"})
            a = ul.find_all("a")
            problems = ",".join([a.text for a in a])
            log.success("SUID Vulnerable: " + binary + "->" + problems)
            alguno = True

if not alguno:
    log.failure("No se encontraron binarios vulnerables")

p.success("GG!")