'''
Created on 2013-11-16

@author: nicolas
'''

import A429LabelField
import A429ParityBit
import A429Exception

class Message(object):
    '''
    This class present functionalities to pack and unpack
    A429 messages. It does not contain any data, but rather contain a list 
    of field, which all contain data in 'engineering' units, as well as the info required to
    pack the data
    TODO: add clear representation
    '''
    def __init__(self,name,parity='odd'):
        '''
        Create an A429 Message by simply adding a label and a parity bit
        Note that the parity is odd by default but can be modified as necessary
        '''
        self._name = name
        self._fields = list()
        self.fieldAdditionRules = (self.__field_overlaps,self.__field_name_already_exist)
         
        self.addField(A429LabelField.LabelField())
        self.addField(A429ParityBit.ParityBit(parity))
        
    def __contain_a_single_label(self):
        '''
        Return True if the message contains a single label field, False otherwise
        '''
        return [isinstance(A429LabelField.LabelField,field) for field in self._fields].count(True)==1
    
    def __contain_a_single_parity(self):
        '''
        Return True if the message contains a single parity field, False otherwise
        '''
        return [isinstance(A429ParityBit.ParityBit,field) for field in self._fields].count(True)==1
         
    def getFieldIndex(self,fieldName):
        '''
        Given a field name, this function return the field index
        (field are ordered by lsb ascending)
        If more that one label share the same name, an exception is returned
        '''
        try: 
            return [index for index , field in enumerate(self._fields) if field.name == fieldName][0]
        except:
            return None
       
    def setLabel(self,label):
        '''
        Set the label corresponding to this message
        TODO: test
        '''
        self.setFieldValueByName('label',label)
 
    def changeParityConvention(self,parityConvention):
        '''
        Change the parity convention for the label
        'odd' is used by default at the message creation
        Parity need to be a string of value 'odd' or 'even'
        TODO: test
        '''
        try:
            parityField = [field for field in self._fields if field.name == 'parity'][0]
            parityField.setConvention(parityConvention)   
        except:
            raise A429Exception.A429MsgStructureError("Message {} has no label field".format(self._name))
    
    def __field_overlaps(self,newField):
        '''
        Return True if the new field bits overlap with
        a field in the message
        '''
        return any([(field.getFootPrint()&newField.getFootPrint()) != 0 for field in self._fields])
    
    def __field_name_already_exist(self,newField):
        '''
        Return True if a field with a similar name already exists
        '''
        return any([(field.name == newField.name) for field in self._fields])
        
    def canThisFieldBeAdded(self,newField):
        '''
        return True if the field passed as argument
        can be added :
        - it does not overlap with any existing field)
        - its name does not correspond to an existing field
        TODO test
        '''        
        for isInvalidField in self.fieldAdditionRules:
            if isInvalidField(newField) : return False

        return True
    
    def addField(self,field):
        '''
        Add a field and reorder the message fields by LSB
        An exception is raised if the field cannot be added (not 
        enougth room or same name)
        TODO test
        '''
        if self.canThisFieldBeAdded(field):
            self._fields.append(field)
            sorted(self._fields, key=lambda field: field.lsb)  # sort list by LBS
        else: 
            if self.__field_name_already_exist(field):
                raise A429Exception.A429MsgStructureError('Field with name {fieldName} already exists\
                                                           in message {messageName}'.format(fieldName=field.name),
                                                                                            messageName=self._name)
            else:
                raise A429Exception.A429MsgStructureError('This fields overlap with existing fields in the message')
    
    def setFieldValueByName(self,fieldName,value):
        '''
        Set the field value given its name 
        TODO: test
        '''
        try:
            labelField = [field for field in self._fields if field.name == fieldName][0]
            labelField.setData(value)   
        except:
            raise A429Exception.A429MsgStructureError("Message {} has no label field".format(self._name))
    
    def clearFields(self):
        '''
        clear all fields values
        TODO test
        '''
        for field in self._fields:
            field.clear()
    
    def areAllFieldValuesSet(self):
        '''
        Return true if all label in the field got their values set
        '''
        field_to_set = [field for field in self._fields if field.name != "parity"]
        return all(field.is_data_set() for field in field_to_set)
    
    def pack(self):
        '''
        Return the 32 bit word that correspond to this message
        with the values currently set
        '''
        field_to_set = [field for field in self._fields if field.name != "parity"]
        if not self.areAllFieldValuesSet():
            listOfNotSetField = [field.name for field in field_to_set if not field.is_data_set()]
            raise A429Exception.A429NoData(fieldName=','.join(listOfNotSetField))
        else:
            word = 0
            for field in field_to_set:
                word = word | field.pack()
            parityField = [field for field in self._fields if field.name == 'parity'][0]
            parityField.setData(word)
            word = word | parityField.pack()  

            return word
    
    def unpack(self,word):
        '''
        Given a 32 bit word, set all the fields values
        '''
        for field in self._fields:
                field.unPack(word)
    
  
        