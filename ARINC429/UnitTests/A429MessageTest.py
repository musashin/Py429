'''
Created on 2013-12-04

@author: nicolas
'''
import unittest
import A429Message
import A429Exception

class TestPacking(unittest.TestCase):
    '''
    Test the packing functionality
    '''
    
    def testBaseMessage(self):
        baseMessage = A429Message.Message('baseMessage', 'odd')
        baseMessage.setLabel('257')
        self.assertEqual(baseMessage.pack(), 0b10000000000000000000000011110101, "Label Not Packed Properly")

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


    def testCannotPackWhenDataNotSet(self):
        '''
        Ensure a message which does not have all
        fields set cannot be packed
        '''

if __name__ == "__main__":
    unittest.main()