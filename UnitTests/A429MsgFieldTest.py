'''
Created on 7 mai 2013

@author: nulysse
'''
import unittest
import A429MsgField

class PackingBaseField(unittest.TestCase):

    def testSanityCheck(self):
        field = A429MsgField.A429MsgField(1,3,"Test Field","301","01")
        packed = field.pack(3)
        print "value is " + str(packed)
        self.assertEqual(packed,3, "Simple Packing Failed")
        pass


if __name__ == "__main__":
    unittest.main()