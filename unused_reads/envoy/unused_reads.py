import itertools

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
          prepend_datetime=False,
          debug=False):
    # Todo: ensure that the path to the outfile exists (not the outfile itself)

    r = envoy.run(command)
    # print envoy results if desired.
    if debug:
        print("envoy command: {}".format(r.command))
        # standard convention: pass 0 for success, 1 or higher for fail
        print("envoy status: {}".format(r.status_code))
        # todo: print only if it is a reasonable length!
        # print("envoy std_out: {}".format(r.std_out))
        print("envoy std_err: {}".format(r.std_err))

    # todo: sometimes commands are failing and this doesn't print.
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
    """
    Convert a sample name like '112_LoW13' or just '112' to the file path of
    that sample's bam file.

     Note: returns the first match, so you need to start with a fully
     specified string!

    :param sample: string that specifies a sample uniquely
    :return: file path to the original .bam file in /workspace/
    """
    # convert something like XY_HOWZ --> a file path for the bam
    home_dir = '/gscratch/lidstrom/meta4_bins/workspace/'
    # make a list of candidate files.  Will check that length is 1.
    candidate_files =[]
    for root, dirs, files in os.walk(home_dir, topdown=False):
        for name in files:
            if sample in name:
                if name.endswith('.bam'):
                    path_to_bam = os.path.join(root, name)
                    print('found path to sample {}: {}'.format(
                        sample, path_to_bam))
                    candidate_files.append(path_to_bam)
    # check that only one file was found (was string fully specific?)
    if len(candidate_files)==1:
        return candidate_files[0]
    else:
        return "error: many candidate files found. \n {}".format(
            candidate_files)


def check_file_exists(filepath):
    # return True if the .fasta at filepath already exist.
    return os.path.isfile(filepath)


def sample_name_to_fasta_name(sample_name, dest_dir):
    return dest_dir + '/fasta_files/' + sample_name + '.fasta'


def sample_name_to_blasted_name(sample_name, dest_dir):
    return dest_dir + '/blast_results/' + sample_name + '-blasted.tsv'


def bam_to_fasta(source_bam, dest_fasta, sam_flag=4,
                 debug=False, intermediate_sam=True):
    if intermediate_sam:
        print("run bam_to_fasta() by making an intermediate .sam file")
    else:
        print("run bam_to_fasta() without making an intermediate .sam file")
    # make sure the .bam file exists
    #print('convert bam to fasta: {}'.format(source_bam))
    assert(os.path.exists(source_bam))

    # take an input .bam file, grab reads with flag=sam_flag, subsmple
    # those results, to the percent specified by subsample, and save a
    # .fasta with the selected reads
    # todo: implement subsampling with -s command.

    if intermediate_sam:
        # run just the first command and save to an intermediate file
        intermediate_sam_path = './dev/temp_int_sam.sam'
        command_1 = \
            "/work/software/samtools/bin/samtools view -f {} {}".format(
                sam_flag, source_bam)
        print("run shell command that makes intermediate .sam file:")
        print(command_1)
        print("save to: {}".format(intermediate_sam_path))
        shell(command_1, intermediate_sam_path, debug=debug)
        # confirm the .sam file was made.
        print('file {} exists: {}'.format(
            intermediate_sam_path, check_file_exists(intermediate_sam_path)))
    # can use triple quotes to have mixed ' and " in python.
    # NEED TO USE \\n not \n
    # source: http://stackoverflow.com/questions/15280050/calling-awk-from-python
    command_2 = """ awk '{OFS="\\t"; print ">"$1"\\n"$10}' """

    if intermediate_sam:
        # run samtools on the intermediate .sam file
        command = command_2 + intermediate_sam_path
        print('run sam to fasta command:')
        print(command)
        print('save to: {}'.format(dest_fasta))
        shell(command, dest_fasta, debug=debug)

        # remove the intermediate .sam file
        print('remove the intermediate .sam file: {}'.format(
            intermediate_sam_path))
        command= 'rm {}'.format(intermediate_sam_path)
        print('rm command: \n {}')
        shell(command, debug=debug)
    else:
        # This loop runs if you don't make an intermediate file.
        print("intermediate_file set to {}: don't write .sam "
              "on way to .fasta".format(intermediate_sam))
        command_1 = \
            "/work/software/samtools/bin/samtools view -f {} {}".format(
                sam_flag, source_bam)
        command_string = command_1 + " | " + command_2
        print("run this shell command that takes .bam to .fasta: ")
        print(command_string)
        print("save standard out to: {}".format(dest_fasta))
        # run the command.
        shell(command_string, outfile=dest_fasta, debug=debug)
        print("!!!!!!!!  WARNING !!!!!!!!!!  Files are truncated to 8.0MB "
              "if you don't write an intermediate .sam file")

    # WORKS:
    # command_string = """ /work/software/samtools/bin/samtools view -f 4
    # /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\\n"$10}' """
    #     # don't run the >.  Use envoy, wrapped in shell() to do this.
    #     # - > ./fasta_files/112_LOW13_unmapped.fasta """

    pass


def blast_fasta(in_file, out_file,
                word_size=24, threads=12,
                outfmt=None, sample_frac=0.10):
    if not outfmt:
        outfmt = '"6 stitle qseqid sseqid ' \
                 'pident length mismatch gapopen qstart qend sstart" '
    print("blast output format: {}".format(outfmt))

    blast_command = \
        "blastn -db /work/data/blast_db/nt -query {fasta} " \
        "-word_size {wordsize} -ungapped -outfmt {format}" \
        "-show_gis -max_target_seqs 1 -num_threads {threads}".format(
            fasta=in_file, format=outfmt, wordsize=word_size, threads=threads)

    print('command to blast: {}'.format(blast_command))
    print('save blast output to: {}'.format(out_file))
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


def pairwise(iterable):
    """
    Take an iterable object (like a list) and return tuple pairs.

    Used for .fasta files to return tuples of (seq_name, sequence), which
    is helpful for downsampling.

    # Example: ['a', 1, 'b', 2, 'c', 3] --> [('a', 1), ('b', 2), ('c', 3)]

    :param iterable: The object (e.g. .fasta read in) to lump into pairs
    :return: Iterable of tuples.
    """

    # "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    # http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    #  for l, d in pairwise(['a', 1, "b", 2, "c", 3]): print l
    a = iter(iterable)
    return itertools.izip(a, a)


def downsample_fasta(fasta_path, n = 10):
    """
    BLAST is the slowest step in this analysis.
    This function returns every nth sequence.
    So if fasta_path points to a fasta file with 1000 sequences and n = 10,
    a file with 1000/10 sequences is written.  That file's name is returned.

    :param fasta_path: path to fasta file you want to downsample
    :param n: downsampling severity.  Only keep (about) sequences/n sequences.
    :return: filename to downsampled .fasta file.  Has the n appended,
            like .fasta1000
    """
    # make output_filename
    out_name = fasta_path + str(n)
    print("output file name for fasta downsampling: {}".format(out_name))
    with open(fasta_path, "r") as source_file, \
            open(out_name, 'w') as dest_file:
    # keep every nth line
    # todo: shuffle it?
        # loop over pairs of lines, and skip the lines that aren't the nth:
        for desc, seq in itertools.islice(pairwise(source_file), 0, None, n):
            # write these pairs of lines to a new file
            # skip this line if n doesn't say keep.
            dest_file.writelines(desc)
            dest_file.writelines(seq)
    # File writing complete.

    # todo: Check that the correct number of lines was written.
    # return the resulting filename
    return(out_name)



