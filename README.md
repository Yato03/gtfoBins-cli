# GTFOBins CLI

Herramienta para consultar rápidamente un conjunto de binarios en la plataforma [GTFOBins](https://gtfobins.github.io/) desde la consola.

## Instalación

```bash
git clone https://github.com/Yato03/gtfoBins-cli
cd gtfoBins-cli
pip install -r requirements.txt
```

## Uso

1. Introducir los binarios en el archivo `binaries.txt`
2. Ejecutar `gtfoBins.py` indicando el tipo de búsqueda que queremos hacer

```bash
python3 gtfoBins.py <modo> 
    Modos:
        - all
        - command
        - shell
        - suid
        - sudo
        - capabilities
```