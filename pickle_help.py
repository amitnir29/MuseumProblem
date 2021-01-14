import pickle


def pickle_to_file(obj, filename):
    """
    :param obj: object to write to file
    :param filename: the file to write to
    """
    outfile = open(filename, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()


def pickle_from_file(filename):
    """
    :param filename: file to read from
    :return: the object in file
    """
    infile = open(filename, 'rb')
    data = pickle.load(infile)
    infile.close()
    return data
