'''
Created on 2013-11-11

@author: nicolas
'''

import A429MsgField
import A429Exception

class ParityBit(object):
    '''
    This class is part of an ensemble of classes
    that can be used as an utility for packing and unpacking A429 messages.
    ParityBit managing the parity bit.
    '''
    
    def __repr__(self):
        return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                              self.__class__.__name__,
                                              id(self),
                                              repr(self._field))

    def __init__(self,parityConvention='odd'):

        '''
        Simply declare an 1 bit field at lsb 32, and keep
        track of the parity convention
        '''
        self._field = A429MsgField.A429MsgField( 32, 1, 'parity')
        
        if type(parityConvention)!=type(str()):
            raise A429Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
        elif parityConvention is not 'odd' and parityConvention is not'even':
            raise A429Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
       
        self._parityConvention = parityConvention
        self._value = None
        
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
            raise A429Exception.A429NoData(self._field.name)
        else:
            return self._value
                    
    def pack(self):
        '''
        Return the 32 bits word corresponding to an A429 message with the bit data (all other bits at zero)
        '''   
        if self._value is None:
            raise A429Exception.A429NoData(self._field.name)
        else:
            return self._field.pack(int(self._value))   
    
    def unpack(self,A429word):
        """ set the bit value given a 32 bit ARINC 429 message value """ 
        self._value = bool(self._field.unpack(A429word)) 
        