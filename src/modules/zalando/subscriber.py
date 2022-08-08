from distutils.log import Log
import requests
import json
from .base import Base
from utils import Proxyz, Logger
import sys


class zalandoSubscriber:
    def __init__(self, taskID, email, password, region, firstname, lastname, street, zipcode, city, proxy):
        self.client = requests.session()
        self.email = email
        self.password = password
        self.region = region.lower()
        self.proxy = proxy.lower()
        self.taskID = taskID
        self.firstname = firstname
        self.lastname = lastname
        self.street = street
        self.zip = str(zipcode)
        self.city = city
        self.start()

    def _isEligible(self):
        try:
            headers = {
                'authority': f'www.zalando.{self.region}',
                'accept': '*/*',
                'accept-language': 'fr-FR,fr;q=0.9',
                'dpr': '1.1',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'viewport-width': '1631',
                'x-kl-ajax-request': 'Ajax_Request',
            }
            params = {
                'context': 'MEMBERSHIP_AREA',
                'flow': '',
                'checkoutId': '',
                'promiseId': '',
            }
            response = self.client.get('https://www.zalando.fr/api/plus/membership-fragment/subscription/form/OVERLAY',

                                       params=params, headers=headers, proxies=Proxyz.randomProxy(self))

            if response.status_code == 200:
                try:
                    if response.json()['eligibility']["eligible"] == True:
                        if response.json()['ui']["showBillingAddressForm"] == True:
                            print("True")
                            print(response.text)
                            # self._sendBillingForm()
                            pass
                        else:
                           # self._selectPaypal()
                            print("False")
                            pass
                    else:
                        Logger.error(
                            self.taskID, f"Not eligible to Zalando+ with {self.email}")
                        sys.exit(1)
                except Exception as e:
                    print(e)
                    Logger.error(
                        self.taskID, f"Not eligible to Zalando+ with {self.email}")
                    sys.exit(1)
            elif response.status_code == 429:
                Logger.error(self.taskID, f"Rate Limit with {self.email}")
                self._isEligible()
            elif response.status_code == 502 or response.status_code == 503:
                Logger.error(self.taskID, f"Proxy error with {self.email}")
                self._isEligible()
        except Exception as e:
            print(e)
            Logger.error(
                self.taskID, f"Error while checking eligibility with {self.email}")

    def _sendBillingForm(self):
        try:
            csrf = Base._getCSRF(self)
            headers = {
                'Host': f'www.zalando.fr',
                'authority': 'www.zalando.fr',
                'accept': '*/*',
                'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                'dpr': '1',
                'origin': f'https://www.zalando.{self.region}',
                'referer': f'https://www.zalando.{self.region}/membership/area/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
                'viewport-width': '2563',
                'x-xsrf-token': csrf,
            }

            json_data = {
                'address': {
                    'gender': 'MALE',
                    'firstName': self.firstname,
                    'lastName': self.lastname,
                    'street': self.street,
                    'zip': self.zip,
                    'city': self.city,
                },
            }
            response = self.client.post(
                'https://www.zalando.fr/api/plus/membership-fragment/subscription/billing-address', headers=headers, json=json_data)
            print(response.text)
            print(response.status_code)

            if response.status_code == 200:
                Logger.normal(
                    self.taskID, f"Successfully send billing info with {self.email}")
                self._selectPaypal()
            elif response.status_code == 400:
                Logger.error(
                    self.taskID, f"Bad Adress with {self.email}")
                sys.exit(1)
            elif response.status_code == 502 or response.status_code == 503 or response.status_code == 500:
                Logger.error(
                    self.taskID, f"Bad Proxy with {self.email}")
                self._sendBillingForm()
            else:
                Logger.error(self.taskID, f"Error with {self.email}")
                sys.exit(1)
        except Exception as e:
            print(e)
            Logger.error(
                self.taskID, f"Error while checking caca with {self.email}")
            sys.exit(1)

    def _selectPaypal(self):
        pass

    def _subscribe(self):
        pass

    def start(self):
        Base._login(self)
        self._isEligible()
        # self._sendBillingForm()
