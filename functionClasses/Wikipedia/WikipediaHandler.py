from functionClasses import AbstractHandler


class WikipediaHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot, input_math_parser):
        AbstractHandler.AbstractHandler.__init__(self)
        self.math_parser = input_math_parser

    def handle(self, message, from_name_full):
        args = ' '.join(message[1:])
        
        return '%s, the answer is %f' % (from_name_full, answer)