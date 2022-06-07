sexual_words = {
    "sexual experience": "intercourse",
    "sexual": "",
    "sexy": "tempting",
    "sex": "lovemaking",
    "blowjob": "oral",
    "blow job": "oral",
    "pussy": "vagina",
    "cock": "penis",
    "dick": "penis",
    "cumshot": "ejaculation",
    "cumming": "ejaculating",
    "cum": "semen",
    "squirt": "flow",
    "porn": "lewd",
    "masturbation": "self-stimulation",
    "anal": "back",
    "fucking": "flippin",
    "fuck": "lay"
}


def censor_sexual_words(string):
    string = string.upper()
    for word in sexual_words:
        string = string.replace(word.upper(), sexual_words[word].upper())
    return string
