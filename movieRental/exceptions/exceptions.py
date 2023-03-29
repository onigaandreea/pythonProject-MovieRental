class ValidationException(Exception):
    def __init__(self, msgs):
        """
        :param msgs: lista de mesaje de eroare
        :type msgs: msgs
        """
        self.__err_msgs = msgs

    def getMessages(self):
        return self.__err_msgs

    def __str__(self):
        return 'Validation Exception: ' + str(self.__err_msgs)


class RepositoryException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def getMessage(self):
        return self.__msg

    def __str__(self):
        return 'Repository Exception: ' + str(self.__msg)


class DuplicateIDException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "ID duplicat.")


class ClientNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Clientul nu a fost gasit.")


class MovieNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Filmul nu a fost gasit.")


class InchiriereNotFoundException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Categoria nu a fost gasita.")

