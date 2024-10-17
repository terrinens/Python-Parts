import os
import string
import random
import shutil
import uuid

def str_ran(n):
    rand_str = ""
    for i in range(n):
        rand_str += str(random.choice(string.ascii_uppercase))
    return rand_str

def copy_md():
    for _ in range(10):
        r_str = str_ran(10)
        shutil.copy('./test.mdx', f'./{uuid.uuid4()}.mdx')

def clear_md():
    for filename in os.listdir('./'):
        if filename.lower().endswith(".mdx"):
            if filename != 'test.mdx':
                os.remove(os.path.join('./', filename))

if __name__ == "__main__":
    copy_md()