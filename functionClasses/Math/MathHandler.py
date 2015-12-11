from functionClasses import AbstractHandler


class MathHandler(AbstractHandler.AbstractHandler):

    def __init__(self, input_bot, input_math_parser):
        AbstractHandler.AbstractHandler.__init__(self)
        self.math_parser = input_math_parser

    def handle(self, message, from_name_full):
        args = ' '.join(message[1:])
        answer = self.handle_math(from_name_full, args, message)
        return '%s, the answer is %f' % (from_name_full, answer)

    def handle_math(self, name, math_str, msg):
        return self.math_parser.eval(math_str)