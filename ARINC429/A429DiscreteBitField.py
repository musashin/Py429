'''
Created on 2013-11-05

@author: nicolas
'''

import A429MsgField
import A429Exception

class DiscreteBitField(A429MsgField.A429MsgField):
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
                                                            repr(A429MsgField.A429MsgField))
        else:
            return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                                  self.__class__.__name__,
                                                  id(self),
                                                  repr(A429MsgField.A429MsgField))

    def __init__(self,bitIndex,bitName,meaningWhenSet,meaningWhenNotSet):
        '''
        Simply declare a 1 bit field at the specified position
        Note: LSB index is 1
        '''
        A429MsgField.A429MsgField.__init__(self,bitIndex, 1,bitName)
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
            raise A429Exception.A429NoData(self.name)
        else:
            return self._value
            
    def clear(self):
        '''
        Clear the label value
        '''
        self._value = None
             
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
        