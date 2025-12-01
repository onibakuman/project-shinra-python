audio_dir_prefix = "sfx/"
command_prefix = "!"
commands = {
    "cum" : "cum.wav",
    "coom" : "coom.wav",
}

def check_if_command(message):
    for command in commands:
        full_command = command_prefix + command
        if full_command in message:
            print("yay we did it. command: " + command + " executed!")
