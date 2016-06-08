import re


def filename_to_title(filename):
    # "abc_to_def" --> "abc \n to def"
    # strip off .tsv
    filename = filename.rstrip('\.tsv')
    bin_list = filename.split("_to_")
    title = '{} \n to {}'.format(bin_list[0], bin_list[1])
    return title


def query_and_ref_names_from_path(filepath):
    """
    Return a tuple of the query and product names from a path including bin
    names separated by "_to".

     E.g. "potential_relpath/bin_a_to_bin_b" --> bin_a, bin_b

    :param filepath: string to search
    :return: dict containing the query_bin, ref_bin
    """

    # \w matches a "word" character: a letter or digit or underbar [a-zA-Z0-9_]
    search = '([\w\.-]+)_to_([\w\.-]+).tsv'
    match = re.search(search, filepath)
    assert match, 'match not found for {} in {}'.format(search, filepath)
    if match:
        return {'query': match.group(1), 'ref':match.group(2)}
    else:
        return None


def extract_bin_number(string):
    # Ga0081607_1001 --> Ga0081607
    # Todo: merge with support_files.bin_lengths.extract_bin_number
    m = re.search("(Ga[0-9]+)_[0-9]+", string)
    assert m, 'no match found in {}'.format(string)
    return m.group(1)


def extract_contig_number(string):
    # Ga0081607_1001 --> 1001
    return re.search("Ga[0-9]+_([0-9]+)", string).group(1)


def bin_source_from_path(bin_path):
    pattern = re.compile(r"/bins/([a-zA-Z0-9_-]+)/*")

    m = pattern.search(bin_path)
    assert m is not None, "no regex match for {}".format(bin_path)
    name = m.group(1)

    #print(name)
    rename_dict = {'isolate': "isolate",
                   'dave': "dave",
                   'fauzi': "fauzi"}
    assert name in rename_dict.keys(), \
        'Name "{}" is not recognized'.format(name)

    bin_category = rename_dict[name]
    #print("bin name for {}: {}".format(bin_path, bin_category))
    return bin_category



