'''
Created on 2013-11-16

@author: nicolas
'''

import A429LabelField
import A429ParityBit

class Message(object):
    '''
    This class present functionalities to pack and unpack
    A429 messages. It does not contain any data, but rather contain a list 
    of field, which all contain data in 'engineering' units, as well as the info required to
    pack the data
    '''

    def __init__(self,parity='odd'):
        '''
        Create an A429 Message by simply adding a label and a parity bit
        Note that the parity is odd by default but can be modified as necessary
        '''
        self._fields = list()
        self.addField(A429LabelField.LabelField())
        self.addField(A429ParityBit.ParityBit(parity))
        
    def setLabel(self,label):
        
        for field in self._fields:
            
        
    def addField(self,field):
        '''
        Add a field and reorder the message fields by LSB
        '''
        self._fields.append(field)
        sorted(self._fields, key=lambda field: field.lsb)  # sort list by LBS
        