import threading
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

def sync_wrapper(video_id):
    asyncio.run(listen_to_youtube_chat(video_id))

def run(video_id):
    thread = threading.Thread(target=sync_wrapper, args=(video_id,))
    thread.start()

    return thread
