import os
import requests


# définition de l'adresse de l'API
api_address = "fastapi"
# port de l'API
api_port = 8000

# définition de l'username
api_username = os.environ.get("USER_NAME").split(':')
# définition du mot de passe
api_password = os.environ.get("PASSWORD").split(':')
# définition du resultat attendu
expected_result = os.environ.get("EXPECTED_RESULT").split(':')

# itération pour les tests d'authentification
for username, password, expected in zip(api_username, api_password, expected_result):
    # requête
    r = requests.post(
        url=f'http://{api_address}:{api_port}/api/v1/login/access-token',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data= {
            'username': f'{username}',
            'password': f'{password}',
        }
)

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == int(expected):
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    # Affichage du test
    output = f'''
    ============================
        Authentication test
    ============================

    request done at "/permissions"
    | username="{username}"
    | password="{password}"

    expected result = {expected}
    actual restult = {status_code}

    ==>  {test_status}

    '''
    print(output)
    
    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('./log/authentication_test.log', 'a') as file:
            file.write(output)
