import os
from pyrogram import Client
from downloader import download_video
from config import api_hash, api_id

print(api_hash)
print(api_id)
app = Client("my_account", api_id=api_id, api_hash=api_hash)


def register():
    app.run()


async def upload_video(url, mes):
    old = [None]

    async def progress(current, total):
        prog = int(current * 100 / total)
        # prog = f"{current * 100 / total:.1f}%"
        if prog != old[0]:
            await mes.edit_text(f'{prog}%')
            old[0] = prog
            print(prog)

    async with app:
        video_name = download_video(url, mes)
        video = await app.send_video('ytvd27_bot', video_name, progress=progress)
        await mes.delete()
        os.remove(video_name)
        return video.video.file_id #4430362
