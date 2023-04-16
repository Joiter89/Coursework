from pprint import pprint
import json
import requests
import configparser

class VKUser:
    def __init__(self):
        self.token = config['DEFAULT']['VK_TOKEN']
        self.vk_user_id = input('Введите свой ID пользователя VK или короткое имя (screen_name): ')
        self.id_album = input("Введите ID альбома: ")
        self.count = input('Введите количество фотографий: ')
        self.dict_with_photo = {}

    def get_photo(self):
        URL = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': self.vk_user_id,
                  'v': 5.131}
        user = requests.get(URL, params=params).json()
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user['response'][0]['id'], 
                  'album_id': self.id_album,
                  'count': self.count,
                  'extended': 1,
                  'access_token': self.token,
                  'v': 5.131}
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        res_get_photo = requests.get(URL, params=params).json()
        for file in res_get_photo['response']['items']:
            file_url = max(file['sizes'], key=lambda x: vk_sizes[x['type']])
            if file['likes']['count'] in self.dict_with_photo.keys():
                self.dict_with_photo[f"{file['likes']['count']}_{file['date']}"] =  file_url['url']
            else:
                self.dict_with_photo[file['likes']['count']] =  file_url['url']
        return
    
    def get_json(self, file):
        with open('result_json.json', 'w') as f:
            json.dump(file,f, ensure_ascii=False, indent=2)
         
class YandexDisk():
    def __init__(self, poligon):
        self.poligon = poligon
    
    def get_headers(self):
        
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.poligon)
        }           
    

    def upload_file_to_disk(self, dict_with_photo, folder_name):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for name, size in dict_with_photo.items():
            params = {'path': f'{folder_name}/{name}.jpg','url': size}
            response = requests.post(upload_url, headers=headers, params=params)   
        if response.status_code == 202:
            print('Фотографии загружены')
        else:
            print('Произошла ошибка')    
        

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    config.sections()
    poligon = config['DEFAULT']['POLIGON_YA']
    folder_name = 'VK'
    vk = VKUser()
    vk.get_photo()
    vk.get_json(vk.dict_with_photo)
    ya = YandexDisk(poligon=poligon)
    ya.upload_file_to_disk(vk.dict_with_photo, folder_name)


    

    

