import os
import requests


# définition de l'adresse de l'API
api_address = os.environ.get("API_ADRESS")
# port de l'API
api_port = os.environ.get("API_PORT")

# définition de l'username
api_username = os.environ.get("USER_NAME").split(':')
# définition du mot de passe
api_password = os.environ.get("PASSWORD").split(':')
# définition du resultat attendu
expected_result = os.environ.get("EXPECTED_RESULT").split(':')
# Fichier de test en CSV
files = {"file": open("./csv_files/test_raw.csv")}
# Réponse attendue
output_expected = [{'2010-10-21/Sydney': 'No'}, {'2010-10-22/Sydney': 'No'}]


# itération pour les tests d'authentification
for username, password, expected in zip(api_username, api_password, expected_result):
    # requête
    r_token = requests.post(
        url=f'http://{api_address}:{api_port}/api/v1/login/access-token',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data= {
            'username': f'{username}',
            'password': f'{password}',
        }
    )  
    token = r_token.json()["access_token"]
    
    r = requests.post(
        url=f'http://{api_address}:{api_port}/api/v1/predict/raw?models=gbc',
        headers={'Authorization': f'Bearer {token}'},
        files=files,
    )   
    
    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if (
        (status_code == int(expected)) 
        and (output_expected == r.json()["data"][:2])
    ):
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    # Affichage du test
    output = f'''
============================
    Predict raw csv test
============================

request done at "/api/v1/predict/raw?models=gbc"
| username="{username}"
| password="{password}"
| model="gbc (Gradient Boosing Classifier)"

expected status code = {expected}
actual status code = {status_code}

expected output = {output_expected}
actual output = {r.json()["data"][:2]}

==>  {test_status}

    '''
    print(output)
    
    # impression dans un fichier
    if os.environ.get('LOG') == '1':
        with open('./log/predict_model_raw_csv_test.log', 'a') as file:
            file.write(output)
