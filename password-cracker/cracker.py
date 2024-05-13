import hashlib
import re
from urllib3 import PoolManager, HTTPResponse


class PasswordCracker(object):

    @staticmethod
    def pattern(i: int) -> re.Pattern:
        return re.compile(r'^[a-zA-Z0-9]{'+str(i)+'}$')

    def is_md5(self, hash_str: str) -> bool:
        return len(hash_str) == 32 and (self.pattern(32).match(hash_str) is not None)

    def is_sha1(self, hash_str: str) -> bool:
        return len(hash_str) == 40 and (self.pattern(40).match(hash_str) is not None)

    def is_sha224(self, hash_str: str) -> bool:
        return len(hash_str) == 56 and (self.pattern(56).match(hash_str) is not None)

    def is_sha256(self, hash_str: str) -> bool:
        return len(hash_str) == 64 and (self.pattern(56).match(hash_str) is not None)

    def is_sha384(self, hash_str: str) -> bool:
        return len(hash_str) == 96 and (self.pattern(96).match(hash_str) is not None)

    def is_sha512(self, hash_str: str) -> bool:
        return len(hash_str) == 128 and (self.pattern(128).match(hash_str) is not None)

    def crack(self, worldlist: list, hash_str: str):
        """
        :param worldlist: list of words;
        :param hash_str: string of hash
        :return: None if found nothing, else return string of password
        """
        guess = None

        if self.is_md5(hash_str):
            for passwrd in worldlist:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break
        elif self.is_sha1(hash_str):
            for passwrd in password_list:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break
        elif self.is_sha224(hash_str):
            for passwrd in password_list:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break
        elif self.is_sha256(hash_str):
            for passwrd in password_list:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break
        elif self.is_sha384(hash_str):
            for passwrd in password_list:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break
        elif self.is_sha512(hash_str):
            for passwrd in password_list:
                if hash_str == hashlib.sha256(bytes(passwrd, 'utf-8')).hexdigest():
                    guess = passwrd
                    break

        return guess


poolManager = PoolManager()
response: HTTPResponse = poolManager.urlopen('GET', 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt')
password_list = response.data.decode('utf-8').split('\n')

password_str: str = 'Undertaker'
hash_string: str = hashlib.sha256(bytes(password_str, 'utf-8')).hexdigest()

pass_type = None
password = None

if password is not None:
    print(f'Password is {password}')
else:
    print('Password not found in WordList.')
