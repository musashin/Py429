'''
Created on 2013-10-17

@author: nicolas
'''

import A429MsgField
import A429Exception


class LabelField(A429MsgField.A429MsgField):
    '''
    This field is use for Label of ARINC 429 messages.
    As such, it is always on bit 1 to 8, and limited to
    an Octal number on 8 bits
    '''

    def __init__(self,label):
        '''
        Simply declare an 8 bits field at lsb 1 
        This function expect label number passed on octal form
        The number is expected as a string so that we always treat the passed
        value as an integer.
        '''
        A429MsgField.A429MsgField.__init__(self, 1, 8, 'label')
        self.setData(label)
     
    def setData(self,label): 
        ''' set the label property '''
        if type(label)!=type(str()):
            raise A429Exception.A429Exception('Label should be given as strings')
        try:
            self._label  = int(label,8)
        except ValueError:
            raise A429Exception.A429MsgRangeError(self.name,\
                                                  0377,\
                                                  self._label) 
    def pack(self):
        '''
        Return the 32 bits word corresponding to an A429 message with the label data (all other bits at zero)
        '''   
        reverted = int('{:08b}'.format(self._label)[::-1], 2) #let's reverse the bit
        return A429MsgField.A429MsgField.pack(self,reverted)
        
    def unpack(self,A429word):
        """ return the value given a 32 bit ARINC 429 message value """ 
        labelrev= A429MsgField.A429MsgField.unpack(self,self.A429word)
        return '{:08b}'.format(labelrev)[::-1], 8