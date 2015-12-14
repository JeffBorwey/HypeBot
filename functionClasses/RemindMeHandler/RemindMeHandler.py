

class RemindMeHandler:

    def __init__(self, input_bot, reply_name, reply_message):
        self.input_bot = input_bot
        self.reply_name = reply_name
        self.reply_message = reply_message

    def job(self):
        self.input_bot.reply_room(self.reply_message, self.reply_name + ', this is a reminder!')
