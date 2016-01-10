from functionClasses import AbstractHandler
from functionClasses.Translate import LanguageDictionary
from microsofttranslator import Translator


class TranslateHandler(AbstractHandler.AbstractHandler):
    def __init__(self, input_bot):
        AbstractHandler.AbstractHandler.__init__(self)

    def handle(self, message, from_name_full, msg_obj):
        args = ' '.join(message[1:])
        splitArgs = args.split('|')
        if len(splitArgs) > 3:
            return "%s, I can't parse your input. Please use one of the formats described in the !help menu." % from_name_full
        languages = LanguageDictionary.getLanguageCodes()

        if len(splitArgs) == 1:
            translated_phrase = self.call_translate_method(splitArgs[0], None, None)
        elif len(splitArgs) == 2:
            if splitArgs[1].upper() in languages.keys():
                translated_phrase = self.call_translate_method(splitArgs[0], None, languages[splitArgs[1].upper()])
            else:
                return "%s, I don't recognize that language. " \
                       "Please use the full names of the language you wish to use and check spelling." % from_name_full
        else:
            if splitArgs[1].upper() in languages.keys() and splitArgs[2].upper() in languages.keys():
                translated_phrase = self.call_translate_method(splitArgs[0], languages[splitArgs[1].upper()],
                                                               languages[splitArgs[2].upper()])
            else:
                return "%s, I don't recognize one of your languages. " \
                       "Please use the full names of the languages you wish to use and check spelling." % from_name_full

        return '%s, your translated phrase is: %s.' % (from_name_full, translated_phrase)

    # Uses the Microsoft Translate API
    def call_translate_method(self, text, from_language, to_language):
        # This is supposed to be secret. I'm not really worried unless we distribute this thing.
        translator = Translator("HypeBot", "6QvARrt7O0/JPsUeNRDeixHIGozNb6O7Gd5cFjFLjYU=")
        if from_language == None:
            from_language = translator.detect_language(text=text)
        if to_language == None:
            to_language = 'en'  # Assume English
        return translator.translate(text=text, to_lang=to_language, from_lang=from_language)
