import requests
from runt_rover.comms.state import State

state = State()

class ConnectionClient():

    @staticmethod
    def connect_to_http_host(host_address):
        '''
        Attempts to establish an HTTP connection to the base station server. The
        'connection' is an abstraction on top of the HTTP requests, which allows the
        base station to be aware of the history of HTTP requests between the rover
        and base station.
        '''
        assert(type(host_address)) == str

        try:
            request_url = '{}/connect'.format(host_address)
            response = requests.get(request_url)
            assert response.status_code == 200
        except AssertionError as err:
            pass

        json_data = response.json()
        state.set_attribute('connection_established', True)
        state.set_attribute('connection_remote_addr', host_address)
        state.set_attribute('connection_id', json_data['connection_id'])

    @staticmethod
    def send_telemetry(data):
        '''
        Sends telemetry data to the base station, if a connection exists
        '''
        assert(type(data)) == dict

        if not state.get_attribute('connection_established'):
            return False # TODO raise exception?

        try:
            request_url = '{}/send_telemetry'.format(state.get_attribute('connection_remote_addr'))
            response = requests.post(request_url, json=data)
            assert response.status_code == 200
        except AssertionError as err:
            pass

    @staticmethod
    def disconnect_from_http_host():
        '''
        Disconnects from the base station server. This indicates to the rover that the
        base station is not actively processing requests from the rover.
        '''

        if not state.get_attribute('connection_established'):
            return False # TODO raise exception?

        try:
            request_url = '{}/disconnect'.format(state.get_attribute('connection_remote_addr'))
            response = requests.get(request_url)
            assert response.status_code == 200
        except AssertionError as err:
            pass

        state.set_attribute('connection_established', False)
        state.set_attribute('connection_remote_addr', None)
        state.set_attribute('connection_id', None)