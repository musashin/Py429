import Exception
import Message

class Bus(object):
    '''
    Present a bus object, that is a collection of
    A429 messsage with uniques Label/SDI combinaison
    '''

    def __init__(self, name, speed='high'):
        '''
        Constructor

        '''
        self._name = name
        self._speed = speed
        self._messages = dict()

    def getMessageNames(self):
        return [message.name for message in self._messages]

    def addMessage(self, message):
        '''
        Add a message to the Bus message dictionnary
        The message shall have a unique label/SDI combinaison
        '''
        label = message.getLabel()
        sdi = message.getSDI()

        if (label, sdi) in self._messages:
            raise Exception.A429MsgStructureError('A message with the same signature\
                                                  already exist in {}'.format(self._name),
                                                  label=label,
                                                  sdi=str(sdi))
        else:
            self._messages[label, sdi] = message

    def replaceMessage(self, message):
        '''
        replace an existing message in the Bus message dictionnary
        The message shall exist already
        '''
        #TODO test
        label = message.getLabel()
        sdi = message.getSDI()

        if (label, sdi) in self._messages:
            self._messages[label, sdi] = message
        else:
            raise Exception.A429MsgStructureError('A message with the same signature\
                                                  do not exist in {}'.format(self._name),
                                                  label=label,
                                                  sdi=str(sdi))

    def removeMessage(self, message):
        '''
        Given an A429 message,
        Remove a message with the same signature from the Bus message dictionnary
        '''
        label = message.getLabel()
        sdi = message.getSDI()


        if (label, sdi) in self._messages:
            del(self._messages[label, sdi])
        else:
            raise Exception.A429MsgStructureError('A message with the same signature\
                                                  do not exist in {}'.format(self._name),
                                                  label=label,
                                                  sdi=str(sdi))