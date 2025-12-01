from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
    
APP_ID = ""
APP_SECRET = ""
USER_SCOPE = [AuthScope.CHAT_READ]

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

async def listen_to_twitch_chat(channel_name):
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


