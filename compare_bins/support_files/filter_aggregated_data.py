import pandas as pd


def load_percent_identies_result():
    return pd.read_csv("percent_identities.tsv" ,sep = '\t')


def subset_given_colnames(name_list, dataframe=None):
    # Copied from compare_fauzi_bins/
    # 160601_ANI_improvements--use_percent_coverage.ipynb

    for name in name_list:
        assert " " not in name, \
            "bin names don't have spaces!  Fix {}".format(name)

    if dataframe is None:
        full_data = load_percent_identies_result()
    else:
        full_data = dataframe

    assert isinstance(full_data, pd.DataFrame)
    all_names = full_data['query name'].unique()

    # build a list of names to pick out.
    plot_names = []

    for org_name in name_list:
        found_names = [n for n in all_names if org_name in n]
        if len(found_names) == 0:
            print("WARNING: no bin names found for string {}".format(
                org_name
            ))
        plot_names += found_names

    assert(len(plot_names) > 0 ), \
        "didn't find any organism names based on name_list"

    # reduce to the desired organisms.
    selected_data = full_data.copy()
    selected_data = selected_data[selected_data['query name'].isin(plot_names)]
    selected_data = selected_data[selected_data['ref name'].isin(plot_names)]

    print("num rows selected: {}".format(selected_data.shape[0]))
    return selected_data