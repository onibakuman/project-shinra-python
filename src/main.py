from platforms import youtube_chat

if __name__ == "__main__":
    import sys
    vid = sys.argv[1] if len(sys.argv) > 1 else "VIDEO_ID_HERE"
    youtube_chat.run(vid)
