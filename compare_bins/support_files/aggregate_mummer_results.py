import glob
import numpy as np
import re
import sys

import pandas as pd

sys.path.append('./support_files/')
#import summarise_bins

import name_extractions


def load_individual_bin_summaries():
    return pd.read_csv('support_files/available_bins.csv', sep =',')


# def load_bin_length_summary():
#     return pd.read_csv('support_files/available_bins.csv', sep =',')


def load_one_mummer_result(filepath):
    """
    Load parsed MUMMER file (parsed into .tsv), and rename
    :param filepath:
    :return:
    """
    # trim ./mummer-results/filename.tsv to filename.tsv
    # col names: TAGS (ref)    TAGS (query)  LEN 1  LEN 2  LEN R  LEN Q
    # COV R  COV Q % IDY

    # Read in parsed MUMMER result.
    df = pd.read_csv(filepath, sep='\t')

    # check that the dataframe is not empty
    if df.shape[0] < 1:
        # return empty dataframe
        return df

    assert df.shape[0] > 0, "dataframe for {} has 0 rows".format(filepath)

    # The 2 argument says split at most 2 times.
    df['mummer file'] = filepath.split("/", 2)[2]

    df['query name'] = \
        df['mummer file'].apply(
            lambda x:
            name_extractions.query_and_ref_names_from_path(x)['query'])
    df['ref name'] = \
        df['mummer file'].apply(
            lambda x:
            name_extractions.query_and_ref_names_from_path(x)['ref'])
    # Split 'TAGS (ref)' = Ga0081624_1057 into a column called 'ref bin'
    # (= 'Ga0081624') and 'ref contig' = 1057
    # Same for 'TAGS (query)
    # Only works for Dave and Fazui bins, so put in a try clause.
    try:
        df['ref id'] = df['TAGS (ref)'].apply(
            lambda x: name_extractions.extract_bin_number(x))
        df['query id'] = df['TAGS (query)'].apply(
            lambda x: name_extractions.extract_bin_number(x))
        df['ref contig'] = df['TAGS (ref)'].apply(
            lambda x: name_extractions.extract_contig_number(x))
        df['query contig'] = df['TAGS (query)'].apply(
            lambda x: name_extractions.extract_contig_number(x))
    except:
        pass
    return df


def prep_summary_for_merge(df, prepend_string):
    """
    Prepend the specified string onto every column name of the dataframe.

    :param df: dataframe to alter the column names of.
    :param prepend_string: string to prpend to each column name.
    :return: dataframe with modified column names
    """
    df2 = df.copy()
    if 'category' in df2.columns:
        df2 = df2.drop('category', axis=1)
    if 'bin path' in df2.columns:
        df2 = df2.drop('bin path', axis=1)
    # prepend the string onto each column name
    df2.columns = map(lambda x: prepend_string + x, df2.columns)
    return df2


def check_column_uniformity(dataframe, colname):
    """
    Check uniformity of a column.  Useful when ensuring merges worked
     correctly.

    :param dataframe:
    :param colname:
    :return:
    """
    if colname in dataframe.columns:
        unique_col_values = dataframe[colname].unique()
        num_unique_values = len(unique_col_values)
        assert num_unique_values == 1, \
            'There are {} unique values for {}: \n {}'.format(
                num_unique_values, colname, unique_col_values)
    return None


def check_columns_uniformity(dataframe, colname_list):
    for colname in colname_list:
        check_column_uniformity(dataframe, colname)
    return None


def prepare_result(filepath):
    """
    Load a MUMmer result as .tsv, and load on the info about the query and
    reference bins

    :param filepath: path to parsed MUMmer result (tsv)
    :return: dataframe with one row per MUMmer match.
    """
    result = load_one_mummer_result(filepath)
    if result.shape[0] == 0:
        return None

    # prepare meta-info for the query bin
    # Customize the generalized metainfo for the query, then the ref.
    query_metainfo = prep_summary_for_merge(
        df=load_individual_bin_summaries(),
        prepend_string='query ')

    # prepare meta-info for the ref bin
    ref_metainfo = prep_summary_for_merge(
        df=load_individual_bin_summaries(),
        prepend_string='ref ')


    def check_merge_failure(merge_name):
        assert result.shape[0] > 0, \
            'after merging on {} metainfo, you only have {} rows ' \
            'remaining. Did inner merge fail?'.format(merge_name,
                                                      result.shape[0])

    def check_merge_name_success():
        unique_query_bin_names = result['query name'].unique()
        unique_ref_bin_names = result['ref name'].unique()
        assert len(unique_query_bin_names) == 1, \
            'should only have one query name, but have {} for {}'.format(
                len(unique_query_bin_names), result['mummer file'][0]
            )
        assert len(unique_ref_bin_names) == 1, \
            'should only have one query name, but have {} for {}'.format(
                len(unique_ref_bin_names), result['mummer file'][0]
            )

    print(result.columns)
    print(query_metainfo.columns)
    result = pd.merge(result, query_metainfo, how='inner')
    check_merge_failure('query')
    check_columns_uniformity(
        result, ['ref id', 'query id', 'query contigs', 'ref contigs'])

    # print(result.columns)
    # print(ref_metainfo.columns)
    result = pd.merge(result, ref_metainfo, how='inner')
    check_merge_failure('referemce')
    check_columns_uniformity(
        result, ['ref id', 'query id', 'query contigs', 'ref contigs'])

    check_merge_name_success()

    return result


def dataframe_is_one_query_target_pair(dataframe):
    """
    make sure there is only one query sequence and reference sequence in the
    given dataframe.  Used to check that we aren't aggregating % identity
    numbers across bin alignment pairs.

    :param dataframe:
    :return:
    """
    num_query_bins = len(dataframe['query name'].unique())
    num_ref_bins = len(dataframe['ref name'].unique())
    if not num_query_bins == 1:
        "Dataframe has a mix of {} query bins: {}".format(
            num_query_bins, dataframe['query name'].unique())
    if not num_ref_bins == 1:
        "Dataframe has a mix of {} reference bins: {}".format(
            num_query_bins, dataframe['ref name'].unique())
    if (num_query_bins == 1) & (num_ref_bins == 1):
        return True
    else:
        return False


def keep_longest_query_match(dataframe):
    """
    Strategy change 6/7/2016: don't use this!  We are going to use all matches,
    even though it will lead to double-counting in some cases.

    Though MUMMER can return multiple alignments per query contig, we are going
    to only keep the longest match.  It would be better to allow two
    non-overlapping alignments, but this is technically more challenging.

    :return:
    """
    # Check that the dataframe corresponds to one query target pair:
    assert dataframe_is_one_query_target_pair(dataframe), \
        "dataframe selected is not specific to one pair of bins"

    # The bins with the longest query alignment length:
    # (LEN 2 is the query, not LEN 1)
    keeper_rows_df = dataframe.groupby('TAGS (query)')['LEN 2'].agg(
        np.max).reset_index()
    # merge this dataframe onto the main dataframe to get the rows with the
    # longest matches.
    longest_rows = pd.merge(dataframe, keeper_rows_df)

    return longest_rows


def length_weighted_percent_identity(dataframe):
    # get a dataframe that has one row per reference contig, and the
    # corresponding longest length
    # LEN 2 = length of query alignment:
    # mummer.sourceforge.net/manual/http://mummer.sourceforge.net/manual/

    # if there are zero rows, return zero similarity

    # calculate the length-weighted percent identiy, known as ANI.
    percent_ident = \
        sum(dataframe['% IDY']*dataframe['LEN 2'])*1./dataframe['LEN 2'].sum()
    return percent_ident


def sum_of_query_alignment_lengths(dataframe):
    """
    Calculate the sum of the query lengths of a given dataframe.

    :param dataframe:
    :return:
    """
    return dataframe['LEN 2'].sum()


def summarize(filepath):
    """
    Return a summary dataframe with the % identity and fraction aligned.
    There should only be one row in this dataframe!

    :param filepath: path to mummer .coords parsed into .tsv format
    :return: a one-row summary dataframe
    """
    # Load the result tsv (meta info gets joined)
    single_result = prepare_result(filepath)
    if single_result is None:
        print('no rows for {}; assume zero similarity'.format(filepath))
        return None

    # As of 6/1/2016 we are only keeping the longest length in an alignment,
    # even though it is likely better to keep multiple alignments per query
    # contig as long as you don't double count alignment regions.
    longest_alignments = keep_longest_query_match(single_result)

    # Prepare a single-row summary for this pair of bins.  Will append %
    # identity on to it.
    # Trim off column names that are unique to a given alignment.
    summary = longest_alignments.copy()
    drop_columns = ['TAGS (ref)', 'TAGS (query)', 'LEN 1', 'LEN 2',
                    'LEN R', 'LEN Q', 'COV R', 'COV Q', '% IDY',
                    'ref contig', 'query contig']
    summary.drop(drop_columns, axis=1, inplace=True)
    summary = summary.drop_duplicates()

    assert(summary.shape[0] == 1), \
        "summary dataframe we will append to needs to have 1 row, but in " \
        "fact has {} rows.  \n {}".format(summary.shape[0], summary.head())

    if longest_alignments.shape[0] == 0:
        # Can't summarise something that didn't get alignments!!
        return None

    else:
        summary['% identity'] = \
            length_weighted_percent_identity(longest_alignments)
        summary['query alignment length total'] = \
            sum_of_query_alignment_lengths(longest_alignments)
        summary['number alignments aggregated'] = longest_alignments.shape[0]
        summary['frac of query aligned'] = \
            summary['query alignment length total']/summary['query bp']
        # The new metric developed by Dave/Janet 5/30/2016:
        summary['estimated % identity'] = \
            summary['% identity']*summary['frac of query aligned']
        return summary


def percent_idty_all_results(filepath_list):
    num_empty = 0
    num_with_contents = 0
    summary_all_samples = pd.DataFrame()
    for filepath in filepath_list:
        # load the dataframe for that file path

        print("summarize {}".format(filepath))
        summary = summarize(filepath)

        if summary is None:
            # print('no alignments found for {}; '
            #       'omit it from summary'.format(filepath))
            num_empty += 1
            continue
        else:
            # Check that the dataframe is one row.
            assert summary.shape[0] == 1, \
                "expected summary row to have 1 row, but it has {}".format(
                    summary.shape[0])
            print('--> {}:'.format(filepath))
            num_with_contents += 1

        # merge on the first row of the repetitive result dataframe
        # if no percent_identities dataframe exists (shouldn't on first
        # loop), then make one.
        if summary_all_samples.empty:
            summary_all_samples = summary
            # print('shape: {}'.format(summary_all_samples.shape))
        else:
            summary_all_samples = summary_all_samples.append(summary)
            # print('shape: {}'.format(summary_all_samples.shape))

    print('number of empty and filled files: {}, {}'.format(
        num_empty, num_with_contents
    ))
    return summary_all_samples

    # merge individual summaries into an umbrella pandas
    # include a file path to that bin.
    # merge on the info about the individual bins
    # return summary dataframe.
    pass


def pivot_identity_table(identity_table, value_var="% identity"):
    identity_table = identity_table.pivot(
        index='query name', columns='ref name', values=value_var)
    identity_table.fillna(value=0, inplace=True)
    return identity_table


def pivot_saved_tsv(saved_tsv_path, out_path):
    df = pd.read_csv(saved_tsv_path, sep='\t')
    df = pivot_identity_table(df)
    df.to_csv(out_path, sep='\t')


if __name__ == "__main__":
    test_samples = glob.glob('./mummer_results/*/*.tsv')
    i_res = percent_idty_all_results(test_samples)

    print('len of test_samples: {}'.format(len(test_samples)))
    print('len of test_samples set: {}'.format(
        len(set(test_samples))))
    unpivoted_path = 'percent_identities.tsv'

    i_res.to_csv(unpivoted_path, sep='\t')
    # pivot for seaborn plotting

    pivoted_path = 'percent_identities--pivoted.tsv'
    pivot_saved_tsv(unpivoted_path, pivoted_path)
