__author__ = 'nicolas'

import unittest
import XMLSerializer
import Bus
import Message
import DiscreteBit

class testSerialization(unittest.TestCase):
    '''
    Test protections against data that does not correspond to the field type
    '''

    def test(self):

        testBus = Bus.Bus('testBus')

        testMessage1 = Message.Message('baseMessage', 'odd')
        testMessage1.setLabel('257')
        testMessage1.addField(DiscreteBit.Field(10,'testBit','test bit is happy','test bit is not happy'))
        testMessage1.setFieldValueByName('testBit',True)
        testMessage1.addField(DiscreteBit.Field(15,'bobo','test bit is happy','test bit is not happy'))

        testBus.addMessage(testMessage1)

        with open("/home/nicolas/Desktop/test.xml", 'w') as XMLFile:

            XMLSerializer.serialize(XMLFile,testBus,True)