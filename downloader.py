import uuid

from yt_dlp import YoutubeDL


def download_video(url, mes):

    name = f'{uuid.uuid4().hex}.mp4'
    opts = {'format': 'bv*[ext=mp4]+ba[ext=m4a]', 'outtmpl': name} #'progress_hooks': [my_hook]
    with YoutubeDL(opts) as yt:
        err = yt.download([url])
        if err:
            print(f'some errors: {err}')
    return name