'''
Created on 2 mai 2013

@author: nulysse
'''

import A429Exception
import bitarray

class A429MsgField(object):
    '''
    This classes represents a an A429 message.
    As such it is characterized by the position and size of the field, indicated by:
        - Field LSB (note that the LSB is indexed 1, to match common data dictionaries definitions)
        - Field Size in bits
        - Name is a human readable name used for various purposes, including error reporting
    This class also offers method to pack (in that case, simply take a value and store it at the appropriate place
    with a 32 bit value) and unpack
        
    '''
    def __init__(self,lsb,size,name,parent_label,parent_sdi):
        '''
        Constructor
        '''
        self.lsb = lsb
        self.size = size
        self.name = name
        self.parent_label = parent_label
        self.parent_sdi = parent_sdi
        
    def unpack(self,A429word):
            pass
        
    def pack(self,value):
        '''
        Take an integer value and return a bit array representing
        the value packed at location corresponding to the message definition
        
        Warning: a A429MsgRangeError is raised if the field is not
        large enougth to store the value.
        '''
        if(abs(value)>(2**self.size)):
            raise A429Exception.A429MsgRangeError(self.parent_label,\
                                                  self.parent_sdi,\
                                                  self.name,\
                                                  (2**self.size).__str__(),\
                                                  '{value}')
        else:
            A429word = bitarray(32)
            A429word = bitarray.bitarray(bin(value<<(self.lsb-1))[2:])
            return A429word
    