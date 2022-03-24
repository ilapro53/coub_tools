import os
import re
import time


def parallel_clean(dir):
    lst = os.listdir(dir)

    def copies_list(fdir):
        cpl = []
        for i in os.listdir(fdir):
            if bool(re.fullmatch(r'.* \(.*\).mp4', i)):
                cpl.append(i)

        return cpl


    while True:
        first_cache = copies_list(dir)

        print('Waiting for changes...')
        while first_cache == copies_list(dir):
            time.sleep(1)

        print('Replacing...')
        for item in first_cache:
            name = item.split(' ')[0]

            try:
                os.replace(os.path.join(f'{dir}', f'{item}'),
                           os.path.join(f'{dir}', f'{name}.mp4'))
                print(f'{item}', '->', f'{name}.mp4')

            except FileNotFoundError:
                print('Not found:', f'{item}')



if __name__ == "__main__":
    parallel_clean(r'K:\Coubs\musecollexion')