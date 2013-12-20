'''
Created on 2013-10-22

@author: nicolas
'''
import unittest
import Label
import Exception

class testValueExceptions(unittest.TestCase):
    
    def testCanRepresentItself(self):
        try:
            Label.Field()
        except Exception:
            self.fail("LabelField cannot represent itself")

    def testLabelFormat(self):
        """
        Confirm that an integer or floating point value is not accepted a labeValue
        """
        label = Label.Field()
        self.assertRaises(Exception.A429Exception,label.setData,5)
        self.assertRaises(Exception.A429Exception,label.setData,8.5)
        
    def testNonOctal(self):
        label = Label.Field()
        self.assertRaises(Exception.A429MsgRangeError,label.setData,'378')
              
    def testLabelUpperLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        label = Label.Field()
        self.assertRaises(Exception.A429MsgRangeError,label.setData,'378')
        
    def testLabelLowerLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        label = Label.Field()
        self.assertRaises(Exception.A429MsgRangeError,label.setData,'-1')
    
class testNoData(unittest.TestCase):
    '''
    Test situation where label is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the label was not set
        '''
        label = Label.Field()
        self.assertRaises(Exception.A429NoData,label.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the label was not set
        '''
        labelField = Label.Field()
        labelField.setData(str(41))
        labelField.clear()
        self.assertRaises(Exception.A429NoData,labelField.pack)
    
    def testClearing(self):
        '''
        Call pack when the label was not set
        '''
        label = Label.Field()
        self.assertRaises(Exception.A429NoData,label.pack)
        
class testLabelCreations(unittest.TestCase):
    """Verify that label fields are created properly"""
    refValues = ((0,0),(41,0b10000100),(107,0b11100010),(206,0b01100001),(350,0b00010111),(377,0xFF))
    
    def testLabelPacking(self):
        """
        pack different labels and confirm they are coded properly
        """
        for label,packed in self.refValues:
            labelField = Label.Field()
            labelField.setData(str(label))
            self.assertEqual(labelField.pack(),packed, "Label Not Packed Properly")
            
    def testLabelUnpacking(self):
        """
        unpack different labels and confirm they are decoded properly
        """
        for label,packed in self.refValues:
            labelField = Label.Field()
            labelField.unpack(packed)
            self.assertEqual(labelField.getData(),int(str(label),8), "Label Not Unpacked Properly")

if __name__ == "__main__":
    unittest.main()