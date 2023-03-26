import re
import math

class FileSentenceSplitter(object):
    """
    Splits the given wall of text into sentences.
    """
    def __init__(self, spacy_model):
        self.spacy_model = spacy_model

    def load_text(self, input_path):
        """
        Loads the text and splits it by the existing \n symbols.
        """
        # loading the data
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
            text_org = text

        # Removing empty lines
        text = re.sub(r"\n{2,}", r"\n", text)
        lines = text.split("\n")
        lines = lines[:-1] # -1 to remove the last empty line
        return lines

    def split_line_into_sentences(self, line):
        """
        Splits a line into sentences. can handle contractions and stuff
        """
        doc = self.spacy_model(line)
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences

    def split_file_by_sentences(self, lines):
        """
        Splits the given text into sentences and returns them.
        """
        # the final file
        true_lines = []
        # progress tracker
        line_counter = 0
        # splitting the text into sentences
        for line in lines:
            sentences = self.split_line_into_sentences(line)
            # adding the sentences to the final list
            for sentence in sentences:
                true_lines.append(sentence)
            # progress tracker
            line_counter = line_counter + 1
            if line_counter % 15000 == 0:
                print("Progress: " + str(math.floor((line_counter/len(lines))*100)) + "%")
                print(str(line_counter) + " lines have been processed. " + str(len(true_lines)) + " sentences have been added.")
        # removing the duplicates
        true_lines = list(set(true_lines))
        print("Total number of sentences: " + str(len(true_lines)))
        return true_lines

    def get_sentences(self, input_path, output_path):
        """
        Main function that executes the rest.
        """
        lines = self.load_text(input_path)
        true_lines = self.split_file_by_sentences(lines)
        # writing everything down
        text = '\n'.join(true_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Saved!")
