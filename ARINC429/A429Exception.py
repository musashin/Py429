'''
Created on 2 mai 2013

@author: nulysse
'''

class A429Exception(Exception):
    '''
    Exception raised whenever an A429 structure is not coherent (ex: overlapping field)
     Attributes:
        Label  -- label of the message that raises the error
        SDI    -- SDI of the message that raises the error
        msg    -- explanation of the error
    '''
    def __init__(self,message,label='unknown',sdi='unknown'):
        self.label = label
        self.sdi = sdi
        self.message = message
    def __str__(self):
        return "Error in Message " \
                + "]  Label-" + self.label + "-" \
                + "  SDI-" + self.sdi + "-] "\
                + self.message+"\n"
            
class A429MsgStructureError(A429Exception):
    '''
    Exception raised whenever an A429 structure is not coherent (ex: overlapping field)
     Attributes:
        Label  -- label of the message that raises the error
        SDI    -- SDI of the message that raises the error
        msg    -- explanation of the error
    '''
    def __init__(self,msg,label="unknown",sdi="unknown"):
        A429Exception.__init__(self, label, sdi)
        self.msg = msg
    def __str__(self):
        error = super(A429MsgStructureError,self).__str__()
        return error + " : " + self.msg
        
        
class A429MsgRangeError(A429Exception):
    '''
    Exception raised whenever an data exceeds the range of data for a field:
        Label        -- label of the message that raises the error
        SDI          -- SDI of the message that raises the error
        field_name   -- name of the field for which the range is exceeded
        accepted_value    -- max/min accepted value
        current_value     -- current_value
        
    '''
    def __init__(self,field_name,accepted_value,current_value,label="unkown",sdi="unkown"):
        A429Exception.__init__(self, label, sdi)
        self.field_name = field_name
        self.accepted_value = str(accepted_value)
        self.current_value = str(current_value)
        
    def __str__(self):
        error = super(A429MsgRangeError,self).__str__()
        range_msg = "value " + self.current_value + " exceeds " + self.accepted_value
        return error + " : " + range_msg

        