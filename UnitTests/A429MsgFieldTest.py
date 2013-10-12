'''
Created on 7 mai 2013

@author: nulysse
'''
import unittest
import A429MsgField
import A429Exception

class PackingBaseField(unittest.TestCase):

    def testSanityCheck1(self):
        
        for integer in range(1, 32-2):
            field = A429MsgField.A429MsgField(integer,2,"Test Field","301","01")
            packed = field.pack(3)
            self.assertEqual(packed,3<<(integer-1), "Simple Packing Failed")
        pass
    
    def testRangeError(self):
        field = A429MsgField.A429MsgField(5,7,"Test Field","301","01")
        self.assertRaises(A429Exception.A429MsgRangeError, field.pack, 4)

if __name__ == "__main__":
    unittest.main()