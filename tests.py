import unittest
import tempfile

from nebula import api
from nebula import conf

api.NEBULA_API_URL = 'http://testserver/api/v1/'
api.API_KEY = 'testkey'


class TestConfig(unittest.TestCase):

    def test_config_file_initialize(self):
        with tempfile.NamedTemporaryFile(mode='rw') as f:
            conf.CONFIG = f.name
            conf._init_conf_file('test_api_key')
            self.assertEquals('API_KEY=test_api_key', f.read())

    def test_getting_api_key_from_config_file(self):
        with tempfile.NamedTemporaryFile(mode='rw') as f:
            conf.CONFIG = f.name
            conf._init_conf_file('test_api_key')

            ret = conf._get_api_key()
            self.assertEquals(ret, 'test_api_key')


class TestAPICalls(unittest.TestCase):

    def test_constructing_login_url(self):
        self.assertEquals('http://testserver/api/v1/login/', api._construct_url(api.LOGIN))

    def test_constructing_get_service_url(self):
        url = api._construct_url(
            action=api.GET,
            service='testservice',
            plan='testplan',
            platform='testplatform')
        self.assertEquals(
            url,
            'http://testserver/api/v1/testkey/get/service/testservice-testplan/testplatform/')

    def test_constructing_destroy_service_url(self):
        url = api._construct_url(
            action=api.DESTROY,
            service_id='testid')
        self.assertEquals(
            url,
            'http://testserver/api/v1/testkey/destroy/service/testid/')

    def test_constructing_status_url(self):
        url = api._construct_url(
            action=api.STATUS,
            service_id='testid')
        self.assertEquals(
            url,
            'http://testserver/api/v1/testkey/service/testid/status/')

    def test_constructing_list_url(self):
        url = api._construct_url(
            action=api.LIST,
            service_id='testid')
        self.assertEquals(
            url,
            'http://testserver/api/v1/testkey/my/services/')

    def test_getting_new_service(self):

        def fake_api_request(method, url, **kwargs):
            return (200, {'id': 1})
        api._api_request = fake_api_request

        result = api.get_service(
            service='testservice',
            plan='testplan',
            platform='testplatform')
        self.assertEquals(1, result)

    def test_getting_new_service_no_id_returned_from_api_server(self):

        def fake_api_request(method, url, **kwargs):
            return (200, {})
        api._api_request = fake_api_request

        params = {
            'service': 'testservice',
            'plan': 'testplan',
            'platform': 'testplatform'
        }

        self.assertRaises(
            SystemExit,
            api.get_service,
            **params)

    def test_getting_new_service_fail_status_code(self):

        def fake_api_request(method, url, **kwargs):
            return (400, {})
        api._api_request = fake_api_request

        params = {
            'service': 'testservice',
            'plan': 'testplan',
            'platform': 'testplatform'
        }

        self.assertRaises(
            SystemExit,
            api.get_service,
            **params)

    def test_destroying_a_service(self):

        def fake_api_request(method, url, **kwargs):
            return (200, {})
        api._api_request = fake_api_request

        result = api.destroy_service('test_id')
        self.assertTrue(result)

    def test_destroying_a_service_fail_status_code(self):

        def fake_api_request(method, url, **kwargs):
            return (400, {})
        api._api_request = fake_api_request

        params = {
            'service_id': 'test_id',
        }

        self.assertRaises(
            SystemExit,
            api.destroy_service,
            **params)

    def test_list_services_fail_status_code(self):

        def fake_api_request(method, url, **kwargs):
            return (400, {})
        api._api_request = fake_api_request

        self.assertRaises(
            SystemExit,
            api.list_services)

        # with the 'all' flag
        self.assertRaises(
            SystemExit,
            api.list_services,
            all=True)

    def test_list_services(self):

        def fake_api_request(method, url, **kwargs):
            return (200, {})
        api._api_request = fake_api_request

        result = api.list_services()
        self.assertTrue(result)
        result = api.list_services(all=True)
        self.assertTrue(result)

    def test_getting_service_status(self):

        def fake_api_request(method, url, **kwargs):
            return (200, {'success': None, 'connection_string': ''})
        api._api_request = fake_api_request

        result = api.get_service_status('test_id')
        self.assertTrue(result)

    def test_getting_service_status_403(self):

        def fake_api_request(method, url, **kwargs):
            return (404, {})
        api._api_request = fake_api_request

        self.assertRaises(
            SystemExit,
            api.get_service_status,
            service_id='test_id')

    def test_getting_service_status_404(self):

        def fake_api_request(method, url, **kwargs):
            return (404, {})
        api._api_request = fake_api_request

        self.assertRaises(
            SystemExit,
            api.get_service_status,
            service_id='test_id')

    def test_getting_service_status_500(self):

        def fake_api_request(method, url, **kwargs):
            return (404, {})
        api._api_request = fake_api_request

        self.assertRaises(
            SystemExit,
            api.get_service_status,
            service_id='test_id')


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
