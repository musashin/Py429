'''
Created on 2013-11-12

@author: nicolas
'''
import unittest
import Label
import Field
import Exception

class ExceptionRaise(unittest.TestCase):

    def testCanRepresentItself(self):
        try:
            Field.Field()
        except Exception:
            self.fail("LabelField cannot represent itself")

    def testInvalidConventions(self):
        """ A429ParityBit should fail for parity convention other than odd or even"""
        self.assertRaises(Exception.A429Exception, Field.Field, "test")
        self.assertRaises(Exception.A429Exception, Field.Field, "")
        self.assertRaises(Exception.A429Exception, Field.Field,5)

class testNoData(unittest.TestCase):
    '''
    Test situation where the bit field is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the bit field was not set
        '''
        bit = Field.Field('odd')
        self.assertRaises(Exception.A429NoData,bit.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the  bit field was not set
        '''
        bit = Field.Field('odd')
        self.assertRaises(Exception.A429NoData,bit.pack)
        
    def testClearing(self):
        '''
        Test data clearing
        '''
        bit = Field.Field('odd')
        bit.setData(0x00)
        bit.clear()
        self.assertRaises(Exception.A429NoData,bit.pack)
              
class testParity(unittest.TestCase):
    '''
    Test Parity Pack/Unpack Algorithm
    '''
    cases = [   {'word':0b001100101,'parity':'even'},
                {'word':0b1110100100101,'parity':'odd'},
                {'word':0b10100101001010,'parity':'even'},
                {'word':0b10000010001,'parity':'odd'}]
       
    def testEmptyMessage(self):
        '''
        Verify Case of no bit set in message
        '''
        parityBitOdd = Field.Field('odd')
        parityBitOdd.setData(0x00)
        self.assertEqual(parityBitOdd.pack(),1<<31, "Parity Not Calculated Properly")
    
        parityBitEven = Field.Field('even')
        parityBitEven.setData(0x00)
        self.assertEqual(parityBitEven.pack(),0, "Parity Not Calculated Properly")
        
    def testFullMessage(self):
        '''
        Verify Case of all bits set in message
        '''
        parityBitOdd = Field.Field('odd')
        parityBitOdd.setData(0x7FFFFFFF)
        self.assertEqual(parityBitOdd.pack(),0, "Parity Not Calculated Properly")
    
        parityBitEven = Field.Field('even')
        parityBitEven.setData(0x7FFFFFFF)
        self.assertEqual(parityBitEven.pack(),1<<31, "Parity Not Calculated Properly")
        
    def testAFewCases(self):
        '''
        Further test the algorithm with a few samples cases manually generated
        '''
        parityBitOdd = Field.Field('odd')
        parityBitEven = Field.Field('even')
        for case in self.cases:
            parityBitOdd.setData(case['word'])
            self.assertEqual(parityBitOdd.pack(),1<<31 if case['parity']=='even' else 0, "Parity Not Calculated Properly")
            parityBitEven.setData(case['word'])
            self.assertEqual(parityBitEven.pack(),0 if case['parity']=='even' else 1<<31, "Parity Not Calculated Properly")      
   
    def testConventionChange(self):
        '''
        Further test the algorithm with a few samples cases manually generated
        '''
        parityBit = Field.Field('odd')
        for case in self.cases:
            parityBit.setConvention('odd')
            parityBit.setData(case['word'])
            self.assertEqual(parityBit.pack(),1<<31 if case['parity']=='even' else 0, "Parity Not Calculated Properly")
            parityBit.setConvention('even')
            self.assertEqual(parityBit.pack(),0 if case['parity']=='even' else 1<<31, "Parity Not Calculated Properly")      

    def testMessageValidityTest(self):
        '''
        Test the function that determine the message validity
        '''
        parityBitOdd = Field.Field('odd')
        parityBitEven = Field.Field('even')
        for case in self.cases:
            self.assertEqual(parityBitOdd.isMessageValid(case['word']),False if case['parity']=='even' else True, "Parity Not Calculated Properly")
            parityBitEven.setData(case['word'])
            self.assertEqual(parityBitEven.isMessageValid(case['word']),True if case['parity']=='even' else False, "Parity Not Calculated Properly")

if __name__ == "__main__":
   
    unittest.main()