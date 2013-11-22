'''
Created on 2013-11-11

@author: nicolas
'''

import A429MsgField
import A429Exception

class ParityBit(A429MsgField.A429MsgField):
    '''
    This class is part of an ensemble of classes
    that can be used as an utility for packing and unpacking A429 messages.
    ParityBit managing the parity bit.
    '''
    
    def __repr__(self):
        return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                              self.__class__.__name__,
                                              id(self),
                                              repr(A429MsgField.A429MsgField))

    def __init__(self,parityConvention='odd'):
        '''
        Init a parity bit field.
        parity convention can either be:
        - 'odd' if the bit sum in the final A429 word shall be odd
        - 'even' if the bit sum in the final A429 word shall be even
        Any other parity convention will raise an exception
        '''
        self._parityConvention = None
        self._value = None
        
        '''
        Simply declare an 1 bit field at lsb 32, and keep
        track of the parity convention
        '''
        A429MsgField.A429MsgField.__init__(self, 32, 1, 'parity')
        
        self.setConvention(parityConvention)
        
    def setConvention(self,parityConvention):
        '''
        set the parity convention
        If a value is set and the parity convention is changing, revert
        the parity bit
        '''
        
        oldConvention = self._parityConvention
        
        if type(parityConvention)!=type(str()):
            raise A429Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
        elif parityConvention is not 'odd' and parityConvention is not'even':
            raise A429Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
       
        self._parityConvention = parityConvention
        
        if self._value is not None:
            if self._parityConvention != oldConvention:
                self._value = ( 0 if self._value == 1 else 1)
                
    def setData(self,messageValue): 
        ''' set the parity bit value,as a function of the parity convention
        This function expect the bit value passed as a integer
        '''
        if type(messageValue)!=type(int()):
            raise A429Exception.A429Exception('message value is expected as integer')
        else:
            count = sum( [messageValue&(1<<i)>0 for i in range(31)] )
            
            if count%2 is 0: # the message content is even
                if self._parityConvention is 'odd':
                    self._value = 1
                else:
                    self._value = 0
            else:
                if self._parityConvention is 'odd':
                    self._value = 0
                else:
                    self._value = 1

    def getData(self): 
        ''' get the bit value '''
        if self._value is None:
            raise A429Exception.A429NoData(self.name)
        else:
            return self._value
                    
    def pack(self):
        '''
        Return the 32 bits word corresponding to an A429 message with the bit data (all other bits at zero)
        '''   
        if self._value is None:
            raise A429Exception.A429NoData(self.name)
        else:
            return A429MsgField.A429MsgField.pack(self,int(self._value))   
    
    def unpack(self,A429word):
        """ set the bit value given a 32 bit ARINC 429 message value """ 
        self._value = bool(A429MsgField.A429MsgField.unpack(self,A429word)) 
        