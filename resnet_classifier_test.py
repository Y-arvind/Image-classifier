#!flask/bin/python
import unittest
from resnet_classifier import ResnetClassifier

class TestCase(unittest.TestCase):
    def test_classifier(self):
        with open("test.jpeg", "rb") as image:
            f = image.read()
            c = ResnetClassifier()
            l = c.classify(f)
            assert l[0][0] == 'Labrador retriever'
        image.close()

if __name__ == '__main__':
    unittest.main()
