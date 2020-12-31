import pickle


def pickle_to_file(obj, filename):
    outfile = open(filename, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()


def pickle_from_file(filename):
    infile = open(filename, 'rb')
    data = pickle.load(infile)
    infile.close()
    return data
