import io
import json
import shutil

import requests
import datetime
import os
from cutter import with_moviepy


class CoubHtmlVideoIMG:

    def __init__(self, coub_id=None, json_data=None):

        if coub_id is not None and json_data is not None:
            raise Exception('Only one argument (ID or json_data) expected')

        elif coub_id is not None:
            response = requests.get(f'https://coub.com/api/v2/coubs/{coub_id}')
            json_data = json.loads(response.text)
            self.__ID = json_data['permalink']['video']
            self.__relevance = datetime.datetime.today()

        elif json_data is not None:
            self.__ID = json_data['permalink']

        self.__html5_json = json_data['file_versions']['html5']['video']

        self.__url_higher = self.__html5_json['higher']['url']
        self.__url_high = self.__html5_json['high']['url']
        self.__url_med = self.__html5_json['med']['url']

        self.__size_higher = self.__html5_json['higher']['size']
        self.__size_high = self.__html5_json['high']['size']
        self.__size_med = self.__html5_json['med']['size']

    def get_url_higher(self):
        return self.__url_higher

    def get_url_high(self):
        return self.__url_high

    def get_url_med(self):
        return self.__url_med

    def get_size_higher(self):
        return self.__size_higher

    def get_size_high(self):
        return self.__size_high

    def get_size_med(self):
        return self.__size_med

    def get_relevance(self):
        return self.__relevance

    def get_id(self):
        return self.__ID


class CoubHtmlAudioIMG:

    def __init__(self, coub_id=None, json_data=None):

        if coub_id is not None and json_data is not None:
            raise Exception('Only ona argument (ID or json_data) expected')

        elif coub_id is not None:
            response = requests.get(f'https://coub.com/api/v2/coubs/{coub_id}')
            json_data = json.loads(response.text)
            self.__ID = json_data['permalink']['video']
            self.__relevance = datetime.datetime.today()

        elif json_data is not None:
            self.__ID = json_data['permalink']

        self.__html5_json = json_data['file_versions']['html5']['audio']

        self.__url_high = self.__html5_json['high']['url']
        self.__url_med = self.__html5_json['med']['url']

        self.__size_high = self.__html5_json['high']['size']
        self.__size_med = self.__html5_json['med']['size']

    def get_url_high(self):
        return self.__url_high

    def get_url_med(self):
        return self.__url_med

    def get_size_high(self):
        return self.__size_high

    def get_size_med(self):
        return self.__size_med

    def get_relevance(self):
        return self.__relevance

    def get_id(self):
        return self.__ID


class CoubDataObject:

    def __init__(self, coub_id=None, json_data=None):
        super().__init__()
        self.__ID = coub_id
        self.__relevance = None

        if coub_id is not None and json_data is not None:
            raise Exception('Only ona argument (ID or json_data) expected')

        elif coub_id is not None:
            response = requests.get(f'https://coub.com/api/v2/coubs/{coub_id}')
            self.__json_data = json.loads(response.text)
            self.__ID = self.__json_data['permalink']
            self.__relevance = datetime.datetime.today()

        elif json_data is not None:
            self.__json_data = json_data
            self.__ID = self.__json_data['permalink']

        date_template = '%Y-%m-%dT%H:%M:%S%z'

        self.__recoub = self.__json_data['recoub']
        self.__title = self.__json_data['title']
        self.__visibility_type = self.__json_data['visibility_type']
        self.__original_visibility_type = self.__json_data['original_visibility_type']
        self.__channel_id = int(self.__json_data['channel_id'])
        self.__created_at = datetime.datetime.strptime(self.__json_data['created_at'], date_template)
        self.__updated_at = datetime.datetime.strptime(self.__json_data['updated_at'], date_template)
        self.__views_count = int(self.__json_data['views_count'])
        self.__featured = self.__json_data['featured']
        self.__published = self.__json_data['published']
        self.__published_at = datetime.datetime.strptime(self.__json_data['published_at'], date_template)
        self.__reversed = self.__json_data['reversed']

        self.__audio_copyright_claim = self.__json_data['audio_copyright_claim']

        self.html_video = CoubHtmlVideoIMG(json_data=self.__json_data)

        if self.__audio_copyright_claim is None:
            self.html_audio = CoubHtmlAudioIMG(json_data=self.__json_data)
        else:
            self.html_audio = None

    def get_relevance(self):
        return self.__relevance

    def get_id(self):
        return self.__ID

    def get_title(self):
        return self.__title

    def get_visibility(self):
        return self.__visibility_type

    def get_channel_id(self):
        return self.__channel_id

    def get_creation_time(self):
        return self.__created_at

    def get_updating_time(self):
        return self.__updated_at

    def get_views_count(self):
        return self.__views_count

    def get_export_json(self):
        return self.__json_data.copy()

    def is_featured(self):
        return self.__featured

    def is_published(self):
        return self.__published

    def get_publishing_time(self):
        return self.__published_at


# print(json.dumps(jsn, indent=3))
# print(CDO.html_video.get_url_higher())

# print(jsn['permalink'])
# print(jsn['title'])
# print(jsn['channel'])
# print(jsn['communities'])
# print(jsn['tags'])
if __name__ == '__main__':
    files = tuple(map(lambda a: a.replace('.mp4', '').replace('.mp3', ''), os.listdir(r'K:\Coubs\ilya-pro')))
    files_total_count = len(files)
    files_cur_count = 0

    save_dir = 'K:\\CoubData\\'

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    for ID in files:
        files_cur_count += 1

        audio_exists = os.path.exists(os.path.join(save_dir, ID, 'audio.mp3'))
        time_exists = os.path.exists(os.path.join(save_dir, ID, 'time.txt'))
        json_exists = os.path.exists(os.path.join(save_dir, ID, 'data.json'))

        if not os.path.exists(os.path.join(save_dir, ID)):
            os.mkdir(os.path.join(save_dir, ID))

        if not (audio_exists and time_exists and json_exists):
            print(f'[{files_cur_count}/{files_total_count}]', ID)
            jsn = json.loads(requests.get(f'https://coub.com/api/v2/coubs/{ID}').text)

            if not audio_exists:
                if 'higher' in jsn['file_versions']['html5']['audio']:
                    aud_url = jsn['file_versions']['html5']['audio']['higher']['url']

                elif 'high' in jsn['file_versions']['html5']['audio']:
                    aud_url = jsn['file_versions']['html5']['audio']['high']['url']

                else:
                    aud_url = jsn['file_versions']['html5']['audio']['med']['url']

                response = requests.get(aud_url)
                with open("response.mp3", "wb") as f:
                    f.write(response.content)

                shutil.move("response.mp3", os.path.join(save_dir, ID, 'audio.mp3'))
                print('Audio added')

            if not time_exists:
                if 'med' in jsn['file_versions']['html5']['video']:
                    vid_url = jsn['file_versions']['html5']['video']['med']['url']

                elif 'high' in jsn['file_versions']['html5']['video']:
                    vid_url = jsn['file_versions']['html5']['video']['high']['url']

                else:
                    vid_url = jsn['file_versions']['html5']['video']['higher']['url']

                response = requests.get(vid_url)
                with open("response.mp4", "wb") as f:
                    f.write(response.content)

                time = round(with_moviepy("response.mp4")[0] - 0.05, 2)
                with open('time.txt', 'w+') as f:
                    f.write(str(time))

                shutil.move("time.txt", os.path.join(save_dir, ID, 'time.txt'))
                print('Time added', with_moviepy("response.mp4")[0], time)

            if not json_exists:
                json_object = json.dumps(jsn, indent=4)
                with open(os.path.join(save_dir, ID, 'data.json'), "w", encoding='utf-8') as outfile:
                    outfile.write(json_object)

                print('Json data added')
