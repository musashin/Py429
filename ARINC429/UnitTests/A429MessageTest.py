'''
Created on 2013-12-04

@author: nicolas
'''
import unittest
import A429Message
import A429Exception
import A429DiscreteBitField

class TestPacking(unittest.TestCase):
    '''
    Test the packing functionality
    '''
    
    def testBaseMessage(self):
        baseMessage = A429Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        self.assertEqual(baseMessage.pack(), 0b10000000000000000000000011110101, "Label Not Packed Properly")
        baseMessage.changeParityConvention('even')
        self.assertEqual(baseMessage.pack(), 0b00000000000000000000000011110101, "Label Not Packed Properly")

    def testSimpleFieldAddition(self):

        baseMessage = A429Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        baseMessage.addField(A429DiscreteBitField.DiscreteBitField(10,'testBit','test bit is happy','test bit is not happy'))
        baseMessage.setFieldValueByName('testBit',True)
        self.assertEqual(baseMessage.pack(), 0b00000000000000000000001011110101, "Label Not Packed Properly")


class TestProtections(unittest.TestCase):
    '''
    Verify safeguard are in place
    '''

    def testCannotPackBasicMessage(self):
        '''
        Ensure the basic message, with no data set, cannot be packed
        '''
        baseMessage = A429Message.Message(name='baseMessage')
        self.assertRaisesRegexp(A429Exception.A429NoData,"label",baseMessage.pack)

    def testCannotAddOverlappingField(self):
        '''
        Ensure that a field cannot be added if it overlaps an existing field
        '''
        baseMessage = A429Message.Message(name='baseMessage')
        overlappingField = A429DiscreteBitField.DiscreteBitField(8,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(A429Exception.A429NoData,baseMessage.addField,overlappingField)


    def testCannotPackWhenDataNotSet(self):
        '''
        Ensure a message which does not have all
        fields set cannot be packed
        '''

if __name__ == "__main__":
    unittest.main()