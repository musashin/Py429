'''
Created on 2013-10-17

@author: nicolas
'''

import MessageField
import Exception

class Field(MessageField.Field):
    '''
    This class is part of an ensemble of classes
    that can be used as an utility for packing and unpacking A429 messages.
    LabelField is more specifically dedicated to managing messages label,
    which are located in the bits 1 to 8 with LSB at bit 8.
    '''
    
    def __repr__(self):
        if self._label is not None:
            return '<%s.%s object at 0x%x, Label %s [%s]>'%(self.__module__,
                                                            self.__class__.__name__,
                                                            id(self),
                                                            oct(self._label),
                                                            repr(MessageField.Field))
        else:
            return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                                  self.__class__.__name__,
                                                  id(self),
                                                  repr(MessageField.Field))
    def __init__(self):
        '''
        Simply declare an 8 bits field at lsb 1
        '''
        MessageField.Field.__init__(self,1, 8, 'label')
        self._label = None
    
    def is_data_set(self):
        return self._label is not None
     
    def setData(self,label): 
        ''' set the label property 
        This function expect label number passed on octal form
        The number is expected as a string so that we always treat the passed
        value as an integer.
        '''
        if type(label)!=type(str()):
            raise Exception.A429Exception('Label should be given as strings')
        try:
            self._label  = int(label,8)
        except ValueError:
            raise Exception.A429MsgRangeError(self.name,\
                                                  0377,\
                                                  label) 
        if(self._label<0):
            raise Exception.A429MsgRangeError(self.name,\
                                                  0,\
                                                  label) 
    def getData(self): 
        ''' get the label property '''
        if self._label is None:
            raise Exception.A429NoData(self.name)
        else:
            return self._label
        
    def clear(self):
        '''
        Clear the label value
        '''
        self._label = None
         
    def pack(self):
        '''
        Return the 32 bits word corresponding to an A429 message with the label data (all other bits at zero)
        '''   
        if self._label is None:
            raise Exception.A429NoData(self.name)
        else:
            reverted = int('{:08b}'.format(self._label)[::-1], 2) #let's reverse the bit
            return MessageField.Field.pack(self,reverted)
        
    def unpack(self,A429word):
        """ set the label given a 32 bit ARINC 429 message value """ 
        labelrev= MessageField.Field.unpack(self,A429word)
        self._label= int('{:08b}'.format(labelrev)[::-1], 2)

    def __eq__(self, other):
        '''
        Define the == operator to compare field definition AND label
        '''
        if isinstance(other, Field):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        '''
        Define the != operator to compare field definition AND label
        '''
        result = self.__eq__(other)

        if result is NotImplemented:
            return result
        return not result

    def serialize(self, stream, serializeState = False ,  parentElement = None):
        '''
        Serialize Field to XML
        '''
        from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

        fieldElement = super(Field,self).serialize(stream,serializeState,parentElement)

        fieldElement.set('type',__name__)
        fieldElement.set('label', oct(self._label))

        return fieldElement