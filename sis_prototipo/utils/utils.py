import hashlib


def generate_sha(file):
    """
    Codifica un archivo para revisar su unicidad
    :param file:
    :return:
    """
    sha = hashlib.sha1()
    file.seek(0)
    while True:
        buf = file.read(104857600)
        if not buf:
            break
        sha.update(buf)
    sha1 = sha.hexdigest()
    file.seek(0)
    return sha1


def luhn(value):
    digits = list(map(int, str(value)))
    oddsum = sum(digits[-1::-2])
    evnsum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (oddsum + evnsum) % 10 == 0
