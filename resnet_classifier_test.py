#!flask/bin/python
import unittest
from resnet_classifier import ResnetClassifier

class TestCase(unittest.TestCase):
    def test_classifier(self):
        with open("images/test.jpeg", "rb") as image:
            f = image.read()
            c = ResnetClassifier()
            l = c.classify(f)
            assert l is not None
            assert len(l)>0 and len(l[0])>1
            assert l[0][0] == 'Labrador retriever'
        image.close()

if __name__ == '__main__':
    unittest.main()
