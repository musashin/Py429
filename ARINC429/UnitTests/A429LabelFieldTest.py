'''
Created on 2013-10-22

@author: nicolas
'''
import unittest
import A429LabelField
import A429Exception


class testExceptions(unittest.TestCase):

    def testLabelFormat(self):
        """
        Confirm that an integer or floating point value is not accepted a labeValue
        """
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429Exception,label.setData,5)
        self.assertRaises(A429Exception.A429Exception,label.setData,8.5)
        
    def testNonOctal(self):
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429MsgRangeError,label.setData,'378')
              
    def testLabelUpperLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429MsgRangeError,label.setData,'378')
        
    def testLabelLowerLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429MsgRangeError,label.setData,'-1')
    
class testNoData(unittest.TestCase):
    '''
    Test situation where label is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the label was not set
        '''
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429NoData,label.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the label was not set
        '''
        label = A429LabelField.LabelField()
        self.assertRaises(A429Exception.A429NoData,label.pack)
    
class testLabelCreations(unittest.TestCase):
    """Verify that label fields are created properly"""
    refValues = ((0,0),(41,0b10000100),(107,0b11100010),(206,0b01100001),(350,0b00010111),(377,0xFF))
    
    def testLabelPacking(self):
        """
        pack different labels and confirm they are coded properly
        """
        for label,packed in self.refValues:
            labelField = A429LabelField.LabelField()
            labelField.setData(str(label))
            self.assertEqual(labelField.pack(),packed, "Label Not Packed Properly")
            
    def testLabelUnpacking(self):
        """
        unpack different labels and confirm they are decoded properly
        """
        pass
        for label,packed in self.refValues:
            labelField = A429LabelField.LabelField()
            labelField.unpack(packed)
            self.assertEqual(labelField.getData(),int(str(label),8), "Label Not Unpacked Properly")
            
if __name__ == "__main__":
    unittest.main()