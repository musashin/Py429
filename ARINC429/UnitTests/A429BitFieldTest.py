'''
Created on 2013-11-06

@author: nicolas
'''
import unittest
import A429DiscreteBitField
import A429Exception


class testValueExceptions(unittest.TestCase):
    '''
    Test protections against data that does not correspond to the field type
    '''

    def testInvalidDataType(self):
        """
        Confirm that only boolean are accepted as values
        """
        label = A429DiscreteBitField.DiscreteBitField(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(A429Exception.A429Exception,label.setData,5)
        self.assertRaises(A429Exception.A429Exception,label.setData,8.5)
        self.assertRaises(A429Exception.A429Exception,label.setData,'x')
        
class testNoData(unittest.TestCase):
    '''
    Test situation where the bit field is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the bit field was not set
        '''
        bit = A429DiscreteBitField.DiscreteBitField(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(A429Exception.A429NoData,bit.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the  bit field was not set
        '''
        bit = A429DiscreteBitField.DiscreteBitField(bitIndex=5,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
        self.assertRaises(A429Exception.A429NoData,bit.pack)
        
class testBitPackandUnpack(unittest.TestCase):
    """Verify that bits are packed and unpacked properly"""
    def testBitPackingSet(self):
        """
        Move a bit from 1 to 32, check only this bit is set
        """
        for i in range(1, 32):
            bit = A429DiscreteBitField.DiscreteBitField(bitIndex=i,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
    
            bit.setData(True)
            self.assertEqual(bit.pack(),1<<(i-1), "Label Not Packed Properly")
    
    def testBitPackingUnset(self):
        """
        Move a bit from 1 to 32, check only this bit is notset
        """
        for i in range(1, 32):
            bit = A429DiscreteBitField.DiscreteBitField(bitIndex=i,
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
            bit = A429DiscreteBitField.DiscreteBitField(bitIndex=i,
                                                      bitName='testBit',
                                                      meaningWhenSet='happy',
                                                      meaningWhenNotSet='unhappy')
    
            for j in range(1, 32):
                bit.unpack(1<<(j-1))
                self.assertEqual(bit.getData(),i==j, "Label Not Un-Packed Properly")

if __name__ == "__main__":
    unittest.main()