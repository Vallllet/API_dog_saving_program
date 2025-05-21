import requests
import json
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class Dog:
    def __init__(self, breed = (input("Enter breed's name:")).lower()):
        self.breed = breed
        self.base_url = 'https://dog.ceo/api/breed'

    def save_random_dog(self):
        logging.info('Started')
        self.responce = requests.get(self.base_url+f'/{self.breed}/'+'images/random')
        self.image_url = self.responce.json()['message']
        self.filename = self.image_url.split('/')[-1]
        self.dog = self.breed + '_' + self.image_url.split('/')[-1]
        yd1.create_folder()
        dog1.get_subbreed()

    def get_subbreed(self):
        self.check = requests.get(self.base_url+'s/list/all').json()
        report = 'load_report' + time.strftime('%Y%m%d%H%M%S')
        with open (f'{report}.json', 'w') as f:
            data = []
            json.dump(data, f, indent=2)
        with open (f'{report}.json', 'r') as f:
            loads = json.load(f)
            if len(self.check['message'][dog1.breed]) > 0:
                self.subbreeds = self.check['message'][dog1.breed]
                for self.subbreed in self.subbreeds:
                    self.image_subbreed_url = (requests.get(self.base_url + f'/{self.breed}/{self.subbreed}/'
                                                            + 'images/random').json())['message']
                    self.dog = self.breed + '_' + self.subbreed + '_' + self.image_subbreed_url.split('/')[-1]
                    yd1.save_dog_with_subbreeds()
                    data1 = {'file_name': self.dog}
                    loads.append(data1)
            else:
                yd1.save_dog_image()
                data1 = {'file_name': self.dog}
                loads.append(data1)
        with open(f'{report}.json', 'w') as f:
            json.dump(loads, f, indent = 2)
        logging.info('Finished')

class YD:
    def __init__(self):
        # Ниже — пример использования из моей программы изначально, но пользователь должен вводить токен, так что...
        # config = configparser.ConfigParser()
        # config.read('settings.ini')
        # self.token = config['Tokens']['yd_token']
        self.token = input('Enter OAuth-token from "Полигон Яндекс Диска":')
        self.headers = {
            'Authorization': f'OAuth {self.token}'
        }
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self):
        creation = requests.put(f'{self.base_url}?path=dogs/{dog1.breed}', headers=self.headers)
        trying = creation.status_code
        if trying == 401:
            logging.error('OAuth token is invalid or not found')
            sys.exit('Running is Failed')


    def save_dog_image(self):
        saving = requests.post(f'{self.base_url}/upload?url={dog1.image_url}&path=dogs/{dog1.breed}/{dog1.dog}',
                               headers=self.headers)
        if saving.status_code == 409:
            logging.warning('1 photo already in collection')
        if saving.status_code == 202:
            logging.info('1 photo is saved')

    def save_dog_with_subbreeds(self):
        saving = requests.post(f'{self.base_url}/upload?url={dog1.image_subbreed_url}&path=dogs/{dog1.breed}/{dog1.dog}',
                               headers=self.headers)
        if saving.status_code == 409:
            logging.warning('1 photo already in collection')
        if saving.status_code == 202:
            logging.info('1 photo is saved')


dog1 = Dog()
yd1 = YD()

dog1.save_random_dog()






