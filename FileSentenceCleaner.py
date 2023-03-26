import re
import os
import cld3

class FileSentenceCleaner(object):
    """
    Cleans all sentence artifacts and standardizes the dataset.
    """
    def __init__(self, space_handler):
        self.space_handler = space_handler

    def load_data(self, input_path):
        """
        Loads input data and gets its length.
        """
        with open(input_path, 'r') as f:
            text = f.read()
            initial_length = str(len(text.split("\n")))
        return text, initial_length

    def fix_quotes(self, text):
        """
        Fixes the quotation marks.
        """
        # replacing the christmas trees and upper doubles
        text = re.sub(r'[«»“”]', '"', text)
        # removing the more exotic ones with the spaces to the right
        text = re.sub(r"„\s*", '"', text)
        lines = text.split("\n")
        # removing the unfit lines and returning back to the normal form
        lines = [l for l in lines if not re.findall(r'‘', l)]
        text = '\n'.join(lines)
        return text

    def fix_apostrophes(self, text):
        """
        Fixes the apostrophes.
        """
        # replacing the ` and ´
        text = re.sub(r'[`´]', "'", text)
        # replacing the true apostrothes with ' symbols
        lines = text.split("\n")
        text = "\n".join([l for l in lines if not(len(re.findall(r'(\W’\w|^’\w)', l)) + len(re.findall(r'(\w’\W|\w’$)', l)) + len(re.findall(r'\W’\W', l)))])
        text = re.sub(r"[’`]", "'", text)
        # fixing the apostrophes-imposters
        letters = "[А-ЩЬЮЯЄҐІЇа-щьюяєґії]"
        text = re.sub(re.compile(f'({letters})' + '"' + f'({letters})'), r"\1'\2", text)
        lines = text.split('\n')
        # removing the lines with an uneven number of marks
        lines = [self.space_handler.space_stripper(l) for l in lines if ((len(re.findall('"', l)) % 2) == 0)]
        text = '\n'.join(lines)
        return text

    def fix_dashes(self, text):
        """
        Fixes the dashes.
        We are setting the 8212 character as the standard.
        """
        # all the possible dashes
        dashes = [chr(8208), chr(8209), chr(8210), chr(8211), chr(8212), chr(8213), \
                chr(8214), chr(8722), chr(12641)]
        # replacing all the dashes with double hyphens
        for dash in dashes:
            text = re.sub(dash, "--", text)
        # and then replacing all of them with our standardized dashes
        text = re.sub(r"-{2,}", "—", text)
        lines = text.split("\n")
        # removing the very specific cases of єднальне тире, which is not fixable by hardcode anyway
        lines = [l for l in lines if not (len(re.findall(r'(\S—\S)', l)) and not len(re.findall(r'(\d—\d)', l)))]
        # unclinging the clinging dashes
        clingy = [l for l in lines if re.findall(r'(\S—\s|\s—\S)', l)]
        clingy = [re.sub(r'(\S)—\s', r"\1 — ", l) for l in clingy]
        clingy = [re.sub(r'\s—(\S)', r" — \1", l) for l in clingy]
        lines = [l for l in lines if not len(re.findall(r'(\S—\s|\s—\S)', l))] + clingy
        # removing the phrase fragments
        lines = [l for l in lines if not (re.findall(r"^\s*—", l))]
        text = "\n".join(lines)
        return text

    def fix_hyphens(self, text):
        """
        Fixes the hyphens
        """
        # replacing dangling hyphens with dashes
        text = re.sub(r"(\W)-(\W)", r"\1—\2", text)
        lines = text.split("\n")
        # getting rid of the dangling hyphens in the beginning of the sentence as dashes
        lines = [re.sub(r"^\s*—", '', l) for l in lines]
        return lines

    def fix_spaces(self, lines):
        """
        Fixes the spaces between words.
        """
        lines = [re.sub(r"\s{2,}", ' ', l) for l in lines] # two and more spaces into one
        lines = [re.sub(r"^\s+", '', l) for l in lines] # one or more spaces in the beginning to remove
        lines = [re.sub(r"\s+$", '', l) for l in lines] # one or more spaces in the end to remove
        lines = [re.sub(r"\s([,:;.!?…])", r"\1", l) for l in lines] # removing the spaces that do not belong here
        return lines

    def fix_marks(self, lines):
        """
        Fixes the ellipsis and other weird stuff like dullipsis.
        """
        # implementing the ellipsis
        lines = [re.sub(r"\.{3,}", chr(8230) + ' ', l) for l in lines]
        text = '\n'.join(lines)
        text = re.sub(r"([^!?])\.\.", r"\1…", text)
        text = re.sub(r"([!?])\.\.", r"\1‥", text)
        # fixing the improper double marks
        text = re.sub(r"([,;:])[,;:]", r"\1", text)
        lines = text.split('\n')
        lines = [re.sub(r'([.!?;])([^)",\s])', r"\1 \2", l) for l in lines]
        lines = [re.sub(r'([,])([^"\s])', r"\1 \2", l) for l in lines]
        text = '\n'.join(lines)
        text = re.sub(r'([:])(\S)', r"\1 \2", text)
        # removing the dullipsis and other weird stuff
        text = re.sub(chr(8230), "...", text)
        text = re.sub(chr(8229), " ", text)
        lines = text.split('\n')
        lines = [l for l in lines if not (re.findall(r'(\S—\s|\s—\S)', l))]
        return lines

    def standardize_text(self, text):
        """
        Unifies and cleans the disrepancies between different formatting methods.
        """
        text = re.sub(r"\n{2,}", r"\n", text) # removes empty lines
        text = self.fix_quotes(text) # fixes the quotation marks
        text = self.fix_apostrophes(text) # fixes the apostrophes
        text = self.fix_dashes(text) # fixes the dashes
        lines = self.fix_hyphens(text) # fixes the hyphens
        lines = self.fix_spaces(lines) # fixes the lines
        lines = self.fix_marks(lines) # fixes the punctuation marks
        return lines

    def remove_unfit_sentences(self, lines):
        """
        Bruteforce cleaners of different sentences that will be trouble in processing.
        """
        # uncomment to see the statistics
        # print('Number of sentences with ": —" signs: ' + str(len([l for l in lines if re.findall(": —", l)])))
        # print('Number of sentences with ", —" signs: ' + str(len([l for l in lines if re.findall(", —", l)])))
        # print('Number of sentences with "... —" signs: ' + str(len([l for l in lines if re.findall("\.\.\. —", l)])))
        # print('Number of sentences with "… —" signs: ' + str(len(re.findall(chr(8230)+r'\s—', text))))
        # print('Number of sentences with <> artifacts: ' + str(len([l for l in lines if re.findall(r'<*>', l)])))
        # print('Number of sentences with [] artifacts: ' + str(len([l for l in lines if re.findall(r"\[*]", l)])))
        # print('Number of sentences that start with punctuation except for dashes: ' + str(len([l for l in lines if l[0] in self.space_handler.upr and l[0] != "—"])))
        # print('Number of sentences that do not have any Ukrainian symbols: ' + str(len([l for l in lines if len(re.findall(r"[А-ЩЬЮЯЄҐІЇа-щьюяєґії]", l)) == 0])))
        # print('Number of sentences with bullshit symbols: ' + str(len([l for l in lines if len(re.findall(r"[�ßüä~@#^*‘₴{}\|/<>]", l))])))

        # making sure that the data is cleanable
        lines = [self.space_handler.space_stripper(l) for l in lines]
        # removing too short or long lines
        lines = [l for l in lines if len(l.split(' ')) in range(5, 30)]
        # removing the direct speech
        lines = [l for l in lines if not (re.findall("\: —", l) or re.findall(", —", l) or re.findall("\.\.\. —", l) or re.findall("; —", l) \
                    or re.findall(chr(8230)+r' —', l) or re.findall("\. —", l) or re.findall('\? —', l) or re.findall('! —', l) or re.findall('—\.', l))]
        # removing the sentences that start with punctuarion except for dashes
        lines = [l for l in lines if not l[0] in self.space_handler.upr]
        # removing the other bs symbols and editorial artifacts
        lines = [l for l in lines if re.findall(r"[А-ЩЬЮЯЄҐІЇа-щьюяєґії]", l) and not re.findall(r"[°♦_■•©�ßüä~@#^*‘₴{}\|/<>×○εχθρώνάδωΩΘλΣ\[\]]", l)]
        # removing very specific sentences with no room for errorifying
        lines = [self.space_handler.space_stripper(l) for l in lines if not (re.findall('"\(', l) or re.findall(',\.', l) or re.findall('\.-', l) or re.findall('\.\.\.,', l) or re.findall('-,', l) \
                or re.findall('\.!', l) or re.findall(':\.', l) or re.findall('-;', l) or re.findall('"-', l) or (re.findall('\.{2}', l) and not re.findall('\.{3}', l)) \
                or re.findall('-\(', l) or re.findall('\.-', l))]
        # removing apparent sentence fragments
        lines = [l for l in lines if l[-1] in self.space_handler.upr]
        # removing sentences in Russian
        lines = [l for l in lines if not (cld3.get_language(l)[0] != 'uk' and cld3.get_language(l)[1] >= .99)]
        return lines

    def clean_author_punctuation(self, lines):
        """
        Removes the ingrammatical author punctuation.
        """
        lines = [re.sub('\?.*', '?', l) for l in lines]
        lines = [re.sub('!.*', '!', l) for l in lines]
        lines = [re.sub('-\.', '.', l) for l in lines]
        lines = [re.sub(' ""', ' ', l) for l in lines]
        lines = [re.sub('/././.,', ',', l) for l in lines]
        lines = [re.sub('/././.?', '?', l) for l in lines]
        # repeating the process after removing the author punctuation
        # making sure that the data is cleanable
        lines = [self.space_handler.space_stripper(l) for l in lines]
        # removing the direct speech
        lines = [l for l in lines if not (re.findall("\: —", l) or re.findall(", —", l) or re.findall("\.\.\. —", l) or re.findall("; —", l) \
                    or re.findall(chr(8230)+r' —', l) or re.findall("\. —", l) or re.findall('\? —', l) or re.findall('! —', l) or re.findall('—\.', l))]
        # removing the sentences that start with punctuarion except for dashes
        lines = [l for l in lines if not l[0] in self.space_handler.upr]
        # removing the other bs symbols and editorial artifacts
        lines = [l for l in lines if re.findall(r"[А-ЩЬЮЯЄҐІЇа-щьюяєґії]", l) and not re.findall(r"[°♦_■•©�ßüä~@#^*‘₴{}\|/<>π×○εχθρώνάδωΩΘλΣ\[\]]", l)]
        # removing very specific sentences with no room for errorifying
        lines = [self.space_handler.space_stripper(l) for l in lines if not (re.findall('"\(', l) or re.findall(',\.', l) or re.findall('\.-', l) or re.findall('\.\.\.,', l) or re.findall('-,', l) \
                or re.findall('\.!', l) or re.findall(':\.', l) or re.findall('-;', l) or re.findall('"-', l) or (re.findall('\.{2}', l) and not re.findall('\.{3}', l)) \
                or re.findall('-\(', l) or re.findall('\.-', l))]
        # removing the author capitalization
        lines = [re.sub('Деталі: ', '', l) for l in lines]
        return lines

    def remove_artifacts(self, lines):
        """
        Removes different artifacts people generally don't use in writing.
        """
        # cleaning the bullshit symbols
        bs_symbols = ['► ', '☛ ', '→ ', '⁃ ', '− ', '₂', '● ']
        text = '\n'.join(lines)
        for bs in bs_symbols:
            text = re.sub(bs, '', text)
        # removing the emojis
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"   # emoticons
            u"\U0001F300-\U0001F5FF"   # symbols & pictographs
            u"\U0001F680-\U0001F6FF"   # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"   # flags (iOS)
            u"\U00002500-\U00002BEF"   # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
            "]+", re.UNICODE)
        lines = text.split("\n")
        lines = [re.sub(emoj, '', l) for l in lines]
        # removing the duplicates
        lines = list(set(lines))
        return lines

    def clean_file(self, input_path, output_path):
        """
        Calls all other functions and runs them in the correct order
        """
        text, initial_length = self.load_data(input_path)
        lines = self.standardize_text(text)
        lines = self.remove_unfit_sentences(lines)
        lines = self.clean_author_punctuation(lines)
        lines = self.remove_artifacts(lines)
        print('Initial length: ' + initial_length)
        print('Final length: ' + str(len(lines)))
        # saving the text
        text = '\n'.join(lines)
        with open(output_path, 'w') as f:
            f.write(text)
        print("Saved!")
