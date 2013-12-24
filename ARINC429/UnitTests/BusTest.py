__author__ = 'nicolas'

import unittest
import Bus
import Exception
import Message


class BusConstruction(unittest.TestCase):
    '''
    Test construction of an ARINC 429 bus
    '''

    def testAddingMessage(self):
         baseMessage1 = Message.Message('baseMessage1', 'odd')
         baseMessage1.setLabel('255')
         baseMessage2 = Message.Message('baseMessage2', 'odd')
         baseMessage2.setLabel('355')
         testBus = Bus.Bus('testBus')
         testBus.addMessage(baseMessage1)
         testBus.addMessage(baseMessage2)

         expectedDico = {(0255, None): baseMessage1, (0355, None): baseMessage2}
         actualDico = testBus._messages

         self.assertDictEqual(expectedDico, actualDico ,'Bus construct not working')

    def testRemovingMessage(self):

         baseMessage1 = Message.Message('baseMessage1', 'odd')
         baseMessage1.setLabel('255')
         baseMessage2 = Message.Message('baseMessage2', 'odd')
         baseMessage2.setLabel('355')
         testBus = Bus.Bus('testBus')
         testBus.addMessage(baseMessage1)
         testBus.addMessage(baseMessage2)

         expectedDico = {(0255, None): baseMessage1, (0355, None): baseMessage2}
         actualDico = testBus._messages

         self.assertDictEqual(expectedDico, actualDico ,'Bus construct not working')

         testBus.removeMessage(baseMessage1)

         expectedDico = { (0355, None): baseMessage2}
         actualDico = testBus._messages

         self.assertDictEqual(expectedDico, actualDico ,'Bus construct not working')

    def testNoDuplicate(self):
        '''
        Verify an exception is raised when attempting to add
        a message in a bus that has he same SDI/Label combinaison
        than a message already existing
        '''
        baseMessage1 = Message.Message('baseMessage1', 'odd')
        baseMessage1.setLabel('255')
        baseMessage2 = Message.Message('baseMessage2', 'odd')
        baseMessage2.setLabel('255')
        testBus = Bus.Bus('testBus')
        testBus.addMessage(baseMessage1)

        self.assertRaises(Exception.A429MsgStructureError, testBus.addMessage, baseMessage2)
