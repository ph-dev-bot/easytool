import os
import csv
import glob
import json


class Files:
    def check_TasksDirectory():
        path = 'Tasks/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        
        ##CHECK ZALANDO DIRECTORY
        path = 'Tasks/zalando'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

        ##CHECK ZALANDO TASKS.CSV
        extension = 'csv'
        os.chdir(path)
        result = glob.glob('*.{}'.format(extension))
        if len(result) == 0:
            data = ['mode', 'email', 'password', 'country', 'newPassword', 'city', 'cityCode', 'address', 'useProxy']
            with open('tasks.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                f.close()


        newPath = '../Results/'
        isExist = os.path.exists(newPath)
        if not isExist:
            os.makedirs(newPath)

        extension = 'csv'
        os.chdir(newPath)
        result = glob.glob('*.{}'.format(extension))
        if len(result) == 0:
            data = ['email', 'password', 'link']
            with open('../Results/success.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            data = ['email', 'password', 'reason']
            with open('../Results/failed.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)

    def check_Config():
        path = 'config/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

        path = 'config/proxies.txt'
        isExist = os.path.exists(path)
        if not isExist:
            with open('config/proxies.txt', 'w', encoding='UTF8') as f:
                pass

        path = 'config/config.json'
        isExist = os.path.exists(path)
        if not isExist:
            data = {"webhook": "", "key": "", "delay": ""}
            with open('Config/config.json', 'w') as f:
                json.dump(data, f, indent=2)
