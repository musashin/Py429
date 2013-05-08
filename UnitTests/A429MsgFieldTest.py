'''
Created on 7 mai 2013

@author: nulysse
'''
import unittest
from A429MsgField import *

class PackingBaseField(unittest.TestCase):

    def testSanityCheck(self):
        field = A429MsgField(1,3,"Test Field","301","01")
        packed = field.pack(3)
        self.assertEqual(packed, bitarray.bitarray('101'), "Simple Packing Failed")
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()