import sys
import logging
from time import sleep
from functools import wraps

import requests

from nebula.conf import NEBULA_API_URL, API_KEY, _init_conf_file

##################### API CALLS ######################
LOGIN = 'login'
GET = 'get'
DESTROY = 'destroy'
STATUS = 'provisioning-status'
LIST = 'list'
##################### END API calls ##################


log = logging.getLogger(__name__)


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not API_KEY:
            log.info('Please login first.')
            sys.exit(1)
        return f(*args, **kwargs)
    return wrapper


def _construct_url(action, service=None, service_id=None, plan=None, platform=None, location=None):
    # FIXME: this is ugly
    if location is None:
        location = ''
    apis = {
        LOGIN: NEBULA_API_URL +
            'login/',
        GET: NEBULA_API_URL +
            '{0}/get/service/{1}-{2}/{3}/'.format(API_KEY, service, plan, platform) + location,
        STATUS: NEBULA_API_URL +
            '{0}/service/{1}/status/'.format(API_KEY, service_id),
        DESTROY: NEBULA_API_URL +
            '{0}/destroy/service/{1}/'.format(API_KEY, service_id),
        LIST: NEBULA_API_URL +
            '{0}/my/services/'.format(API_KEY),
    }
    return apis[action]


def _api_request(method, url, **kwargs):
    try:
        r = method(url, **kwargs)
    except Exception:
        log.error('Error connecting to Nebula API.')
        log.error('Please try again later.')
        sys.exit(1)

    try:
        data = r.json()
    except:
        log.error('Error: Unexpected response from Nebula API: {}'.format(r.content))
        sys.exit(1)
    try:
        status_code = r.status_code
    except:
        log.error('Error connecting to Nebula API.')
        log.error('Please try again later.')
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
        log.error(data['errors'])
        sys.exit(1)

    if status_code == 200:
        api_key = data['api_key']
        _init_conf_file(api_key)
        log.info('Login Successful!')
        return True
    else:
        log.error('Unexpected error. Login Failed.')


@require_api_key
def get_service_status(service_id, retry=False, max_retries=60):
    def _handle_output(status_code, data, retry):
        if status_code == 403:
            log.error(data)
            sys.exit(1)
        elif status_code == 404:
            log.error('We could not find a service with the given ID.')
            sys.exit(1)
        elif status_code == 500:
            log.error(data)
            sys.exit(1)
        elif status_code == 400:
            if retry:
                sys.stdout.write('\r{0}'.format('.' * ping))
                sys.stdout.flush()
            else:
                log.error(data)
                sys.exit(1)

        elif status_code == 200:
            log.info(data['success'])
            log.info('Connection string: ' + data['connection_string'])
            return True
        else:
            log.error('Unexpected Error.')
            sys.exit(1)

    try:
        url = _construct_url(STATUS, service_id=service_id)
        if retry:
            for ping in range(1, max_retries):
                status_code, data = _api_request(requests.get, url)
                done = _handle_output(status_code, data, retry)
                if done:
                    return True
                sleep(5)
            log.error('\nError: This seems to be taking longer than expected.')
            log.error('Please wait a few minutes and then check service status manually with "nebula status".')
        else:
            status_code, data = _api_request(requests.get, url)
            return _handle_output(status_code, data, retry)

    except KeyboardInterrupt:
        log.error('\nNOTE: You can still check the progress with the "nebula status" command.')
        sys.exit(1)


@require_api_key
def get_service(service, plan, platform, location):
    url = _construct_url(GET, service=service, plan=plan, platform=platform, location=location)
    status_code, data = _api_request(requests.get, url)
    if status_code != 200:
        log.error(data)
        sys.exit(1)

    service_id = data.get('id')

    if not service_id:
        log.error('Error: Could not retrieve Service ID from Nebula API')
        sys.exit(1)

    return service_id


@require_api_key
def destroy_service(service_id):
    url = _construct_url(DESTROY, service_id=service_id)
    status_code, data = _api_request(requests.delete, url)
    if status_code == 200:
        log.info(data)
        return True
    else:
        log.error(data)
        sys.exit(1)


@require_api_key
def list_services(all=False):
    ROW = "{0} : {1}"
    url = _construct_url(LIST)
    status_code, data = _api_request(requests.get, url)
    if status_code == 200:
        if not data.get('services'):
            log.info('No services found...')
        for service in data.get('services', []):
            if service.get('status') == 'running' or all:
                log.info(ROW.format('ID', service.get('service_id')))
                log.info(ROW.format('STATUS', service.get('status').upper()))
                log.info(ROW.format('PLAN', service.get('plan')))
                log.info(ROW.format('Connection String', service.get('description')))
                log.info(ROW.format('Started at', service.get('started_at')))
                log.info(ROW.format('Destroyed at', service.get('destroyed_at')))
                log.info("\n")
        return True
    else:
        log.error(data)
        sys.exit(1)
