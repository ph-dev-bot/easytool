import json
import subprocess
import requests
import sys
import time


class Auth:

    def check_without_key():
        current_machine_id = str(subprocess.check_output(
            'wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        key_input = input("Enter your key: ")
        license_key = key_input
        API_KEY = ""
        url = "https://api.metalabs.io/v4/licenses/" + str(license_key)
        headers = {
            "Authorization": f"Bearer {API_KEY}"}
        response = requests.get(url, headers=headers)
        if response.text == "Not Found":
            print(f"This key doesn't exist")
            time.sleep(3)
            sys.exit()

        elif response.text == '{"error":{"message":"This API call cannot be made with a publishable API key. Please use a secret API key. You can find a list of your API keys at https://hyper.co/developers.","type":"invalid_request_error"}}':
            print(f"This key doesn't exist")
            time.sleep(3)
            sys.exit()

        else:
            headers = {
                'Authorization': f'Bearer {API_KEY}'
            }
            request = requests.get(
                f'https://api.hyper.co/v4/licenses/{license_key}', headers=headers).json()
            metadata = str(request['metadata'])
            if metadata == "{}":

                headers = {
                    'Authorization': f'Bearer {API_KEY}',
                    'Content-Type': 'application/json'
                }

                payload = {
                    'metadata': {
                        'hwid': current_machine_id
                    }
                }

                req = requests.patch(
                    f'https://api.hyper.co/v4/licenses/{license_key}', headers=headers, json=payload)
                if req.status_code == 200:
                    works = "yes"

                print(f'Your license is bound to this device now.')
                try:
                    with open("config/config.json", "r+") as jsonFile:
                        data = json.load(jsonFile)
                        data["key"] = license_key
                        jsonFile.seek(0)
                        json.dump(data, jsonFile)
                        jsonFile.truncate()
                except Exception as e:
                    print(f'Error changing key: {e}')

            else:
                metadata = str(request['metadata']['hwid'])

                if metadata == current_machine_id:
                    try:
                        with open("config/config.json", "r+") as jsonFile:
                            data = json.load(jsonFile)
                            data["key"] = license_key
                            jsonFile.seek(0)
                            json.dump(data, jsonFile)
                            jsonFile.truncate()
                    except Exception as e:
                        print(f'Error changing key: {e}')
                else:
                    print(f'You can only use 1 license per device.')
                    time.sleep(3)
                    sys.exit()

    def check_with_key(key):
        current_machine_id = str(subprocess.check_output(
            'wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

        API_KEY = ""
        url = "https://api.metalabs.io/v4/licenses/" + str(key)
        headers = {
            "Authorization": f"Bearer {API_KEY}"}

        response = requests.get(url, headers=headers)

        if response.text == "Not Found":
            print(f"This key doesn't exist")
            time.sleep(3)
            sys.exit()

        elif response.text == '{"error":{"message":"This API call cannot be made with a publishable API key. Please use a secret API key. You can find a list of your API keys at https://hyper.co/developers.","type":"invalid_request_error"}}':
            print(f"This key doesn't exist")
            time.sleep(3)
            sys.exit()

        else:
            headers = {
                'Authorization': f'Bearer {API_KEY}'
            }

            request = requests.get(
                f'https://api.hyper.co/v4/licenses/{key}', headers=headers).json()
            metadata = str(request['metadata'])

            if metadata == "{}":

                headers = {
                    'Authorization': f'Bearer {API_KEY}',
                    'Content-Type': 'application/json'
                }

                payload = {
                    'metadata': {
                        'hwid': current_machine_id
                    }
                }

                req = requests.patch(
                    f'https://api.hyper.co/v4/licenses/{key}', headers=headers, json=payload)
                if req.status_code == 200:
                    works = "yes"
                    print(f'Your license is bound to this device now.')

            else:
                metadata = str(request['metadata']['hwid'])
                if metadata == current_machine_id:
                    usertag = request['user']['discord']['tag']
                else:
                    print(f'You can only use 1 license per device.')
                    time.sleep(3)
                    sys.exit()

    def check():
        with open("config/config.json", "r") as jsonFile:
            data = json.load(jsonFile)

        if not data["key"]:
            Auth.check_without_key()
        else:
            Auth.check_with_key(data["key"])

    def getDiscordName():
        with open("../config/config.json", "r+") as jsonFile:
            data = json.load(jsonFile)
        headers = {
            'Authorization': f'Bearer '
        }

        req = requests.get(
            f'https://api.hyper.co/v6/licenses/{data["key"]}', headers=headers)
        if req.status_code == 200:
            pseudo = f"{req.json()['integrations']['discord']['username']}#{req.json()['integrations']['discord']['discriminator']}"
            return pseudo
        return None
