import abc


class AbstractHandler():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, message, from_name_full):
        """Implement this to handle a message received in the current HipChat room"""
        return
