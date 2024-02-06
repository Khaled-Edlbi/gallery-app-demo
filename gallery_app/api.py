from django_project.settings import client_id, client_secret
import requests


def check_token(access_token):

    url = "https://api.imgur.com/3/feed"

    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        response = requests.request("GET", url, headers=headers)
        return response.json()

    except requests.RequestException as e:
        return {'success': False, 'data': {'error': str(e)}}


def get_new_token(refresh_token):

    url = "https://api.imgur.com/oauth2/token"

    payload = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.request("POST", url, data=payload)
        return response.json()

    except requests.RequestException as e:
        return {'success': False, 'data': {'error': str(e)}}
