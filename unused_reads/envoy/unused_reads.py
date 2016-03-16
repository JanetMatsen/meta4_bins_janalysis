import os
import time

import envoy

# TODO: assert that it is python 2.  envoy seemed to freak out with Python 3.
# see demo on my laptop.

def write_to_file(text, filename, prepend_datetime=False):
    with open(filename, 'a') as myfile:
            if prepend_datetime:
                myfile.write("Current date & time " +
                             time.strftime("%c") + '\n')
            myfile.write(text)
    pass


def shell(command,
          outfile=None,
          prepend_datetime=True,
          debug=False):
    r = envoy.run(command)
    # print envoy results if desired.
    if debug:
        print("envoy command: {}".format(r.command))
        # standard convention: pass 0 for success, 1 or higher for fail
        print("envoy status: {}".format(r.status_code))
        print("envoy std_out: {}".format(r.std_out))
        print("envoy std_err: {}".format(r.std_err))

    if r.status_code > 0:
        print("error: {}".format(r.std_err))
    # print standard_out_if_no_outfile
    if not outfile:
        print(r.std_out)
    else:
        # save output to file
        write_to_file(r.std_out, filename=outfile,
                      prepend_datetime=prepend_datetime)
    pass


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def sample_name_to_bam_filepath(sample):
    # convert something like XY_HOWZ --> a file path for the bam
    # todo: fix this placeholder/
    if sample=='112_LOW13':
        return '/gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam'
    else:
        print("FUNCTION NOT WRITTEN YET")
        return None


def check_file_exists(filepath):
    # return True if the .fasta at filepath already exist.
    return os.path.isfile(filepath)


def sample_name_to_fasta_name(sample_name):
    return './fasta_files/' + sample_name + '.fasta'


def sample_name_to_blasted_name(sample_name):
    return  './blast_results/' + sample_name + '-blasted.tsv'


def bam_to_fasta(source_path, dest_path, std_out_file,
                 sam_flag=4, header=True, subsample=0.01):
    # make sure the .bam file exists
    print('convert bam to fasta: {}'.format(source_path))
    assert(os.path.exists(source_path))

    # take an input .bam file, grab reads with flag=sam_flag, subsmple
    # those results, to the percent specified by subsample, and save a
    # .fasta with the selected reads
    # todo: implement subsampling.
    command_1 = "/work/software/samtools/bin/samtools view -f {} {}".format(
        sam_flag, source_path)
    print(command_1)
    # can use triple quotes to have mixed ' and " in python.
    # NEED TO USE \\n not \n
    # source: http://stackoverflow.com/questions/15280050/calling-awk-from-python
    command_2 = """ | awk '{OFS="\t"; print ">"$1"\\n"$10}' """
    print(command_2)
    command_3 = """ - > ./fasta_files/{}""".format(dest_path)
    command_string = command_1 + command_2 + command_3

    # NEED TO USE \\n not \n
    # source: http://stackoverflow.com/questions/15280050/calling-awk-from-python
    # WORKS:
    #command_string = """ /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\\n"$10}' """
    #     # don't run the >.  Use envoy, wrapped in shell() to do this.
    #     # - > ./fasta_files/112_LOW13_unmapped.fasta """
    print("run this shell command: ")
    print(command_string)
    # run the command.
    shell(command_string, outfile=dest_path)

    pass


def blast_fasta(in_file, out_file, outfmt=None):
    if not outfmt:
        outfmt = '"6 stitle qseqid sseqid ' \
                 'pident length mismatch gapopen qstart qend sstart" '
    print("blast output format: {}".format(outfmt))

    blast_command = \
        """
        blastn -db /work/data/blast_db/nt -query {}
        -word_size 24 -ungapped -outfmt {}
        -show_gis -max_target_seqs 1 -num_threads 12
        """.format(in_file, outfmt)
        # 'blastn -db /work/data/blast_db/nt -query {} '.format(in_file) + \
        # '-word_size 24 -ungapped -outfmt {}'.format(outfmt) + \
        # '-show_gis -max_target_seqs 1 -num_threads 12 > {}'
    print(blast_command)
    print('command to blast: {}'.format(blast_command))
    # qseqid   --> Query Seq-id    (default)
    # sseqid   --> Subject Seq-id  (default)
    # pident   --> Percentage of identical matches  (default)
    # length   --> Alignment length  (default)
    # mismatch --> Number of mismatches (default)
    # gapopen  --> Number of gap openings (default)
    # qstart   --> Start of alignment in query (default)
    # qend     --> End of alignment in query (default)
    # sstart   --> Start of alignment in subject (default)

    # run the shell command (envoy)
    shell(blast_command, outfile=out_file)
    pass



