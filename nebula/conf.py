from os.path import expanduser, join


##################### CONFIG #########################
NEBULA_API_URL = 'http://localhost:8000/api/v1/'
CONFIG = join(expanduser("~"), '.nebula.conf')
PLATFORMS = ['digital-ocean', 'rackspace', 'linode', 'aws']
#################### END CONFIG ######################


def _get_api_key():
    API_KEY = None
    try:
        with open(CONFIG) as config:
            lines = config.readlines()
            for line in lines:
                if line.startswith('API_KEY'):
                    API_KEY = line.split('=')[1].strip()
    except IOError:
        print('Warning: File nebula.conf not found.')
    return API_KEY


def _init_conf_file(api_key):
    """
    This function is used to initialize the ~/.nebula.conf file and to refresh it
    with a new API_KEY
    """
    with open(CONFIG, 'w') as config:
        line = 'API_KEY={0}'.format(api_key)
        config.write(line)


API_KEY = _get_api_key()
