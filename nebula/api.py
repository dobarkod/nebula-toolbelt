import sys
from time import sleep
from functools import wraps

import requests

from nebula.conf import NEBULA_API_URL, API_KEY, _init_conf_file

##################### API CALLS ######################
LOGIN = 'login'
GET = 'get'
PROVISIONING_STATUS = 'provisioning-status'
##################### END API calls ##################


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not API_KEY:
            print('Please login first.')
            sys.exit(1)
        return f(*args, **kwargs)
    return wrapper


def _construct_url(action, service=None, service_id=None, plan=None, platform=None):
    apis = {
        LOGIN: NEBULA_API_URL +
            'login/',
        GET: NEBULA_API_URL +
            '{0}/get/service/{1}-{2}/{3}/'.format(API_KEY, service, plan, platform),
        PROVISIONING_STATUS: NEBULA_API_URL +
            '{0}/service/{1}/status/'.format(API_KEY, service_id)
    }
    return apis[action]


def _api_request(method, url, **kwargs):
    try:
        r = method(url, **kwargs)
    except:
        print('Error connecting to Nebula API.')
        print('Please try again later.')
        sys.exit(1)

    try:
        data = r.json()
    except:
        print('Error: Unexpected response from Nebula API: {}'.format(r.content))
        sys.exit(1)
    try:
        status_code = r.status_code
    except:
        print('Error connecting to Nebula API.')
        print('Please try again later.')
        sys.exit(1)

    return status_code, data


def login():
    from getpass import getpass

    try:
        input = raw_input
    except NameError:
        pass
    email = input("Email: ")
    password = getpass()
    url = _construct_url(LOGIN)
    status_code, data = _api_request(
        requests.post,
        url,
        data={'email': email, 'password': password})

    if status_code == 401:
        print(data['errors'])
        sys.exit(1)

    if status_code == 200:
        api_key = data['api_key']
        _init_conf_file(api_key)
        print('Login Successful!')
        sys.exit(0)


@require_api_key
def get_service_status(service_id, retry=False):
    try:
        url = _construct_url(PROVISIONING_STATUS, service_id=service_id)
        if retry:
            for ping in range(1, 60):
                status_code, data = _api_request(requests.get, url)
                if status_code == 404:
                    sys.stdout.write('\r{0}'.format('.' * ping))
                    sys.stdout.flush()
                    sleep(5)
                if status_code == 200:
                    print(data['success'])
                    print('Connection string: ' + data['connection_string'])
                    sys.exit(0)
            print('\nError: This seems to be taking longer than expected.')
            print('Please wait a few minutes and then check service status manually with "nebula status".')
        else:
            status_code, data = _api_request(requests.get, url)
            if status_code == 403:
                print(data)
                sys.exit(1)
            if status_code == 404:
                print('We could not find a service with the given ID.')
                sys.exit(1)
            if status_code == 200:
                print(data['success'])
                print('Connection string: ' + data['connection_string'])
                sys.exit(0)

    except KeyboardInterrupt:
        print('\nNOTE: You can still check the progress with the status command.')


@require_api_key
def get_service(service, plan, platform):
    url = _construct_url(GET, service=service, plan=plan, platform=platform)
    status_code, data = _api_request(requests.get, url)
    if status_code != 200:
        print(data)
        sys.exit(1)

    service_id = data.get('id')

    if not service_id:
        print('Error: Could not retrieve Service ID from Nebula API')
        sys.exit(1)

    return service_id
