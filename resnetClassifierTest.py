#!flask/bin/python
import os
import unittest
from resnetClassifier import ResnetClassifier

class TestCase(unittest.TestCase):
    def test_classifier(self):
        c = ResnetClassifier("test.jpeg")
        l = c.test()
        print(l)
        assert l[0][0] == 'Labrador retriever'

if __name__ == '__main__':
    unittest.main()
