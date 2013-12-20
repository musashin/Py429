'''
Created on 2013-12-04

@author: nicolas
'''
import unittest
import Message
import Exception
import DiscreteBit

class TestMessageConstruction(unittest.TestCase):
    '''
    Test message construction methods
    '''

    def testCanRepresentItself(self):
        try:
            Message.Message('baseMessage', 'odd')
        except Exception:
            self.fail("A429Message cannot represent itself")

    def testFieldAddition(self):
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
        self.assertTrue(baseMessage.isFieldInMessage('testBit'),'Cannot add field properly')

    def testFieldDeletion(self):
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
        self.assertTrue(baseMessage.isFieldInMessage('testBit'),'Cannot add field properly')
        baseMessage.removeField('testBit')
        self.assertFalse(baseMessage.isFieldInMessage('testBit'),'Cannot remove field properly')

    def testFieldAdditionReadiness(self):
        '''
        make sure the function that verify all data are set behaves properly
        '''
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
        sameNameField = DiscreteBit.Field(12,'testBit','test bit is happy','test bit is not happy')
        overlappingField = DiscreteBit.Field(10,'notTestBit','test bit is happy','test bit is not happy')
        differentNameField = DiscreteBit.Field(13,'notTestBit','test bit is happy','test bit is not happy')
        self.assertTrue(baseMessage.canThisFieldBeAdded(differentNameField),'canThisFieldBeAdded cannot be trusted')
        self.assertFalse(baseMessage.canThisFieldBeAdded(sameNameField),'canThisFieldBeAdded cannot be trusted')
        self.assertFalse(baseMessage.canThisFieldBeAdded(overlappingField),'canThisFieldBeAdded cannot be trusted')

class TestPacking(unittest.TestCase):
    '''
    Test the packing functionality
    '''
    
    def testBaseMessage(self):
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        self.assertEqual(baseMessage.pack(), 0b10000000000000000000000011110101, "Label Not Packed Properly")
        baseMessage.changeParityConvention('even')
        self.assertEqual(baseMessage.pack(), 0b00000000000000000000000011110101, "Label Not Packed Properly")

    def testSimpleMessage(self):
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        baseMessage.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
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
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.unpack(0b10000000000000000000000011110101)
        self.assertEqual(baseMessage.getLabel(), 0257, "Label Not UnPacked Properly")
        baseMessage.changeParityConvention('even')
        self.assertEqual(baseMessage.pack(), 0b00000000000000000000000011110101, "Label Not Unpacked Properly")

    def testSimpleMessage(self):
        '''
        Validate added field is unpacked
        '''
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
        baseMessage.unpack(0b00000000000000000000001011110101)
        self.assertEqual(baseMessage.getFieldValueByName('testBit'), True, "Label Not unpacked Properly")
        baseMessage.unpack(0b10000000000000000000000011110101)
        self.assertEqual(baseMessage.getFieldValueByName('testBit'), False, "Label Not unpacked Properly")


class TestProtections(unittest.TestCase):
    '''
    Verify safeguard are in place
    '''

    def testCannotPackBasicMessage(self):
        '''
        Ensure the basic message, with no data set, cannot be packed
        '''
        baseMessage = Message.Message(name='baseMessage')
        self.assertRaisesRegexp(Exception.A429NoData,"label",baseMessage.pack)

    def testCannotAddOverlappingField(self):
        '''
        Ensure that a field cannot be added if it overlaps an existing field
        '''
        baseMessage = Message.Message(name='baseMessage')
        overlappingField = DiscreteBit.Field(8,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(Exception.A429MsgStructureError,baseMessage.addField,overlappingField)

        overlappingField = DiscreteBit.Field(32,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(Exception.A429MsgStructureError,baseMessage.addField,overlappingField)

    def testCannotHaveDuplicateFieldNames(self):
        '''
        Ensure there cannot be 2 fields with the same name
        '''
        baseMessage = Message.Message(name='baseMessage')
        overlappingField = DiscreteBit.Field(12,'testBit','test bit is happy','test bit is not happy')
        baseMessage.addField(overlappingField)

        overlappingField2 = DiscreteBit.Field(20,'testBit','test bit is happy','test bit is not happy')
        self.assertRaises(Exception.A429MsgStructureError,baseMessage.addField,overlappingField2)

    def testMessageValidityCheck(self):
        '''
        Test a en exception is raised when attempting to unpack and invalid message
        '''
        baseMessage = Message.Message('baseMessage', 'odd')
        self.assertRaises(Exception.A429InvalidMessage,baseMessage.unpack,0b00000000000000000000000011110101)
        baseMessage.changeParityConvention('even')
        self.assertRaises(Exception.A429InvalidMessage,baseMessage.unpack,0b10000000000000000000000011110101)

    def testDataCanBeCleared(self):
        '''
        Ensure the clear data function perform as expected
        '''
        baseMessage = Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        self.assertEqual(baseMessage.pack(), 0b10000000000000000000000011110101, "Label Not Packed Properly")
        baseMessage.clearFields()
        self.assertRaisesRegexp(Exception.A429NoData,"label",baseMessage.pack)

if __name__ == "__main__":
    unittest.main()