'''
Created on 2013-11-11

@author: nicolas
'''

import MessageField
import Exception

class Field(MessageField.Field):
    '''
    This class is part of an ensemble of classes
    that can be used as an utility for packing and unpacking A429 messages.
    ParityBit managing the parity bit.
    '''
    
    def __repr__(self):
        return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                              self.__class__.__name__,
                                              id(self),
                                              repr(MessageField.Field))

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
        MessageField.Field.__init__(self, 32, 1, 'parity')
        
        self.setConvention(parityConvention)
    
    def is_data_set(self):
        return self._value is not None
        
    def setConvention(self,parityConvention):
        '''
        set the parity convention
        If a value is set and the parity convention is changing, revert
        the parity bit
        '''
        
        oldConvention = self._parityConvention
        
        if type(parityConvention)!=type(str()):
            raise Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
        elif parityConvention is not 'odd' and parityConvention is not'even':
            raise Exception.A429Exception("Parity Convention {} is not handled".format(parityConvention))
       
        self._parityConvention = parityConvention
        
        if self._value is not None:
            if self._parityConvention != oldConvention:
                self._value = ( 0 if self._value == 1 else 1)
                
    def setData(self,messageValue): 
        ''' set the parity bit value,as a function of the parity convention
        This function expect the bit value passed as a integer
        '''
        if type(messageValue)!=type(int()):
            raise Exception.A429Exception('message value is expected as integer')
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

    def isMessageValid(self,A429word):
        '''
        Determine if the message is valid given the message content and the parity convention
        @param A429word: 32 bit packed ARINC 429 word
        @return: True if the message is valid
        '''
        count = sum( [A429word&(1<<i)>0 for i in range(32)] )

        if count%2 is 0: # the message content is even
            if self._parityConvention is 'odd':
                return False
            else:
                return True
        else:
            if self._parityConvention is 'odd':
                return True
            else:
                return False

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

    def serialize(self, stream, parentElement = None):
        '''
        Serialize Field to XML
        '''
        from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

        fieldElement = super(Field,self).serialize(stream,parentElement)

        fieldElement.set('type',__name__)
        fieldElement.set('convention', self._parityConvention)

        return fieldElement