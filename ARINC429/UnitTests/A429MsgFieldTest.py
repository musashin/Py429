'''
Created on 7 mai 2013

@author: nulysse
'''
import unittest
import A429MsgField
import A429Exception

class PackingBaseFieldNormal(unittest.TestCase):
    """ Verify Packing Functionality """    
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
            
    def testUpperBound(self):
        field = A429MsgField.A429MsgField(32,1,"Test Field")
        packed = field.pack(0x0)
        self.assertEqual(packed,0x0, "Cannot pack MSB")
        packed = field.pack(0x1)
        self.assertEqual(packed,0x80000000, "Cannot pack MSB")
        
    def testLowerBound(self):
        field = A429MsgField.A429MsgField(1,1,"Test Field")
        packed = field.pack(0x0)
        self.assertEqual(packed,0x0, "Cannot pack LSB")
        packed = field.pack(0x1)
        self.assertEqual(packed,0x1, "Cannot pack LSB")
    
    def testPackingFewReferenceValues(self):
        """ Test Packing for a few reference values """
        refValues = ((3,4),(11,5),(13,9),(21,8),(30,2),(4,16))
        for lsb,size in refValues:
            field = A429MsgField.A429MsgField(lsb,size,"test field")
            for movingBit in range(0,(size-1)):
                packed = field.pack(1<<movingBit)
                self.assertEqual(packed,1<<(movingBit+lsb-1))
                
    def testUnPackingFewReferenceValues(self):
        """ Test unpacking for a few reference values """
        refValues = ((3,4),(11,5),(13,9),(21,8),(30,2),(4,16))
        for lsb,size in refValues:
            field = A429MsgField.A429MsgField(lsb,size,"test field")
            for movingBit in range(0,(size-1)):
                unpacked = field.unpack(1<<(movingBit + lsb -1))
                self.assertEqual(unpacked,1<<(movingBit))
    
    def testFootPrint(self):
        ''' Test Foot print calculations'''
        refValues = ({'lsb':3,'size':4,'footPrint':0b111100},
                     {'lsb':1,'size':32,'footPrint':0b11111111111111111111111111111111},
                     {'lsb':1,'size':1,'footPrint':0b1},
                     {'lsb':5,'size':10,'footPrint':0b11111111110000},
                     {'lsb':15,'size':7,'footPrint':0b111111100000000000000})
        for testCase in refValues:
            field = A429MsgField.A429MsgField(testCase['lsb'],testCase['size'],"test field")
            self.assertEqual(field.getFootPrint(),testCase['footPrint'])
        
class PackingRangeLimits(unittest.TestCase):
    """ Verify Range Limiting Exceptions """
    def testRangeExceededMax(self):
        """ A429MsgField Should fail when the data to pack exceeds the size of the field"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.pack, 4)
        
    def testRangeExceededMin(self):
        """ A429MsgField Should fail when the data to pack is lower than zero"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.pack, -0.001)
        
class UnPackingRangeLimits(unittest.TestCase):
    """ Verify Range Limiting Exceptions """
    def testRangeExceededMax(self):
        """ A429MsgField Should fail when the data to unpack is larger than a 32 bit word"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.unpack, 0x1FFFFFFFF)
        
    def testRangeExceededMin(self):
        """ A429MsgField Should fail when the data to pack is lower than zero"""
        field = A429MsgField.A429MsgField(5,2,"Test Field")
        self.assertRaises(A429Exception.A429MsgRangeError, field.unpack, -0.001)
  
class StructureExceptions(unittest.TestCase):
    """ Verify Field Structure Exceptions"""
    def testLowLSB(self):
        """ A429MsgField shall be capable of holding all bits set to 1"""
        # self.assertRaises(A429Exception.A429MsgStructureError, A429MsgField.A429MsgField,0,1,"Test Field")
        
    def testTooLargeField(self):
        """ MSB shall never be greater then 32 """
        self.assertRaises(A429Exception.A429MsgStructureError, A429MsgField.A429MsgField,1,33,"Test Field")
         
               
if __name__ == "__main__":
    unittest.main()