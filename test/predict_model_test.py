import os
import requests
import json

# définition de l'adresse de l'API
api_address = os.environ.get('API_ADRESS')

# port de l'API
api_port = os.environ.get('API_PORT')

# emplacement du fichier de log
api_log_dir = os.environ.get('API_LOG_DIR')

def unit_test(n, username, password, data, model, response_expected, output_expected=None, file_log=False):

    #Authentication
    r = requests.post(
        url=f'http://{api_address}:{api_port}/api/v1/login/access-token',
        data= {
            'grant_type': 'password',
            'username':username,
            'password':password
        }
    )
    token = json.loads(r.text)['access_token']
    
    #Request
    r = requests.post(
        url=f'http://{api_address}:{api_port}/api/v1/predict?models={model}',
        headers={'Authorization': f'Bearer {token}'},
        json={'data':data}
    )
    
    test_status = 'FAILURE'
    if response_expected==r.status_code:
        if output_expected is None:
            test_status = 'SUCCESS'
        elif output_expected==json.loads(r.text):
            test_status = 'SUCCESS'
    
    output = f'''
    ============================
            Predict test {n}
    ============================

    request done at "/api/v1/predict/{model}"
    | username="{username}"
    | password="{password}"
    | data= (next lines)
    "{data}"

    expected status code = {response_expected}
    actual status code = {r.status_code}
    
    expected output = {output_expected}
    actual output = {r.text}

    ==>  {test_status}

    '''

    print(output)

    # impression dans un fichier
    if file_log:
        with open(api_log_dir + '/api_test.log', 'a') as file:
            file.write(output)

file_log = (os.environ.get('LOG') == str(1))

unit_test(1, 'alice', 'wonderland', 
          [["2010-08-23","Melbourne",6.1,17.1,0.0,3.2,5.8,"N",52.0,"N","NNW",28.0,26.0,59.0,41.0,1014.4,1010.7,3.0,7.0,10.5,15.4,"No"]],
          'gbc',
          200,
          {"RainTomorrow": [["2010-08-24","Melbourne","Yes"]]},
          file_log)

unit_test(2, 'alice', 'wonderland', 
          [
              ["2010-08-23","Melbourne",6.1,17.1,0.0,3.2,5.8,"N",52.0,"N","NNW",28.0,26.0,59.0,41.0,1014.4,1010.7,3.0,7.0,10.5,15.4,"No"],
              ["2010-09-23","Melbourne",10.9,16.2,0.0,1.6,2.1,"SW",33.0,"SW","WSW",22.0,19.0,61.0,51.0,1027.1,1025.0,7.0,7.0,12.4,15.3,"No"]
          ],
          'gbc',
          200,
          {"RainTomorrow": 
            [
              ["2010-08-24","Melbourne","Yes"],
              ["2010-09-24","Melbourne","No"]
            ]
          },
          file_log)

