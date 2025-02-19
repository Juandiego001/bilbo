import os
import json
import data
import colorama
import requests
from pathlib import Path
from colorama import Fore
from dotenv import load_dotenv, set_key

# Carga las variables de entorno del archivo .env
dotenv_path = Path('.env')
load_dotenv(dotenv_path)

API_PORT = os.getenv('API_PORT')
WP_NUMBER = os.getenv('WP_NUMBER')
FULL_URL = f'http://localhost:{API_PORT}/api/chatbot/webhook'

def check_env_vars() -> None:
    '''Function to verify if the environment variables are setted'''
    global API_PORT, WP_NUMBER, FULL_URL

    if not os.getenv('API_PORT'):
        print(Fore.CYAN + 'Ingrese el valor para el puerto del backend (API_PORT): ')
        API_PORT = input(Fore.YELLOW + '> ')
        FULL_URL = f'http://localhost:{API_PORT}/webhook'
        set_key(dotenv_path, 'API_PORT', API_PORT)
        print(Fore.CYAN + 'API_PORT configurada y guardada en .env')

    if not os.getenv('WP_NUMBER'):
        print(Fore.CYAN + 'Ingrese el número a donde desea recibir los mensajes (WP_NUMBER). Recuerde colocar 57 para especificar que es de Colombia: ')
        WP_NUMBER = input(Fore.YELLOW + '> ')
        set_key(dotenv_path, 'WP_NUMBER', WP_NUMBER)
        print(Fore.CYAN + 'WP_NUMBER configurada y guardada en .env')


# Formato base para el envío de los mensajes a WhatsApp
send_data = data.data

# Inicializar colorama para habilitar colores en Windows
colorama.init(autoreset=True)

# Convertir el diccionario a formato JSON
headers = {'Content-Type': 'application/json'}

def send_message(temp_number: str = '') -> None:
    '''Function to send message'''

    final_wp_number = temp_number if temp_number else WP_NUMBER

    print(Fore.CYAN + 'Mensaje a enviar: ')
    message = input(Fore.YELLOW + '> ')
    print('')

    # Se especifica a enviar el mensaje ingresado anteriormente
    send_data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'] = message

    # Se especifica el teléfono al que se enviará el mensaje de respuesta del bot
    send_data['entry'][0]['changes'][0]['value']['messages'][0]['from'] = final_wp_number

    # Envío de petición
    response = requests.post(FULL_URL, headers=headers, data=json.dumps(data.data))

     # Verificar el estado de la respuesta
    if response.status_code == 200:
        print(Fore.CYAN + f'Respuesta: ')
        print(Fore.YELLOW + f'> {response.json().get('message')}')
        print('')
    

if __name__ == '__main__':
    print(Fore.GREEN + 'Script para automatizar el envío de mensajes de WhatsApp con el fin de agilizar las pruebas.\n')
    check_env_vars()

    while True:
        print(Fore.CYAN + '¿Qué quieres hacer?')
        print(Fore.CYAN + '1. Enviar un mensaje')
        print(Fore.CYAN + '2. Ver variables de entorno')
        print(Fore.CYAN + '3. Cambiar variables de entorno')
        print(Fore.CYAN + '4. Enviar un mensaje temporalmente a otro número')
        print(Fore.CYAN + '5. Finalizar')
        selection = int(input(Fore.CYAN + '> '))
        print('')

        if selection == 1:
            send_message()
        elif selection == 2:
            print(Fore.CYAN + f'API_PORT: {API_PORT}')
            print(Fore.CYAN + f'WP_NUMBER: {WP_NUMBER}')
        elif selection == 3:
            print(Fore.CYAN + 'Ingrese el valor para el puerto del backend (API_PORT): ')
            API_PORT = input(Fore.YELLOW + '> ')
            print(Fore.CYAN + 'Ingrese el número a donde desea recibir los mensajes (WP_NUMBER). Recuerde colocar 57 para especificar que es de Colombia: ')
            WP_NUMBER = input(Fore.YELLOW + '> ')
        elif selection == 4:
            print(Fore.CYAN + 'Ingrese el número temporal a donde desea recibir los mensajes. Recuerde colocar 57 para especificar que es de Colombia: ')
            temp_number = input(Fore.YELLOW + '> ')
            print('')
            send_message(temp_number)
        elif selection == 5:
            break

        print('')
