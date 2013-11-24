'''
Created on 2013-10-17

@author: nicolas
'''

import A429MsgField
import A429Exception

class LabelField(A429MsgField.A429MsgField):
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
                                                            repr(A429MsgField.A429MsgField))
        else:
            return '<%s.%s object at 0x%x [%s]>'%(self.__module__,
                                                  self.__class__.__name__,
                                                  id(self),
                                                  repr(A429MsgField.A429MsgField))

    def __init__(self):
        '''
        Simply declare an 8 bits field at lsb 1
        '''
        A429MsgField.A429MsgField.__init__(self,1, 8, 'label')
        self._label = None
     
    def setData(self,label): 
        ''' set the label property 
        This function expect label number passed on octal form
        The number is expected as a string so that we always treat the passed
        value as an integer.
        '''
        if type(label)!=type(str()):
            raise A429Exception.A429Exception('Label should be given as strings')
        try:
            self._label  = int(label,8)
        except ValueError:
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  0377,\
                                                  label) 
        if(self._label<0):
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  0,\
                                                  label) 
    def getData(self): 
        ''' get the label property '''
        if self._label is None:
            raise A429Exception.A429NoData(self.name)
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
            raise A429Exception.A429NoData(self.name)
        else:
            reverted = int('{:08b}'.format(self._label)[::-1], 2) #let's reverse the bit
            return A429MsgField.A429MsgField.pack(self,reverted)
        
    def unpack(self,A429word):
        """ set the label given a 32 bit ARINC 429 message value """ 
        labelrev= A429MsgField.A429MsgField.unpack(self,A429word)
        self._label= int('{:08b}'.format(labelrev)[::-1], 2)