def subset_given_colnames(name_list):
    # Copied from compare_fauzi_bins/
    # 160601_ANI_improvements--use_percent_coverage.ipynb
    full_data = pd.read_csv("percent_identities.tsv" ,sep = '\t')
    all_names = full_data['query name'].unique()

    # build a list of names to pick out.
    plot_names = []

    for org_name in name_list:
        plot_names += [n for n in organism_names if org_name in n]

    # reduce to the desired organisms.
    selected_data = full_data.copy()
    selected_data = selected_data[selected_data['query name'].isin(plot_names)]
    selected_data = selected_data[selected_data['ref name'].isin(plot_names)]

    print("num rows selected: {}".format(selected_data.shape[0]))
    return selected_data