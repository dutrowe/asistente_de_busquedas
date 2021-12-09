import os, time, pathlib, sys, webbrowser, requests, bs4
import speech_recognition as sr
from gtts import gTTS as gt
from playsound import playsound as ps



saludo = """¿qué deseas buscar en yahoo?.

Puedes decir la palabra "cancelar" para cancelar la búsqueda."""

def hablar(frase_principal, frase_error, idioma = 'es', acento = 'com.mx'):
    """ 
    Funcionalidad para que el asistente hable; el idioma por default
    es Español y el acento Latino
    """
    try:
        gt(frase_principal, lang= idioma, tld= acento).save(pathlib.Path('sonido.wav'))
    # El introducir string de texto vacios, causa un AssertionError
    except AssertionError:
        gt(frase_error, lang= idioma, tld= acento).save(pathlib.Path('sonido.wav'))

    # Reproduce el sonido
    time.sleep(5)
    ps(pathlib.Path('sonido.wav'))

    # Borra el archivo creado
    os.remove(pathlib.Path('sonido.wav'))

def escuchar(idioma = 'es-MX', cmd_msg = 'Puedes hablar ahora', print_msg = False):

    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        if print_msg == True:
            print(cmd_msg)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language= idioma)
    except sr.UnknownValueError:
        texto = False

    return texto
    

if __name__ == '__main__':

    hablar(frase_principal= saludo, frase_error= "Se ha producido un error")
    respuesta = escuchar(cmd_msg= saludo, print_msg= True)
    cantidad = 0

    while respuesta == False:
        hablar(frase_principal= f'No escucho lo que dices... {saludo}', frase_error= "Se ha producido un error")
        respuesta = escuchar(cmd_msg= saludo)
        cantidad+=1
        if cantidad > 1 and respuesta == False:
            hablar(frase_principal= 'Voy a cerrar, hasta luego', frase_error= 'Error')
            break
            
    if respuesta == False:
        sys.exit()
    elif respuesta.lower() == 'cancelar':
        hablar(frase_principal= 'Hasta luego', frase_error= 'Error')
    else:
        hablar(frase_principal= f'Voy a buscar {respuesta} en yahoo, te aviso cuando haya terminado', frase_error= 'Error')

        # res = requests.get(f'https://google.com/search?q={respuesta}')
        res = requests.get(f'https://search.yahoo.com/search;_ylt=?p={respuesta}')
        # print(res.status_code)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        anchor_tags = soup.select('.searchCenterMiddle > li h3 > a')
        cantidad_resultados = min(3, len(anchor_tags))

        for link in anchor_tags[:cantidad_resultados + 1]:
            webbrowser.open(link.get('href'))
