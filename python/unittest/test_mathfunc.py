import unittest
from mathfunc import *

class TestMathFunc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    #skip Decorator
    @unittest.skip("i don't want to run this case.")
    def test_minus(self):
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        self.skipTest('do not run this.')   #unittest skip method
        self.assertEqual(6, multi(3, 2))

    def test_divide(self):
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main()
