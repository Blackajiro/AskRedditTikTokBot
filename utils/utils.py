import nltk

# Define max paragraphs length (on screen characters)
MAX_PARAPGRAH_CHARS = 400


def split_comment(text):
    paragraphs = []

    try:

        # Init nltk and split into sentences
        nltk.download('punkt')
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(text)

        # Combine sentences into paragraphs
        string_group = ''
        for string in sentences:

            if len(string) > MAX_PARAPGRAH_CHARS:
                raise Exception("Paragraph too long")

            if len(string_group) + len(string) > MAX_PARAPGRAH_CHARS:
                paragraphs.append(string_group)
                string_group = ''

            string_group += string

    except Exception as e:
        print(e)
        exit(-1)

    return paragraphs
