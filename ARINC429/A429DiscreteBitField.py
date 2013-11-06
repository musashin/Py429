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
        