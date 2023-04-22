from database_operations import store_data
import json

################################################################################
#                               GET ENDPOINTS                                  #
################################################################################

def get_status():
    return {'status': 'OK'}

################################################################################
#                              POST ENDPOINTS                                  #
################################################################################

def post_status(data):
    store_data(data)
    return {'status': 'OK', 'data': data.decode()}

################################################################################
#                              ERROR ENDPOINTS                                 #
################################################################################

def get_404():
    return {'error': 'Endpoint not found'}

def post_404(data):
    return {'error': 'Endpoint not found', 'data': data.decode()}

