import unittest
from mydict import Dict

class TestDict(unittest.TestCase):
    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)                # d.a == 1 ?
        self.assertEqual(d.b, 'test')           # d.b == 'test' ?
        self.assertTrue(isinstance(d, dict))    # d == dict ?

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        #通过d['empty']访问不存在的key时，断言会抛出keyerror
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        #通过d.empty访问不存在的key时，我们期待抛出AttributeError
        with self.assertRaises(AttributeError):
            value = d.empty

if __name__ == '__main__':
    unittest.main()
