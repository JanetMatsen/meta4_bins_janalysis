__author__ = 'jmatsen'

import pandas as pd
import seaborn as sns

import aggregate_mummer_results
import name_extractions
import filter_aggregated_data

import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_identity_vs_len(filepath, save_path='./plots/'):
    """
    Make a little scatter plot with a dot for each contig.
    x = LEN 2 (length of query alignment), y = % IDY.

    :param filepath:
    :param save_path:
    :return:
    """
    df = aggregate_mummer_results.load_one_mummer_result(filepath)
    if df.shape[0] > 1:
        plot = df.plot.scatter(x='LEN 2', y='% IDY')
        filename = df['mummer file'][0]
        plot.set_title(name_extractions.filename_to_title(filename), y=1.05)
        if save_path:
            save_path = save_path + filename.rstrip('.tsv') + '.pdf'
            plot.figure.savefig(save_path, bbox_inches='tight')


def plot_old_versus_new_ani(dataframe, column_pair_lists):
    """
    Plot old metrics for ANI versus new metrics as scatter plots.

    As seen in ani_preliminary_plots.ipynb

    :param dataframe:
    :param column_pair_lists: list of tuples.  One tuple per sub-plot.
    E.g. column_pairs =
    [('% identity (1)', '% identity (2)'),
    ('frac of query aligned (1)', 'frac of query aligned (2)'),
    ('estimated % identity (1)', 'estimated % identity (2)')
    ]
    :return: plot with one sub-plot per tuple
    """

    # Append on new column names.
    # Frac aligned doesn't look good sharing a colorscale with percent values
    # that range from 0 to ~100
    if 'frac of query aligned (1)' in dataframe.columns:
        dataframe['% of query aligned (1)'] = \
            dataframe['frac of query aligned (1)']*100
    else:
        print ('"frac of query aligned (1)" not found')
    if 'frac of query aligned (2)' in dataframe.columns:
        dataframe['% of query aligned (2)'] = \
            dataframe['frac of query aligned (2)']*100

    for column_pair in column_pair_lists:
        for colname in column_pair:
            assert colname in dataframe.columns, \
                """Column "{}" isn't in dataframe. Colnames: {}""".format(
                    colname, dataframe.columns)


    plot_width = 4.5*len(column_pair_lists)
    fig, axs = plt.subplots(1, len(column_pair_lists),
                            figsize=(plot_width, 4))

    for i, tup in enumerate(column_pair_lists):
        print(i)
        print(tup)

        metric_name = name_extractions.summary_stat_type(tup[0])

        plot_ax = axs[i]

        low = dataframe[tup[0]].min()
        high = dataframe[tup[0]].max()
        plot_ax.plot([low, high], [low, high], '--',
                     c='gray', lw=2)
        # plt.ylim((low, high))
        # plt.xlim((low, high))
        print(plot_ax)
        dataframe.plot(kind='scatter', ax=plot_ax,
                       x=tup[0], y=tup[1], title=metric_name, alpha=0.2)
    sns.despine()



def plot_metrics_as_heatmaps(metric_list, organism_list,
                             figsize=(10, 6), filename = None):
    """
    Pass a list of metrics and a list of partial bin names to make heat maps from.

    Metrics can be those built-in to the summary dataframe (made by
    aggregate_mummer_results.py) that is loaded below, with the additions of
    "% of query aligned (1)" and "% of query aligned (2)", which are added
    in this function.

    The strings in organism_list specify which bins to include.  Any bin with
    a string that contains one of the strings in organism_list will be
    included.  Bin names do not have spaces!

    Currently all heatmap scales' range is from 0 to 100, which makes it
    suitable for plotting percents.  To allow the fraction of the query
    that is aligned to be displayed,

    :param dataframe: summary dataframe as
    :param metric_list: list of column names to make heat maps out of.
        Can be just one name
    :param organism_list: list of strings to use when deciding what bins to
        include.  Can be general like 'Methylotenera mobilis', which will grab
        all bins with that string present in their name, or a full bin name
        that will map to only one bin.
    :param figsize: size of the entire figure.
    :param filename: name to save resulting figure to.  If set to None, no
        figure will be saved.
    :return:
    """

    assert isinstance(metric_list, list), 'metric_list needs to be a list'
    assert isinstance(organism_list, list), 'organism_list needs to be a list'

    print(len(metric_list))
    fig, axn = plt.subplots(1, len(metric_list),
                            sharex=True, sharey=True,
                            figsize=figsize)
    cbar_ax = fig.add_axes([.91, .3, .03, .4])

    data = filter_aggregated_data.subset_given_colnames(
        name_list = organism_list)

    # Add on % coverage columns so the fraction aligned can be included
    # in this 0 to 100 scale.
    data['% of query aligned (1)'] = data['frac of query aligned (1)']*100.0
    data['% of query aligned (2)'] = data['frac of query aligned (2)']*100.0

    assert data.shape[0] > 0, 'dataframe has no rows after filtering'

    # Make the heat maps, one by one.
    for i, metric in enumerate(metric_list):
        # prepare pivoted data
        print("i: {}, metric: {}".format(i, metric))
        subplot_ax = axn[i]
        print('axis: {}'.format(subplot_ax))

        # check that all of the supplied values to use for heat-map fill values
        # exist in that dataframe
        assert metric in data.columns, \
            """metric "{}" doesn't exist. Please chose from: \n {}""".format(
                metric, data.columns)

        subplot_data = aggregate_mummer_results.pivot_identity_table(
            data, value_var=metric)

        sns.heatmap(subplot_data, ax=axn[i],
                    cbar=i == 0,
                    vmin=0, vmax=100,
                    cbar_ax=None if i else cbar_ax
                   )
        subplot_ax.set_title(metric)

    fig.tight_layout(rect=[0, 0, .9, 1])
    print(type(fig))
    print(type(axn))
    if filename is not None:
        fig.savefig(filename)
        fig.savefig(filename.rstrip('pdf') + 'svg')
