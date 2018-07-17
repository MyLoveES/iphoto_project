import random
import string

from util.mongo_connect import collection


def generate_code():
    """
    生成四位数字的验证码
    :return:
    """
    seeds = "1234567890"
    random_str = []
    for i in range(6):
        random_str.append(random.choice(seeds))

    return "".join(random_str)


def make_share_url():
    figures = random.randint(12, 18)
    sequence = string.ascii_letters+string.digits+'$-_+!*()'
    url = []
    while True:
        for i in range(figures):
            url.append(random.choice(sequence))
        url = ''.join(url)
        if not collection.find_one({"url": url}):
            break
    return url


def make_share_password():
    sequence = string.ascii_lowercase+string.digits
    return ''.join(random.sample(sequence, 4))


def make_face_token():
    return "face_token_"+make_share_url()