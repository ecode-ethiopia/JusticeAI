import numpy

from feature_extraction.pre_processing.pre_processor import PreProcessor
from util.file import Save
from util.constant import Path
from util.log import Log


def run(command_list, filename=None):
    """
    Gets all information from precedent and saves binary model_training
    :param data_to_extract: decision or facts
    :param command_list: command line arguments
    :return: None
    """
    nb_of_files = -1
    try:
        nb_of_files = int(command_list[0])
    except ValueError:
        Log.write("Excepted numerical value")
    parser = PreProcessor()
    precedent_dict = parser.parse_files(Path.raw_data_directory, nb_of_files=nb_of_files)
    fact = __get_tuple(precedent_dict, "facts")
    decision = __get_tuple(precedent_dict, "decisions")

    # deallocate memory
    precedent_dict = None

    s = Save(r"pre_processing")
    if filename is None:
        s.save_binary("facts_pre_processed.bin", fact)
        s.save_binary("decisions_pre_processed.bin", decision)
    else:
        # this only exists to allow unittests
        s.save_binary(filename + ".bin", fact)


def __get_tuple(precedent_dict, data_to_extract):
    """
    Creates a tuple from the dictionary values
    :param precedent_dict: dict["facts"/"decisions"] : dict["vectors"]["fact"]["filenames"]
    :param data_to_extract: String
    :return:tupple(vectors, fact, filenames)
    """
    X = []
    labels = []
    precedent_files = []

    for fact in precedent_dict[data_to_extract]:
        X.append(precedent_dict[data_to_extract][fact].dict["vector"])
        labels += ([precedent_dict[data_to_extract][fact].dict["fact"]])
        precedent_files.append(precedent_dict[data_to_extract][fact].dict["precedence"])

    X = numpy.matrix(X)
    labels = numpy.array(labels)
    precedent_files = numpy.array(precedent_files)

    return X, labels, precedent_files