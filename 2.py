import os

with os.scandir('C:\Machine-Learning') as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            print(entry.name)
            print(entry.stat())


#help(os)