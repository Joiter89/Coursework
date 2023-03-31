from pprint import pprint
import requests
class VKUser:
    def __init__(self):
        self.token = input('Введите токен VK: ')
        self.vk_user_id = input('Введите свой ID пользователя VK: ')
        self.id_album = input("Введите ID альбома: ")
        self.count = input('Введите количество фотографий: ')
        self.dict_with_photo = {}
    def get_photo(self):
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.vk_user_id, 
                  'album_id': self.id_album,
                  'count': self.count,
                  'extended': 1,
                  'access_token': self.token,
                  'v': 5.131}
        res_get_photo = requests.get(URL, params=params).json()
        for k in res_get_photo['response']['items']:
            for l in k['sizes']:
                if l['type'] == 'x':
                    self.dict_with_photo[k['likes']['count']] = l['url']
        return
         
class YandexDisk():
    def __init__(self,poligon):
        self.poligon = poligon

    def get_headers(self):
        
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.poligon)
        }           
    
    def upload_file_to_disk(self, photo_dict, disk_file_path, url):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for key, val in photo_dict.items():
            params = {'path': f'{disk_file_path}/{key}.jpg','url': val}
            response = requests.post(upload_url, headers=headers, params=params)
        return response.json()
        

if __name__ == '__main__':
    vk = VKUser()
    vk.get_photo()
    ya = YandexDisk(poligon='')
    ya.upload_file_to_disk(vk.dict_with_photo, disk_file_path = 'Photo_VK', url = 'val')

    

    

