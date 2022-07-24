import random


class Prox:
    def randomProxy():
        try:
            lisT = []
            filename = 'config/proxies.txt'
            with open(filename, 'r', encoding="utf-8") as file:
                for line in file:
                    line = line.rstrip("\n")
                    ip = line.split(":")[0]
                    port = line.split(":")[1]
                    user = line.split(":")[2]
                    mdp = line.split(":")[3]
                    goodFormat = f'{user}:{mdp}@{ip}:{port}'
                    proxyDict = {
                        'http': f'http://{goodFormat}',
                        'https': f'https://{goodFormat}'
                    }
                    lisT.append(proxyDict)
            if len(lisT) == 0:
                print("No proxies Loaded!")
                return
            else:
                return random.choice(lisT)
        except:
            print("Error in your proxies file! Check and restart!")
            return
