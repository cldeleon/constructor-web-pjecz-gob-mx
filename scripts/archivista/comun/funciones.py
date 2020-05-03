import re
import unicodedata

def cambiar_acentos(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return(str(text))

def cambiar_a_ruta_segura(text):
    text = cambiar_acentos(text.lower())
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_/-]', '', text)
    return(text)

def cambiar_a_identificador(text):
    text = cambiar_acentos(text.lower())
    text = re.sub('[/]+', '-', text)
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return(text)
