import os
from os.path import join, getsize

for root, dirs, files in os.walk('C:\examles'):
    print(root, "consumes ")
    print(root,files)
    print(sum(getsize(join(root, name)) for name in files), end=" ")
    print("bytes in", len(files), "non-directory files")
    if 'CVS' in dirs:
        dirs.remove('CVS')  # don't visit CVS directories
