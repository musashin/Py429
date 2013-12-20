'''
Created on 2013-11-06

@author: nicolas
'''
import unittest
import DiscreteBit
import Exception


class testValueExceptions(unittest.TestCase):
    '''
    Test protections against data that does not correspond to the field type
    '''
    
    def testCanRepresentItself(self):
        try:
            DiscreteBit.Field(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        except Exception:
            self.fail("LabelField cannot represent itself")


    def testInvalidDataType(self):
        """
        Confirm that only boolean are accepted as values
        """
        label = DiscreteBit.Field(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(Exception.A429Exception,label.setData,5)
        self.assertRaises(Exception.A429Exception,label.setData,8.5)
        self.assertRaises(Exception.A429Exception,label.setData,'x')
        
class testNoData(unittest.TestCase):
    '''
    Test situation where the bit field is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the bit field was not set
        '''
        bit = DiscreteBit.Field(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(Exception.A429NoData,bit.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the  bit field was not set
        '''
        bit = DiscreteBit.Field(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(Exception.A429NoData,bit.pack)
     
    def testClearing(self):
        '''
        Call pack when the label was not set
        '''
        bit = DiscreteBit.Field(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        bit.setData(True)
        bit.clear()
        self.assertRaises(Exception.A429NoData,bit.pack)
        
class testBitPackandUnpack(unittest.TestCase):
    """Verify that bits are packed and unpacked properly"""
    def testBitPackingSet(self):
        """
        Move a bit from 1 to 32, check only this bit is set
        """
        for i in range(1, 32):
            bit = DiscreteBit.Field(bitIndex=i,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
    
            bit.setData(True)
            self.assertEqual(bit.pack(),1<<(i-1), "Label Not Packed Properly")
    
    def testBitPackingUnset(self):
        """
        Move a bit from 1 to 32, check only this bit is not set
        """
        for i in range(1, 32):
            bit = DiscreteBit.Field(bitIndex=i,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
    
            bit.setData(False)
            self.assertEqual(bit.pack(),0, "Label Not Packed Properly")
            
    def testBitUnpacking(self):
        """
        Move a unpacked dit from 1 to 32 in a packed word, make sure the field
        varies accordingly
        """
        for i in range(1, 32):
            bit = DiscreteBit.Field(bitIndex=i,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
    
            for j in range(1, 32):
                bit.unpack(1<<(j-1))
                self.assertEqual(bit.getData(),i==j, "Label Not Un-Packed Properly")

if __name__ == "__main__":
    unittest.main()