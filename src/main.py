import threading
if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else "VIDEO_ID_HERE"
    read_credential_file("twitch_credentials.txt")
