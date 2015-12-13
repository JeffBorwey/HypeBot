webCharacters = {}
webCharacters[' '] = '%20'
webCharacters["\'"] = '%27'

def convertRawStringToURL(raw_string):
    for key, conversion in webCharacters.iteritems():
        raw_string = raw_string.replace(key, conversion)

    return raw_string
