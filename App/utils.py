import random


def get_color():
    return random.randint(0,256)


def generate_code():
    source= "1234567890zxcvbnmasdfghjkklqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM"
    code = ''
    for i in range(0,4):
        code +=random.choice(source)
    return code