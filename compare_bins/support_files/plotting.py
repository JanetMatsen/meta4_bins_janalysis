__author__ = 'jmatsen'

import aggregate_mummer_results
import name_extractions


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
