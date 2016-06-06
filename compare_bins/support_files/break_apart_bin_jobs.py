import os

import numpy as np

import pandas as pd

def write_bin_lists_to_files(chunk_size=60):
    bins = pd.read_csv('./support_files/available_bins.csv')
    print(bins.head())
    bin_names = bins[['bin path']]
    print(bins.head())
    file_dir = './support_files/jobs/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # break names into chunks and write
    for g, df in bin_names.groupby(np.arange(len(bin_names)) // chunk_size):
        job_number = g + 1
        print("g: {}".format(g))
        print(df.head(1))
        print(df.tail(1))
        filename = file_dir + "{}--{}_rows".format(job_number, df.shape[0])
        print('filename: {}'.format(filename))
        # g + '--' + df.shape[0] + "rows.tsv"
        df.to_csv(filename, sep='\t' , header=False, index=False)
    # for i, bin_sub_list in enumerate(chunk_it(bin_names, 10)):
    #     file_name = './support'+ i + "--" + bin_sub_list[0] + "--" + bin_sub_list[-1]
    #     with open(file_name, 'w') as outfile:
    #         outfile.write(line)




def chunk_it(seq, num):
    # chunkIt(range(10), 3) --> [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
    # median chunk size:
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
      out.append(seq[int(last):int(last + avg)])
      last += avg

    return out


if __name__ == "__main__":
    num_files = 50
    print('break up bin paths into {} files'.format(num_files))
    write_bin_lists_to_files(num_files)
