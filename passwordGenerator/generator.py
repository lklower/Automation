import string
from argparse import ArgumentParser
import random

random.seed(random.randint(1, 9999))

/**
 handle special charaters function.
**/
def special_charaters():
    l: list = ['!', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '|', '/', '[', ']', '{', '}', ':', '.', ',', ';', '?', '<', '>']
    random.shuffle(l)
    return l


def lowercase_latters():
    l: list = [i for i in string.ascii_lowercase]
    random.shuffle(l)
    return l


def uppercase_latters():
    l: list = [i for i in string.ascii_uppercase]
    random.shuffle(l)
    return l


def digits():
    l: list = [i for i in string.digits]
    random.shuffle(l)
    return l


def main(args):
    password: list[str] = []
    combination: list = special_charaters() + lowercase_latters() + uppercase_latters() + digits()

    total: int = args.digit + args.lowercase + args.uppercase + args.special_chars
    password_size: int = max(total, args.min_length)

    if args.digit > 0:
        password += random.choices(digits(), weights=None, k=args.digit)
        password_size -= args.digit

    if args.lowercase > 0:
        password += random.choices(lowercase_latters(), weights=None, k=args.lowercase)
        password_size -= args.lowercase

    if args.digit > 0:
        password += random.choices(uppercase_latters(), weights=None, k=args.uppercase)
        password_size -= args.uppercase

    if args.digit > 0:
        password += random.choices(special_charaters(), weights=None, k=args.special_chars)
        password_size -= args.special_chars

    if password_size > 0:
        for _ in range(password_size):
            random.shuffle(combination)
            password.append(random.choice(combination))
            password_size -= 1

    random.shuffle(password)
    str_password: str = ''.join(password)

    print(f'You generated password is: {str_password}', end='\n')


if __name__ == '__main__':
    parser = ArgumentParser(prog='Password Generator', description='Generate the random password with this tool')

    parser.add_argument('-d', '--digit', default=1, type=int, help='At least numbers of digits should contain in the password')
    parser.add_argument('-l', '--lowercase', default=1, type=int, help='At least umbers of lowercase latters should contain in the password')
    parser.add_argument('-u', '--uppercase', default=1, type=int, help='At least Numbers of uppercase letters should contain in the password')
    parser.add_argument('-s', '--special-chars', default=1, type=int, help='At least Numbers of special chars should contain in the password')
    parser.add_argument('-m', '--min-length', default=10, type=int, help='The minimium length of password. Default set to 10')

    main(args=parser.parse_args())
