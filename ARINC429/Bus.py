__author__ = 'nicolas'


class Bus(object):
    '''
    This class represents an ARINC 429 bus, that is it contains:
    - speed characteristic for the bus
    - a list of unique A429m messages
    '''

    def __init__(self,speed = 'high'):
        ''''
        Create an A429 bus
        '''
        self.__speed = speed
        self.__messages = list()

    def addMessage(self,message):
        '''
        Add a new message definition to the bus
        Message in the same bus should have unique name.
        Additionnaly, duplicate label/SDI are not authorised.
        @param message: ARINC 429 message
        '''
        #TODO code
        pass

    def getMessage(self,messageName)
        '''
        Get a reference to a message given its name
        @param messageName: Name of the message to access
        @return: reference to the message
        '''
        #TODO
        pass

    def removeMessage(self,messageName):
        '''
        Remove a message from the bus, given its name
        @param messageName: name of the message to remove
        @return:
        '''
        #TODO
        pass