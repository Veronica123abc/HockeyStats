import os
from pathlib import Path
import uuid


def string_to_file(data, parent_dir, filename=None):
    if filename is None:
        filename = str(uuid.uuid4())
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    with open(os.path.join(parent_dir, filename),'w+') as f:
        f.write(data)

    print('Wrote ' + str(len(data)) + ' to ' + os.path.join(parent_dir, filename))
