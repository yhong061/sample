# coding=utf-8
import unittest
from test_mathfunc import TestMathFunc

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [TestMathFunc("test_add"), TestMathFunc("test_minus"), TestMathFunc("test_divide"), TestMathFunc("test_multi")]
    suite.addTests(tests)
    
    #output test results to Console
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    #output test reults to files
    #with open('UnittestTextReport.txt', 'a') as f:
    #    runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #    runner.run(suite)
        
