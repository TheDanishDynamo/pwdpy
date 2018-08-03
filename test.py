import unittest
from pwdpy import PasswordGenerator
from pwdpy import PasswordHelper
import numpy


class TestPasswordGeneratorMethods(unittest.TestCase):

    def test_generate_default_blank(self):
        pg = PasswordGenerator()
        self.assertEqual(len(pg.generate()), 0)

    def test_generate_1_defaults(self):
        pg = PasswordGenerator(length=1)
        self.assertEqual(len(pg.generate()), 1)

    def test_generate_1_number(self):
        pg = PasswordGenerator(length=1, numbers=True)
        p = pg.generate()
        self.assertTrue(p in pg.NUMBERS)

    def test_generate_1_symbol(self):
        pg = PasswordGenerator(length=1, symbols=True)
        p = pg.generate()
        self.assertTrue(p in pg.SYMBOLS)

    def test_generate_1_lowercase(self):
        pg = PasswordGenerator(length=1, lowercase=True)
        p = pg.generate()
        self.assertTrue(p in pg.LOWER_CASE)

    def test_generate_1_max_domain(self):
        pg = PasswordGenerator(length=1, numbers=True,
                               symbols=True, lowercase=True, uppercase=True)
        p = pg.generate()
        self.assertTrue(p in pg.getMaxDomain())

    def test_generate_5_max_domain(self):
        pg = PasswordGenerator(length=5)
        p = pg.generate()
        self.assertEqual(len(p), 5)

    def test_generate_1_to_1000_max_domain(self):
        for n in range(1, 1001):
            pg = PasswordGenerator(
                length=n, numbers=True, symbols=True, lowercase=True, uppercase=True)
            p = pg.generate()

            # validate length
            self.assertEqual(n, len(p))

            # validate complexity
            for c in p:
                self.assertTrue(c in pg.getActiveDomain())

    def test_generate_44_max_domain(self):
        for n in range(44, 45):
            pg = PasswordGenerator(
                length=n, numbers=True, symbols=True, lowercase=True, uppercase=True)
            p = pg.generate()

            # validate length
            self.assertEqual(n, len(p))

    def test_generate_domain_analysis(self):
        """Generate and verify password.

        Generate a password and verify that each character is
        evenly distributed in each domain NLUS, with some slack
        in case of length not divisible by 4 (NLUS)
        """
        pwl = 10
        pg = PasswordGenerator(length=pwl, numbers=True,
                               symbols=True, lowercase=True, uppercase=True)
        p = pg.generate()
        n, l, u, s = 0, 0, 0, 0
        for c in p:
            if c in pg.NUMBERS:
                n += 1
            if c in pg.LOWER_CASE:
                l += 1
            if c in pg.UPPER_CASE:
                u += 1
            if c in pg.SYMBOLS:
                s += 1
        diff = numpy.subtract((n, l, u, s), (pwl/4, pwl/4, pwl/4, pwl/4))
        for x in diff:
            self.assertTrue(abs(x) < 2)

    def test_generate_1_uppercase(self):
        pg = PasswordGenerator(length=1, uppercase=True)
        p = pg.generate()
        self.assertTrue(p in pg.UPPER_CASE)

    def test_get_domain_group_count(self):
        pg = PasswordGenerator(length=1)
        dgc = pg.getDomainGroupCount()
        self.assertEqual(dgc, 4)

    def test_validate_1_numbers(self):
        pg = PasswordGenerator(length=1, numbers=True)
        p = pg.generate()
        print(p)
        helper = PasswordHelper()
        self.assertTrue(helper.validate(numbers=True, lowercase=False, password=p))

    def test_validate_4_nlus(self):
        pg = PasswordGenerator(length=4, numbers=True, lowercase=True, uppercase=True, symbols=True)
        p = pg.generate()
        print(p)
        helper = PasswordHelper()
        self.assertTrue(helper.validate(password=p, numbers=True, lowercase=True, uppercase=True, symbols=True))


'''
    Sample tests

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
'''

if __name__ == '__main__':
    unittest.main()
