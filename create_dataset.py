from data_classes.FileSentenceSplitter import FileSentenceSplitter
from data_classes.FileSentenceCleaner import FileSentenceCleaner
from helpers.classes.SpaceHandler import SpaceHandler
import spacy_udpipe

def main(input_path=".data/output"):
    # initializing the spacy model
    models_dir = "./helpers/modules"
    spacy_model_path = models_dir + "/ukrainian-iu-ud-2.5-191206.udpipe"
    SPACY_UDPIPE_MODEL = spacy_udpipe.load_from_path(
        lang="uk",
        path=spacy_model_path,
    )
    # initializing the modules
    fss = FileSentenceSplitter(SPACY_UDPIPE_MODEL)
    fsc = FileSentenceCleaner(SpaceHandler())
    # running the modules
    fss.get_sentences(input_path + "/amalgamation.txt", input_path + "/cleaned.txt")
    fsc.clean_file(input_path + "/cleaned.txt", input_path + "/dataset.txt")
    return 0

if __name__ == "__main__":
    main()