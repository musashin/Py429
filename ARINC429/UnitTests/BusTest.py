__author__ = 'nicolas'

import unittest
import Bus
import Exception
import Message


class BusConstruction(unittest.TestCase):
    '''
    Test construction of an ARINC 429 bus
    '''

    def testCanBuildBus(self):
         baseMessage1 = Message.Message('baseMessage1', 'odd')
         baseMessage1.setLabel('255')
         baseMessage2 = Message.Message('baseMessage2', 'odd')
         baseMessage2.setLabel('355')
         testBus = Bus.Bus('testBus')
         testBus.addMessage(baseMessage1)
         testBus.addMessage(baseMessage2)
         self.assertEqual(len(testBus._messages), 2, 'Bus construct not working')
         expectedDico = {('255', None): baseMessage2, ('355', None): baseMessage1}
         madeDico = testBus._messages
         self.assertDictEqual(expectedDico, madeDico ,
                              'Bus construct not working')


    def testNoDuplicate(self):
        '''
        Verify an exception is raised if duplicate ,messages are raised
        '''