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
