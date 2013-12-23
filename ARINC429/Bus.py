import Exception


class Bus(object):
    '''
    Present a bus object, that is a collection of
    A429 messsage with uniques Label/SDI combinaison
    '''

    def __init__(self, name,speed='high'):
        self._name = name
        self._speed = speed
        self._messages = dict()

    def addMessage(self, message):
        '''
        Add a message to the Bus message dictionnary
        The message shall have a unique label/SDI combinaison
        '''
        label = message.getLabel()
        sdi = None  #TODO: add SDI handling

        if (label, sdi) in self._messages:
            raise Exception.A429MsgStructureError('A message with the same signature\
                                                  already exist in {}'.format(self._name),
                                                  label=label,
                                                  sdi=str(sdi))
        else:
            self._messages[label, sdi] = message

    def removeMessage(self, message):
        '''
        Remove a message to the Bus message dictionnary
        '''
        pass