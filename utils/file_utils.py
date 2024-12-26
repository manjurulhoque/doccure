import string
from random import choice


def generate_file_name(length=30):
    letters = string.ascii_letters + string.digits
    return "".join(choice(letters) for _ in range(length))


def profile_photo_directory_path(instance, filename):
    return "profiles/{0}".format(
        generate_file_name() + "." + filename.split(".")[-1]
    )
