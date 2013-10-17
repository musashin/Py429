'''
Created on 2 mai 2013

@author: nulysse
'''

import A429Exception

class A429MsgField(object):
    '''
    This classes represents a an A429 message field.
    As such it is characterized by the position and size of the field, indicated by:
        - Field LSB (note that the LSB is indexed 1, to match common data dictionaries definitions)
        - Field Size in bits
        - Name is a human readable name used for various purposes, including error reporting
    This class also offers method to pack (in that case, simply take a value and store it at the appropriate place
    with a 32 bit value) and unpack
        
    '''
    def __init__(self,lsb,size,name):
        '''
        Constructor
        '''
        self.lsb = lsb
        
        if lsb<1:
            raise A429Exception.A429MsgStructureError("LSB cannot be lower than 1")
            
        self.size = size
        
        if (lsb+size)>33:
            raise A429Exception.A429MsgStructureError("Field cannot exceed bit 32")
        
        self.name = name
        self.data = None
        
    def unpack(self,A429word):
        """ return the value given a 32 bit ARINC 429 message value """ 
        if (A429word<0):
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  0,\
                                                  '{A429word}')
        elif (A429word>0xFFFFFFFF): 
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  0xFFFFFFFF,\
                                                  '{A429word}')
        else:
            return A429word>>(self.lsb-1)                                                                        
        
    def pack(self,value):
        """
        Take an integer value and return a bit array representing
        the value packed at location corresponding to the message definition
        
        Warning: a A429MsgRangeError is raised if the field is not
        large enough to store the value.
        """
        if(abs(value)>((2**self.size)-1)):
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  ((2**self.size)-1).__str__(),\
                                                  '{value}')
        elif value<0:
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  "0",\
                                                  '{value}')
        else:
            self.data = value<<(self.lsb-1)
            
            return self.data
    