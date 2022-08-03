from distutils.log import Log
import requests
import json
from .base import Base
from utils import Proxyz, Logger


class zalandoSubscriber:
    def __init__(self, taskID, email, password, region, proxy):
        self.client = requests.session()
        self.email = email
        self.password = password
        self.region = region.lower()
        self.proxy = proxy.lower()
        self.taskID = taskID
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
                if response.json()['eligibility']["eligible"] == True:
                    if response.json()['ui']["showBillingAddressForm"] == True:
                        self._sendBillingForm()
                    else:
                        self._selectPaypal()
                else:
                    Logger.error(self.taskID, f"Not eligible to Zalando+ with {self.email}")


    

            elif response.status_code == 429:
                Logger.error(self.taskID, f"Rate Limit with {self.email}")
                self._isEligible()
            elif response.status_code == 502 or response.status_code == 503:
                Logger.error(self.taskID, f"Proxy error with {self.email}")
                self._isEligible()
        except:
            Logger.error(
                self.taskID, f"Error while checking eligibility with {self.email}")

    def _sendBillingForm(self):
        pass
    def _getCsrf(self):
        pass

    def _selectPaypal(self):
        pass

    def _subscribe(self):
        pass

    def start(self):
        Base._login(self)
        self._isEligible()
