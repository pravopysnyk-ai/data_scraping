import os

class TextMerger(object):
    """
    Merges all .txt files in the given folder
    """
    def __init__(self):
        pass
    
    def concatenate_files(self, input_directory):
        """
        Concatenates the text files together.
        """
        all_lines = []
        for filename in os.listdir(input_directory):
            with open(os.path.join(input_directory, filename), 'r') as f:
                text = f.read()
                lines = text.split('\n')
                all_lines.append(lines)
        return all_lines

    def split_into_lines(self, all_lines):
        """
        Splits the text wall into given lines.
        Does not split them into sentences, there is a separate module for that.
        """
        sentences_raw = []
        for i in range(len(all_lines)):
            for j in range(len(all_lines[i])):
                if all_lines[i][j] != '' and all_lines[i][j] != '\n':
                    sentences_raw.append(all_lines[i][j])
        sentences_raw = list(set(sentences_raw)) # removing the duplicates
        print("We got " + str(len(sentences_raw)) + " lines in total!")
        return sentences_raw

    def merge_text(self, input_directory):
        """
        Runs all the existing functions and saves the output as 
        amalgamation.txt in the input_directory.
        """
        all_lines = self.concatenate_files(input_directory)
        sentences_raw = self.split_into_lines(all_lines)
        with open(input_directory + "/amalgamation.txt", 'w') as f:
            for sentence in sentences_raw:
                f.write(sentence + '\n')
        print("Done!")