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

class TestUnpacking(unittest.TestCase):
    ''''
    Test the unpacking functionality
    '''

    def testBaseMessage(self):
        '''
        Test a base message -just label and parity- can be unpacked properly
        '''
        baseMessage = A429Message.Message('baseMessage', 'odd')
        baseMessage.unpack(0b10000000000000000000000011110101)
        self.assertEqual(baseMessage.getLabel(), 0257, "Label Not UnPacked Properly")
        baseMessage.changeParityConvention('even')
        self.assertEqual(baseMessage.pack(), 0b00000000000000000000000011110101, "Label Not Packed Properly")

    def testSimpleFieldAddition(self):
         pass
        #TODO


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
        self.assertRaises(A429Exception.A429MsgStructureError,baseMessage.addField,overlappingField)

        overlappingField = A429DiscreteBitField.DiscreteBitField(32,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(A429Exception.A429MsgStructureError,baseMessage.addField,overlappingField)

    def testCannotHaveDuplicateFieldNames(self):
        '''
        Ensure there cannot be 2 fields with the same name
        '''
        baseMessage = A429Message.Message(name='baseMessage')
        overlappingField = A429DiscreteBitField.DiscreteBitField(12,'testBit','test bit is happy','test bit is not happy')
        baseMessage.addField(overlappingField)

        overlappingField2 = A429DiscreteBitField.DiscreteBitField(20,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(A429Exception.A429MsgStructureError,baseMessage.addField,overlappingField2)

    def testMessageValidityCheck(self):
        '''
        Test a en exception is raised when attempting to unpack and invalid message
        '''
        baseMessage = A429Message.Message('baseMessage', 'odd')
        self.assertRaises(A429Exception.A429InvalidMessage,baseMessage.unpack,0b00000000000000000000000011110101)
        baseMessage.changeParityConvention('even')
        self.assertRaises(A429Exception.A429InvalidMessage,baseMessage.unpack,0b10000000000000000000000011110101)

    def testCannotPackWhenDataNotSet(self):
        '''
        Ensure a message which does not have all
        fields set cannot be packed
        '''
        #TODO

if __name__ == "__main__":
    unittest.main()