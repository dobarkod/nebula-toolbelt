
def _construct_url(action, service=None, service_id=None, plan=None):
    apis = {
        GET: NEBULA_API_URL +
            '{0}/get/service/{1}-{2}/'.format(API_KEY, service, plan),
        PROVISIONING_STATUS: NEBULA_API_URL +
            '{0}/service/{1}/status/'.format(API_KEY, service_id)
    }
    return apis[action]
