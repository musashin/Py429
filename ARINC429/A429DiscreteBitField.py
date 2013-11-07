'''
Created on 2013-11-05

@author: nicolas
'''

import A429MsgField
import A429Exception

class DiscreteBitField(object):
    '''
    This subclass of A429MsgField is part of an ensemble of classes
    that can be used as an utility for packing and unpacking A429 messages.
    LabelField is more specifically dedicated to managing bits in discrete
    ARINC 429 messages.
    '''
    
    def __repr__(self):
        if self._value is not None:
            return '<%s.%s object at 0x%x, value %s [%s]>'%(self.__module__,
                                                            self.__class__.__name__,
                                                            id(self),
                                                            str(self._value),
                                                            repr(self._field))
        else:
            return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                                  self.__class__.__name__,
                                                  id(self),
                                                  repr(self._field))

    def __init__(self,bitIndex,bitName,meaningWhenSet,meaningWhenNotSet):
        '''
        Simply declare a 1 bit field at the specified position
        Note: LSB index is 1
        '''
        self._field = A429MsgField.A429MsgField(bitIndex, 1,bitName)
        self._value = None
        self._meaningWhenSet = meaningWhenSet
        self._meaningWhenNotSet = meaningWhenNotSet
        
    def setData(self,bitValue): 
        ''' set the bit value
        This function expect the bit value passed as a boolean
        '''
        if type(bitValue)!=type(bool()):
            raise A429Exception.A429Exception('Bit are expected as bool')
        else:
            self._value  = bitValue
            
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
        