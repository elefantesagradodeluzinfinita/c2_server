from emergency import Emergency
from database_operations import store_snapshot_data
from database_operations import insert_emergencies
from database_operations import get_pending_gps
import json
import requests
import re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

################################################################################
#                               GET ENDPOINTS                                  #
################################################################################

def get_main():
    return {'location': 'main'}

def get_status():
    return {'status': 'OK'}

def get_pending_gps_list():
    return {'gps list': get_pending_gps()}

def get_data_curl():
    # Obtener datos de la página web
    url = 'https://sgonorte.bomberosperu.gob.pe/24horas'
    response = requests.get(url)
    html = response.content

    # Parsear los datos HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar el elemento tbody
    tbody = soup.find('tbody')

    # Inicializar el contador
    count_tr = 0

    # Lista para almacenar las instancias de Emergency
    emergencies = []

    # Recorrer el interior del tbody
    for tr in tbody.find_all('tr'):
        # Reiniciar el contador
        count_else = 0

        # Variables para almacenar los valores de cada etiqueta
        identifier = ''
        timestamp = ''
        location = ''
        type = ''
        status = ''
        units = ''
        other = ''
        map = ''

        # Mostrar los valores de cada elemento interno del tr
        for th in tr.find_all('th'):
            if th.text.strip() != '':
                print(th.text.strip())

        for td in tr.find_all('td'):
            if td.text.strip() != '':
                    count_else += 1
                    if count_else == 1:
                        identifier = td.text.strip()
                        print("<IDENTIFIER>" + td.text.strip() + "</IDENTIFIER>")
                    elif count_else == 2:
                        timestamp = td.text.strip()
                        print("<TIMESTAMP>" + td.text.strip() + "</TIMESTAMP>")
                    elif count_else == 3:
                        location = td.text.strip()
                        print("<LOCATION>" + td.text.strip() + "</LOCATION>")
                    elif count_else == 4:
                        type = td.text.strip()
                        print("<TYPE>" + td.text.strip() + "</TYPE>")
                    elif count_else == 5:
                        status = td.text.strip()
                        print("<STATUS>" + td.text.strip() + "</STATUS>")
                    elif count_else == 6:
                        units = td.text.strip().replace('\n', ', ')
                        print("<UNITS>" + td.text.strip().replace('\n', ', ') + "</UNITS>")
                    else:
                        other = td.text.strip()
                        print("<OTHER>" + td.text.strip() + "</OTHER>")
        
        for button in tr.find_all('button'):
            if button.has_attr('onclick'):
                map = button['onclick']
                print("<MAP>" + button['onclick'] + "</MAP>")
        
        # Crear una instancia de Emergency con los valores asignados
        emergency = Emergency(identifier, timestamp, location, type, status, units, other, map)

        # Agregar la instancia a la lista de emergencies
        emergencies.append(emergency)

        # Incrementar el contador y salir del bucle si se han dado 5 vueltas
        #count_tr += 1
        #if count_tr == 5:
        #    break

    insert_emergencies(emergencies)

    # Devolver un diccionario que indique que todo ha salido correctamente
    return {'status': 'OK'}

################################################################################
#                              POST ENDPOINTS                                  #
################################################################################

def post_status(data):
    store_snapshot_data(data)
    return {'status': 'OK', 'data': data.decode()}

################################################################################
#                              ERROR ENDPOINTS                                 #
################################################################################

def get_404():
    return {'error': 'Endpoint not found'}

def post_404(data):
    return {'error': 'Endpoint not found', 'data': data.decode()}

