import requests
import json
from utils import Proxyz, Logger
import sys


class Base:
    def _login(self):
        try:
            Logger.normal(self.taskID, f"Try to login with {self.email}")
            payload = json.dumps({
                "password": self.password,
                "email": self.email,
            })
            headers = {
                'Host': f'www.zalando.{self.region}',
                'x-ts': '1657206656338',
                'x-sig': 'e23be00d3bb326342925745937965fa35eac6c54',
                'User-Agent': 'zalando/22.8.0 (iPhone; iOS 15.1; Scale/2.00)',
                'x-logged-in': 'false',
                'x-device-type': 'smartphone',
                'x-frontend-type': 'mobile-app',
                'x-zalando-mobile-app': '3580f92a4bafb890i',
                'x-device-os': 'ios',
                'x-os-version': '15.1',
                'x-app-domain': '11',
                'x-device-platform': 'ios',
                'Accept-Language': '*',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            response = self.client.post("https://glados.fashion-store.zalan.do/api/mobile/v3/user/login.json",
                                        headers=headers, data=payload, proxies=Proxyz.randomProxy(self))

            if response.status_code == 200:
                if response.json()["successful"] == True:
                    Logger.mid(self.taskID,
                               f"Successful logged with {self.email}")
                if response.json()["successful"] == False:
                    Logger.error(
                        self.taskID, f"Failed to login with {self.email}")
                    sys.exit(1)
            else:
                Logger.error(self.taskID, f"Loggin Error with {self.email}")
                sys.exit(1)
        except Exception as e:
            Logger.error(self.taskID, f"Error with {self.email}")
            sys.exit(1)

    def _getCSRF(self):
        try:
            Logger.normal(self.taskID, f"Getting csrf token with {self.email}")
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'fr-FR',
                'Connection': 'keep-alive',
                'Origin': f'https://www.zalando.{self.region}',
                'Referer': f'https://www.zalando.{self.region}/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            response = self.client.get(f"https://m.zalando.{self.region}",
                                       headers=headers, proxies=Proxyz.randomProxy(self))
            if response.status_code == 200:
                for cookie in self.client.cookies:
                    if cookie.name == "frsx":
                        xsrf = cookie.value
                return xsrf
            elif response.status_code == 502 or response.status_code == 503:
                Logger.error(self.taskID, f"Proxy Error with {self.email}")
                self._getCSRF()
            else:
                Logger.error(self.taskID, f"Error with {self.email}")
                sys.exit(1)
        except Exception as e:
            Logger.error(self.taskID, f"Error with {self.email}")
            self._getCSRF()
