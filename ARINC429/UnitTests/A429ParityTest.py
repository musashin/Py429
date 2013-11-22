'''
Created on 2013-11-12

@author: nicolas
'''
import unittest
import A429LabelField
import A429ParityBit
import A429Exception

class ExceptionRaise(unittest.TestCase):

    def testCanRepresentItself(self):
        try:
            A429ParityBit.ParityBit()
        except Exception:
            self.fail("LabelField cannot represent itself")

    def testInvalidConventions(self):
        """ A429ParityBit should fail for parity convention other than odd or even"""
        self.assertRaises(A429Exception.A429Exception, A429ParityBit.ParityBit, "test")
        self.assertRaises(A429Exception.A429Exception, A429ParityBit.ParityBit, "")
        self.assertRaises(A429Exception.A429Exception, A429ParityBit.ParityBit,5)

class testNoData(unittest.TestCase):
    '''
    Test situation where the bit field is accessed before having been set
    '''
    def testGetDataNoData(self):
        '''
        Call get data when the bit field was not set
        '''
        bit = A429ParityBit.ParityBit('odd')
        self.assertRaises(A429Exception.A429NoData,bit.getData)
    
    def testPackNoData(self):
        '''
        Call pack when the  bit field was not set
        '''
        bit = A429ParityBit.ParityBit('odd')
        self.assertRaises(A429Exception.A429NoData,bit.pack)
        
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
        parityBitOdd = A429ParityBit.ParityBit('odd')
        parityBitOdd.setData(0x00)
        self.assertEqual(parityBitOdd.pack(),1<<31, "Parity Not Calculated Properly")
    
        parityBitEven = A429ParityBit.ParityBit('even')
        parityBitEven.setData(0x00)
        self.assertEqual(parityBitEven.pack(),0, "Parity Not Calculated Properly")
        
    def testFullMessage(self):
        '''
        Verify Case of all bits set in message
        '''
        parityBitOdd = A429ParityBit.ParityBit('odd')
        parityBitOdd.setData(0x7FFFFFFF)
        self.assertEqual(parityBitOdd.pack(),0, "Parity Not Calculated Properly")
    
        parityBitEven = A429ParityBit.ParityBit('even')
        parityBitEven.setData(0x7FFFFFFF)
        self.assertEqual(parityBitEven.pack(),1<<31, "Parity Not Calculated Properly")
        
    def testAFewCases(self):
        '''
        Further test the algorithm with a few samples cases manually generated
        '''
        parityBitOdd = A429ParityBit.ParityBit('odd')
        parityBitEven = A429ParityBit.ParityBit('even')
        for case in self.cases:
            parityBitOdd.setData(case['word'])
            self.assertEqual(parityBitOdd.pack(),1<<31 if case['parity']=='even' else 0, "Parity Not Calculated Properly")
            parityBitEven.setData(case['word'])
            self.assertEqual(parityBitEven.pack(),0 if case['parity']=='even' else 1<<31, "Parity Not Calculated Properly")      
   
    def testConventionChange(self):
        '''
        Further test the algorithm with a few samples cases manually generated
        '''
        parityBit = A429ParityBit.ParityBit('odd')
        for case in self.cases:
            parityBit.setConvention('odd')
            parityBit.setData(case['word'])
            self.assertEqual(parityBit.pack(),1<<31 if case['parity']=='even' else 0, "Parity Not Calculated Properly")
            parityBit.setConvention('even')
            self.assertEqual(parityBit.pack(),0 if case['parity']=='even' else 1<<31, "Parity Not Calculated Properly")      
     
if __name__ == "__main__":
   
    unittest.main()