import pytchat
import asyncio
from utils import commands

async def listen_to_youtube_chat(video_id):
    chat = pytchat.create(video_id=video_id)
    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                print(f"{c.datetime} [{c.author.name}] : {c.message}")
                commands.check_if_command(c.message)
            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        chat.terminate()
