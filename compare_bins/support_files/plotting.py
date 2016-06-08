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
    fig, axs = plt.subplots(1, len(column_pair_lists), figsize=(10, 6))

    for i, tup in enumerate(column_pair_lists):
        print(i)
        print(tup)

        low = dataframe[tup[0]].min()
        high = dataframe[tup[0]].max()
        plt.plot([low, high], [low, high], '--', c='gray', lw=2)
        # plt.ylim((low, high))
        # plt.xlim((low, high))
        plot_ax = axs[i]
        print(plot_ax)
        dataframe.plot(kind='scatter', ax=plot_ax,
                       x=tup[0], y=tup[1], title='abc')
    sns.despine()


def plot_metrics_as_heatmaps(metric_list, organism_list, figsize=(10, 6),
                            filename = None):
    # Copied from compare_fauzi_bins/
    # 160601_ANI_improvements--use_percent_coverage.ipynb

    # e.g.
    # p = plot_metrics_as_heatmaps(
    #   ['% identity', '% of query aligned', 'estimated % identity'],
    #   ['Methylotenera mobilis', 'Acidovorax'],
    #   figsize=(11, 4),
    #   filename = '160601_ANI_metric_development.pdf')

    print(len(metric_list))
    fig, axn = plt.subplots(1, len(metric_list),
                            sharex=True, sharey=True,
                            figsize=figsize)
    cbar_ax = fig.add_axes([.91, .3, .03, .4])

    data = filter_aggregated_data.subset_given_colnames(
        name_list = organism_list)
    data['% of query aligned'] = data['frac of query aligned']*100

    for i, metric in enumerate(metric_list):
        # prepare pivoted data
        print("i: {}, metric: {}".format(i, metric))
        subplot_ax = axn[i]
        print('axis: {}'.format(subplot_ax))
        subplot_data = aggregate_mummer_results.pivot_identity_table(data,
                                                                     value_var=metric)
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
