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
        
    def getFieldIndex(self,fieldName):
        '''
        Given a field name, this function return the field index
        (field are ordered by lsb ascending)
        If more that one label share the same name, an exception is returned
        '''
        pass
        
    def setLabel(self,label):
        '''
        Set the label corresponding to this message
        '''
        for field in self._fields:
            pass
        
    def changeParityConvention(self,parity):
        '''
        Change the parity convention for the label
        'odd' is used by default at the message creation
        Parity need to be a string of value 'odd' or 'even'
        '''
        pass
    
    def validateMessage(self):
        '''
        Validate this message is valid, return
        True if this is the case, False otherwise:
        - it does not overlap with any existing field)
        - its name does not correspond to an existing field
        - there is at least one 'label' field and one 'parity' field
        - TODO: more for BDC label
        '''
        pass
    
    def canThisFieldBeAdded(self,field):
        '''
        return True if the field passed as argument
        can be added :
        - it does not overlap with any existing field)
        - its name does not correspond to an existing field
        '''
        pass
    
    def clearFields(self):
        '''
        clear all fields values
        '''
        pass
    
    def areAllFieldValuesSet(self):
        '''
        Return true if all label in the field got their values set
        '''
        pass
    
    def pack(self):
        '''
        Return the 32 bit word that correspond to this message
        with the values currently set
        '''
        pass
    
    def unpack(self,word):
        '''
        Given a 32 bit word, set all the fields values
        '''
        pass
    
    def setFieldValueByName(self,fieldName,value):
        '''
        Set the field value given its name 
        '''
        pass
    
    def setFieldValueByIndex(self,fieldIndex,value):
        '''
        Set the field value given its index (field are ordered
        by lsb ascending)
        '''
        pass
        
    def addField(self,field):
        '''
        Add a field and reorder the message fields by LSB
        '''
        self._fields.append(field)
        sorted(self._fields, key=lambda field: field.lsb)  # sort list by LBS
        