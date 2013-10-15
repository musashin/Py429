'''
Created on 7 mai 2013

@author: nulysse
'''
import unittest
import A429MsgField
import A429Exception

class PackingBaseFieldNormal(unittest.TestCase):
    
    def testMax(self):
        """ A429MsgField shall be capable of holding all bits set to 1 """
        field = A429MsgField.A429MsgField(1,32,"Test Field")
        packed = field.pack(0xFFFFFFFF)
        self.assertEqual(packed,0xFFFFFFFF, "Cannot Reach Max Range")
        
    def testSanityCheck(self):
        """ Verify a Simple 2 Bit Integer can be configured everywhere in the message """   
        for integer in range(1, 31):
            field = A429MsgField.A429MsgField(integer,2,"Test Field")
            packed = field.pack(3)
            self.assertEqual(packed,3<<(integer-1), "Simple Packing Failed")

    def testRangeExceededMax(self):
        """ A429MsgField Should fail when the data to pack exceeds the size of the field"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.pack, 4)
        
    def testRangeExceededMin(self):
        """ A429MsgField Should fail when the data to pack is lower than zero"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.pack, -0.001)
  
class StructureExceptions(unittest.TestCase):
    def testLowLSB(self):
        """ A429MsgField shall be capable of holding all bits set to 1"""
        # self.assertRaises(A429Exception.A429MsgStructureError, A429MsgField.A429MsgField,0,1,"Test Field")
        
    def testTooLargeField(self):
        """ MSB shall never be greater then 32 """
        self.assertRaises(A429Exception.A429MsgStructureError, A429MsgField.A429MsgField,1,33,"Test Field")

if __name__ == "__main__":
    unittest.main()