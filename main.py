import pytchat
import asyncio

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
    
APP_ID = ""
APP_SECRET = ""
USER_SCOPE = [AuthScope.CHAT_READ]

audio_dir_prefix = "sfx/"
command_prefix = "!"
commands = {
    "cum" : "cum.wav",
    "coom" : "coom.wav",
}

def read_credential_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            APP_ID = lines[0].strip()
            APP_SECRET = lines[1].strip()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_if_command(message):
    for command in commands:
        full_command = command_prefix + command
        if full_command in message:
            print("yay we did it. command: " + command + " executed!")

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

async def listen_to_twitch_chat(channel_name):
    # Set up Twitch client and authenticate
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # Create chat instance
    chat = await Chat(twitch)

    # Event handler for ready (join channel)
    async def on_ready(ready_event: EventData):
        print(f'Bot ready, joining channel: {channel_name}')
        await ready_event.chat.join_room(channel_name)

    # Event handler for messages
    async def on_message(msg: ChatMessage):
        print(f"{msg.timestamp} [{msg.user.name}] : {msg.text}")
        check_if_command(msg.text)

    # Register handlers
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    # Start listening
    chat.start()

    try:
        await asyncio.Event().wait()  # Run until interrupted
    except KeyboardInterrupt:
        pass
    finally:
        chat.stop()
        await twitch.close()

if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else "VIDEO_ID_HERE"
    read_credential_file("fake_credentials.txt")
    asyncio.run(main(vid))
    asyncio.run(listen_to_twitch_chat("onibakuman"))
