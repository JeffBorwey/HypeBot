import random

from functionClasses import AbstractHandler

class RollHandler(AbstractHandler.AbstractHandler):

    MAX_COUNT = 100

    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])
        splitArgs = args.split('d')

        if(len(splitArgs) != 2):
            return "%s, I couldn't parse your input. "  \
                   'Use the format xdy with x being number and y type of dice.' % from_name_full
        elif(not splitArgs[0].isdigit() or not splitArgs[1].isdigit() or
            int(splitArgs[0]) <= 0 or int(splitArgs[1]) <= 0 or
            int(splitArgs[0]) > self.MAX_COUNT or int(splitArgs[1]) > self.MAX_COUNT):
            return '%s, Use numbers between 1 and %s. Nice try though.' % (from_name_full, str(self.MAX_COUNT))
        else:
            pipsOnDice = int(splitArgs[1])
            diceCount = int(splitArgs[0])
            sum = 0
            allDice = []
            if diceCount == 1:
                result = random.randint(1, pipsOnDice)
                return '%s, I rolled a %s.' % (from_name_full, str(result))
            else:
                retString = '%s, I rolled the following numbers: ' % from_name_full
                for x in range(0, diceCount):
                    oneDiceRoll = random.randint(1, pipsOnDice)
                    sum += oneDiceRoll
                    allDice.append(oneDiceRoll)
                    retString += str(oneDiceRoll) + ", "

                retString = retString[0:-2]

                retString += "\n That's a total of %s." % str(sum)
                return retString