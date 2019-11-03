import requests

def espn_authenticate(user, pwd):
        url_api_key = 'https://registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/api-key?langPref=en-US'
        url_login = 'https://ha.registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/guest/login?langPref=en-US'

        # Make request to get the API-Key
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url_api_key, headers=headers)
        if response.status_code != 200 or 'api-key' not in response.headers:
            print('Unable to access API-Key')
            print('Retry the authentication or continuing without private league access')
            return
        api_key = response.headers['api-key']

        # Utilize API-Key and login information to get the swid and s2 keys
        headers['authorization'] = 'APIKEY ' + api_key
        payload = {'loginValue': user, 'password': pwd}
        response = requests.post(url_login, headers=headers, json=payload)
        if response.status_code != 200:
            print('Authentication unsuccessful - check username and password input')
            print('Retry the authentication or continuing without private league access')
            return
        data = response.json()
        if data['error'] is not None:
            print('Authentication unsuccessful - error:' + str(data['error']))
            print('Retry the authentication or continuing without private league access')
            return
        return {
            "espn_s2": data['data']['s2'],
            "swid": data['data']['profile']['swid']
        }