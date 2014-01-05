'''
Created on 2013-11-16

@author: nicolas
'''

import Label
import Parity
import Exception

class Message(object):
    '''
    This class present functionalities to pack and unpack
    A429 messages. It does not contain any data, but rather contain a list 
    of field, which all contain data in 'engineering' units, as well as the info required to
    pack the data
    '''
    def __init__(self,name,parity='odd'):
        '''
        Create an A429 Message by simply adding a label and a parity bit
        Note that the parity is odd by default but can be modified as necessary
        '''
        self.name = name
        self._fields = list()
        self.fieldAdditionRules = (self.__field_overlaps,self.__field_name_already_exist)
         
        self.addField(Label.Field())
        self.addField(Parity.Field(parity))

    def __repr__(self):

        listOfFields= ','.join([field.name for field in self._fields])

        return '<%s.%s object at 0x%x [contain %s]>'%(self.__module__,
                                              self.__class__.__name__,
                                             id(self),
                                             listOfFields)
    def __contain_a_single_label(self):
        '''
        Return True if the message contains a single label field, False otherwise
        '''
        return [isinstance(Label.Field,field) for field in self._fields].count(True)==1
    
    def __contain_a_single_parity(self):
        '''
        Return True if the message contains a single parity field, False otherwise
        '''
        return [isinstance(Parity.Field,field) for field in self._fields].count(True)==1

       
    def setLabel(self,label):
        '''
        Set the label corresponding to this message
        '''
        self.setFieldValueByName('label',label)

    def getLabel(self):
        '''
        Get the label corresponding to this message
        '''
        return self.getFieldValueByName('label')

    def getSDI(self):
        '''
        Get the SDI corresponding to this message
        SDI are optionals: if this message has no SDI,
        return None
        '''
        try:
            return self.getFieldValueByName('sdi')
        except:
            return None

    def changeParityConvention(self,parityConvention):
        '''
        Change the parity convention for the label
        'odd' is used by default at the message creation
        Parity need to be a string of value 'odd' or 'even'
        '''
        try:
            parityField = [field for field in self._fields if field.name == 'parity'][0]
            parityField.setConvention(parityConvention)   
        except:
            raise Exception.A429MsgStructureError("Message {} has no label field".format(self.name))
    
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
        '''        
        for isInvalidField in self.fieldAdditionRules:
            if isInvalidField(newField) : return False

        return True
    
    def addField(self,field):
        '''
        Add a field and reorder the message fields by LSB
        An exception is raised if the field cannot be added (not 
        enough room or same name)
        '''
        if self.canThisFieldBeAdded(field):
            self._fields.append(field)
            sorted(self._fields, key=lambda field: field.lsb)  # sort list by LBS
        else: 
            if self.__field_name_already_exist(field):
                raise Exception.A429MsgStructureError('Field with name {fieldName} already exists\
                                                           in message {messageName}'.format(fieldName=field.name,
                                                                                            messageName=self.name))
            else:
                raise Exception.A429MsgStructureError('This fields overlap with existing fields in the message')

    def removeField(self,fieldName):
        '''
        Remove a message field given its name
        '''
        self._fields = [field for field in self._fields if not field.name==fieldName]

    def isFieldInMessage(self,fieldName):
        '''
        Return True if the field with a given name
        is part of the message, False otherwise
        '''
        return any(field.name == fieldName for field in self._fields)

    def setFieldValueByName(self,fieldName,value):
        '''
        Set the field value given its name
        '''
        try:
            labelField = [field for field in self._fields if field.name == fieldName][0]
            labelField.setData(value)   
        except IndexError:
            raise Exception.A429MsgStructureError("Message {} has no label field".format(self.name))

    def getFieldValueByName(self,fieldName):
        '''
        Get the field value given its name
        '''
        try:
            labelField = [field for field in self._fields if field.name == fieldName][0]
            return labelField.getData()
        except IndexError:
            raise Exception.A429MsgStructureError("Message {} has no label field".format(self.name))
    
    def clearFields(self):
        '''
        clear all fields values
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
            raise Exception.A429NoData(fieldName=','.join(listOfNotSetField))
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
        parityField = [field for field in self._fields if field.name == 'parity'][0]
        if not parityField.isMessageValid(word):
            raise Exception.A429InvalidMessage(label=self.name)

        else:
            for field in self._fields:
                    field.unpack(word)
    
  
    def serialize(self, stream, serializeState = False , parentElement = None):
        '''
        Serialize Message to XML
        '''

        from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

        if parentElement is None:
            messageElement = Element('Message')
        else:
            messageElement = SubElement(parentElement, 'Message')

        messageElement.set('name',self.name)

        for field in self._fields:
            field.serialize(stream,serializeState, messageElement)

        return messageElement