'''
Created on 2013-11-05

@author: nicolas
'''

import MessageField
import Exception

class Field(MessageField.Field):
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
                                                            repr(MessageField.Field))
        else:
            return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                                  self.__class__.__name__,
                                                  id(self),
                                                  repr(MessageField.Field))

    def __init__(self,bitIndex,bitName,meaningWhenSet,meaningWhenNotSet):
        '''
        Simply declare a 1 bit field at the specified position
        Note: LSB index is 1
        '''
        MessageField.Field.__init__(self,bitIndex, 1,bitName)
        self._value = None
        self._meaningWhenSet = meaningWhenSet
        self._meaningWhenNotSet = meaningWhenNotSet
    
    def is_data_set(self):
        return self._value is not None
        
    def setData(self,bitValue): 
        ''' set the bit value
        This function expect the bit value passed as a boolean
        '''
        if type(bitValue) != type(bool()):
            raise Exception.A429Exception('Bit are expected as bool')
        else:
            self._value  = bitValue
            
    def getData(self): 
        ''' get the bit value '''
        if self._value is None:
            raise Exception.A429NoData(self.name)
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
            raise Exception.A429NoData(self.name)
        else:
            return MessageField.Field.pack(self,int(self._value))
        
    def unpack(self,A429word):
        """ set the bit value given a 32 bit ARINC 429 message value """ 
        self._value = bool(MessageField.Field.unpack(self,A429word))

    def __eq__(self, other):
        '''
        Define the == operator to compare field definition AND parity convention
        '''
        if isinstance(other, Field):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        '''
        Define the != operator to compare field definition AND parity convention
        '''
        result = self.__eq__(other)
        '''
        Define the != operator to compare size, lsb and name
        '''
        if result is NotImplemented:
            return result
        return not result

    def serialize(self, stream, serializeState = False ,  parentElement = None):
        '''
        Serialize field to XML
        '''
        from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

        fieldElement = super(Field,self).serialize(stream,serializeState,parentElement)

        fieldElement.set('type',__name__)
        fieldElement.set('meaningWhenSet', self._meaningWhenSet)
        fieldElement.set('meaningWhenNotSet', self._meaningWhenNotSet)

        if serializeState:
            fieldElement.text = str(self._value)

        return fieldElement