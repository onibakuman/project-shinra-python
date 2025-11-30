import pytchat
import asyncio

audio_dir = "sfx/"
commands = { "!cum" : "cum.wav" }

def check_if_command(message):
    if "cum" in message:
        print("cum is in the message!")

async def main(video_id):
    chat = pytchat.create(video_id=video_id)
    try:
        while chat.is_alive():
            for c in chat.get().sync_items():
                print(f"{c.datetime} [{c.author.name}] : {c.message}")
                check_if_command(c.message)
            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        chat.terminate()

if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else "VIDEO_ID_HERE"
    asyncio.run(main(vid))
