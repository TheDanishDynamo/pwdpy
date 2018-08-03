# https://www.practicepython.org/exercise/2014/05/28/16-password-generator.html
# https://www.practicepython.org/exercises/

'''
Write a password generator in Python.
Be creative with how you generate passwords -
strong passwords have a mix of lowercase letters,
uppercase letters, numbers, and symbols.
The passwords should be random, generating a new
password every time the user asks for a new password.
Include your run-time code in a main method.

Extra:

Ask the user how strong they want their password to be. For weak passwords, pick a word or two from a list.

Password Length
Include Symbols
Include Numbers
Include Lowercase Characters
Include Uppercase Characters
'''
import random
import string
import re


class PasswordGenerator:

    # Constructor; Define and init complexity
    def __init__(self, length=0, symbols=False, numbers=False, uppercase=False, lowercase=False, repeating=False):
        self.length = length  # Length of generated password
        self.symbols = symbols  # Include special characters
        self.numbers = numbers  # Include 0-9
        self.uppercase = uppercase  # Include A-Z
        self.lowercase = lowercase  # Include a-z
        self.repeating = repeating  # If True then same element can occur multiple times
        self.UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
        self.SYMBOLS = r"{}()[]#:;^,.?!|&_`~@$%/\+-=*'" + chr(34)
        self.NUMBERS = "0123456789"
        self.domain = ""
        # self.symbols = symbols
        if self.symbols:
            self.domain += self.SYMBOLS
        # self.numbers = numbers
        if self.numbers:
            self.domain += self.NUMBERS
        # self.uppercase = uppercase
        if self.uppercase:
            self.domain += self.UPPER_CASE
        # self.lowercase = lowercase
        if self.lowercase:
            self.domain += self.LOWER_CASE

        # Ease of use but questionsble default
        if self.domain == "" and self.length > 0:
            self.domain = self.UPPER_CASE + self.LOWER_CASE + self.SYMBOLS + self.NUMBERS
            self.lowercase = True
            self.uppercase = True
            self.symbols = True
            self.numbers = True

        # Base-N - the number of characters in the domain
        self.base = len(self.domain)

    def getStrength(self):
        # TODO: Find a more accurate measure
        if self.base > 20 and self.length > 6:
            return "strong"
        else:
            return "weak"

    def getDomainGroupCount(self):
        # sum(x > 0 for x in frequencies)
        return sum(x for x in [self.uppercase, self.lowercase, self.symbols, self.numbers] if x)

    def getMaxDomain(self):
        return self.UPPER_CASE + self.LOWER_CASE + self.SYMBOLS + self.NUMBERS

    def getActiveDomain(self):
        return self.domain

    def getMaxBase(self):
        return len(self.getMaxDomain())

    def getLength(self):
        return self.length

    # return random list or set of lowercase with length of self.length
    def generate(self):
        if self.base == 0:
            return ""
        divisor = 0
        if self.lowercase:
            divisor += 1  # E.g. 8/1 for lowercase only w length 8
        if self.uppercase:
            divisor += 1  # E.g. 8/2, 8/1
        if self.symbols:
            divisor += 1  # E.g. 8/3, 8/2, 8/1
        if self.numbers:
            divisor += 1  # E.g. 4/4, 8/3, 8/2, 8/1

        if divisor == 0:
            raise Exception(
                "Password complexity must include upper case, lower case or symbols")

        if self.length == 0:
            raise Exception("Length must be greater than zero")

        if False:
            pass
            # TODO: raise exception if upp/lower/symbol/number and length < 4

        temp = ""
        remainder_length = self.length
        part_length = int(self.length / divisor)
        if part_length == 0:
            part_length = 1

        # ISSUE: if password length is 1, a number is always chosen
        # FIX: Randomize the call order of the following if's

        call_order = [1, 2, 3, 4]

        random.shuffle(call_order)

        # TODO: Consider map or lambda on call_order
        for c in call_order:
            if c == 1:
                if self.lowercase and remainder_length > 0:
                    remainder_length -= part_length
                    temp += self.LOWER_CASE[:part_length]
            elif c == 2:
                if self.uppercase and remainder_length > 0:
                    remainder_length -= part_length
                    temp += self.UPPER_CASE[:part_length]
            elif c == 3:
                if self.symbols and remainder_length > 0:
                    remainder_length -= part_length
                    temp += self.SYMBOLS[:part_length]
            elif c == 4:
                if self.numbers and remainder_length > 0:
                    remainder_length -= part_length
                    temp += self.NUMBERS[:part_length]
            if remainder_length <= 0:
                break

        remainder_length = self.getLength()-len(temp)
        # If there still is remainder,
        # append random characters from the active domains
        if remainder_length > 0:
            supplement = "".join(random.choice(self.getActiveDomain()) for i in range(remainder_length))
            temp += supplement

        print(self.SYMBOLS)
        # Randomize
        return self.shuffle(temp)

    def shuffle(self, s):
        l = list(s)
        random.shuffle(l)
        return "".join(l)

class PasswordHelper:
    def __init__(self):
        self.pwdgen = PasswordGenerator()

    def validate(self, password, numbers=False, lowercase=False, uppercase=False, symbols=False):
        if numbers:
            # Look for numbers in password
            p = re.compile(".*["+self.pwdgen.NUMBERS+"].*")
            print(p.findall(password))
            if len(p.findall(password)) == 0:
                return False
        if lowercase:
            # Look for lowercase in password
            p = re.compile(".*["+self.pwdgen.LOWER_CASE+"].*")
            print(p.findall(password))
            if len(p.findall(password)) == 0:
                return False
        if uppercase:
            # Look for uppercase in password
            p = re.compile(".*["+self.pwdgen.UPPER_CASE+"].*")
            print(p.findall(password))
            if len(p.findall(password)) == 0:
                return False
        if symbols:
            # Look for symbols in password
            # Symbols are tricky because regex use the []() etc
            # so use for .. in ..
            found = False
            for c in password:
                if c not in self.pwdgen.SYMBOLS:
                    found = False
                else:
                    found = True
                    break
            if not found:
                return False

        # All the above checks passed, so it's good!!
        return True
