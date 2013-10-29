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
        self.assertRaises(TypeError,A429LabelField.LabelField,5)
        self.assertRaises(TypeError,A429LabelField.LabelField,8.5)
        
    def testNonOctal(self):
        self.assertRaises(A429Exception.A429MsgRangeError,A429LabelField.LabelField,'378')
        
            
    def testLabelUpperLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        self.assertRaises(A429Exception.A429MsgRangeError,A429LabelField.LabelField,'378')
        
    def testLabelLowerLimit(self):
        """
        Confirm that value above 377 are rejected
        """
        self.assertRaises(A429Exception.A429MsgRangeError,A429LabelField.LabelField,'-1')
    
class testLabelCreations(unittest.TestCase):
    """Verify that label fields are created properly"""

    def testLabelGeneration(self):
        """
        packed different possible labels and confirm they are packed properly
        """
        refValues = ((0,0),(41,0b10000100),(107,0b11100010),(206,0b01100001),(350,0b00010111),(377,0xFF))
        for label,packed in refValues:
            labelField = A429LabelField.LabelField(str(label))
            self.assertEqual(labelField.pack(),packed, "Label Not Packed Properly")
            


if __name__ == "__main__":
    unittest.main()