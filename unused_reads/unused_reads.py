import itertools

import os
import re
import time

import envoy

# TODO: assert that it is python 2.  envoy seemed to freak out with Python 3.
# see demo on my laptop.


SAMPLES = ['112_LOW13', '82_HOW10', '70_HOW9', '57_HOW8', '32_HOW6',
           '19_HOW5', '74_LOW10']
# 74_LOW10 is a control: turned out pretty well.



def write_to_file(text, filepath, prepend_datetime=False):
    """
    Write text (usually standard output from envoy) to file.

    Designed to be called from shell()
    :param text: test to write to file
    :param filepath: path to save output file to
    :param prepend_datetime: option to record current date and time
    :return: nothing
    """
    with open(filepath, 'a') as myfile:
            if prepend_datetime:
                myfile.write("Current date & time " +
                             time.strftime("%c") + '\n')
            myfile.write(text)
    pass


def shell(command, outfile=None,
          prepend_datetime=False, debug=False):
    """
    Execute a command line call.

    Prints to the terminal if outfile is not specified.

    Wrapper for envoy package, which wraps python's subprocess built-in

    :param command: command (as string) to run via envoy.  Escape
    backslashes (\\n not \n)
    :param outfile: file path to write to.  If not specified, standard out
    is printed (and not saved)
    :param prepend_datetime: Option to record when the command was run.  (
    Not usually used)
    :param debug: Use debug mode?  Prints the command used, exit status, and
    standard error.  Will (eventually) print a preview of standard error,
    but currently doesn't support that.
    :return:
    """
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
        write_to_file(r.std_out, filepath=outfile,
                      prepend_datetime=prepend_datetime)
    pass


def create_dir(directory):
    """
    Create a directory if it doesn't already exist.

    :param directory: path to a directory
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_file_exists(filepath):
    """
    Return True if the specified file path exists, and False if not

    :param filepath: path to the file under investigation
    :return: True if file exists, False if not.
    """
    # return True if the .fasta at filepath already exist.
    return os.path.isfile(filepath)


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
    candidate_files = []
    for root, dirs, files in os.walk(home_dir, topdown=False):
        for name in files:
            if sample in name:
                if name.endswith('.bam'):
                    path_to_bam = os.path.join(root, name)
                    print('found path to sample {}: {}'.format(
                        sample, path_to_bam))
                    candidate_files.append(path_to_bam)
    # check that only one file was found (was string fully specific?)
    if len(candidate_files) == 1:
        return candidate_files[0]
    else:
        return "error: many candidate files found. \n {}".format(
            candidate_files)


def sample_name_to_fasta_path(sample_name, dest_dir):
    """
    Convert sample name like '70_HOW9' to a file path to save the .fasta
    file in

    :param sample_name: a string specifying a sample name, typically like
     '70_HOW9'
    :param dest_dir: directory to save to
    :return: file path string
    """
    return dest_dir + '/fasta_files/' + sample_name + '.fasta'


def sample_name_to_blasted_path(sample_name, dest_dir):
    """
    Create a path to put a blast result in, using a sample name and
    destination directory.

    :param sample_name: e.g. '70_HOW9'
    :param dest_dir:  directory to place file in
    :return: file path string
    """
    return dest_dir + '/blast_results/' + sample_name + '-blasted.tsv'


def bam_to_fasta(source_bam, dest_fasta, sam_flag=4,
                 debug=False, intermediate_sam=True):
    """
    Convert a .bam file to a .fasta using samtools and the specified
    samtools flag.

    :param source_bam: file path to .bam file to extract reads from
    :param dest_fasta: file path to save resulting .fasta file to
    :param sam_flag: samtools flag to use.
    :param debug: run in debug mode?  Passed to all envoy shell commands.
    :param intermediate_sam: Write an intermediate .sam file (that gets
    deleted) on the way to the .fasta file?  Currently only True is
    supported; envoy truncated my piped commands at 8.0kb in tests.
    :return:
    """

    # dictionary that converts description of a samtools flag into a
    # numerical value used in the samtools call.
    samtools_flag_converter = {'unmapped': 4, 'multiple': 256}
    # if the samtools flag passed was a string, convert it to a bit flag.
    if type(sam_flag) == str:
        try:
            sam_flag = samtools_flag_converter[sam_flag]
        except LookupError:
            print "error: sam string {} could not be converted to " \
                  "a samtools command".format(sam_flag)

    if intermediate_sam:
        print("run bam_to_fasta() by making an intermediate .sam file")
    else:
        print("run bam_to_fasta() without making an intermediate .sam file")

    # make sure the .bam file exists
    assert(os.path.exists(source_bam))

    if intermediate_sam:
        # run just the first command and save to an intermediate file
        # write the temp file into the .fasta dir.
        intermediate_sam_path = 'dest_fasta'.rstrip('.fasta') + '.sam'
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
    # source:
    # http://stackoverflow.com/questions/15280050/calling-awk-from-python
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
        command = 'rm {}'.format(intermediate_sam_path)
        print('rm command: \n {}')
        shell(command, debug=debug)
    else:
        # SKIPPING INTERMEDIATE .sam FILE DOESN'T WORK!  Piping w/ envoy
        # limits the file to 8kb in my experience.
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
    # /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/
    # LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\\n"$10}' """
    #     # don't run the >.  Use envoy, wrapped in shell() to do this.
    #     # - > ./fasta_files/112_LOW13_unmapped.fasta """

    pass


def blast_format_to_col_names(blast_outfmt):
    """
    Change a blast format such as '"6 stitle qseqid sseqid pident length"'
    to a tab-separated line that can be used for .tsv column names such as
    "stitle    qseqid    sseqid    pident    length"

    :param blast_outfmt: a blast
    :return: string with tabs between column names
    """
    # first check that the blast_outfmt is type 6, the type this is designed
    #  to support.
    assert(blast_outfmt.startswith('"6 ')), \
        'only designed for BLAST outfmt type 6, e.g. ' \
        '"6 stitle qseqid sseqid pident length evalue" '

    # strip off the leading digit:
    colnames = re.sub("\d+ ", "", blast_outfmt)
    # replace spaces with tabs.
    colnames = re.sub(" ", "\t", colnames)
    return colnames


def blast_fasta(in_file, out_file,
                blast_db='nt',
                word_size=24, max_target_seqs=1, threads=12,
                outfmt=None):
    """
    Blast a fasta file, save as .tsv

    :param in_file: path to .fasta file to BLAST
    :param out_file: path to save the file at
    :param blast_db: path to the blast database to use OR nick name.  Nick
    name can be 'nt' or 'bins'.
    :param word_size: BLAST setting.  Larger --> faster & less sensitive
    :param max_target_seqs: maximum number of blast hits to return.
    :param threads: BLAST setting for parallelization
    :param outfmt: output format to use (optional)
    :return: saves a blast file, and returns the path to the file
    """
    if not outfmt:
        outfmt = '"6 stitle qseqid sseqid ' \
                 'pident length evalue bitscore ' \
                 'mismatch gapopen qstart qend sstart send" '
    print("blast output format: {}".format(outfmt))

    blast_db_paths = {'nt': '/work/data/blast_db/nt',
                      'bins': '/work/data/blast_db/genome_bins'}
    if blast_db in blast_db_paths.keys():
        blast_db = blast_db_paths[blast_db]

    blast_command = \
        "blastn -db {db} -query {fasta} " \
        "-word_size {wordsize} -ungapped -outfmt {format}" \
        "-show_gis -max_target_seqs {mts} -num_threads {threads}".format(
            db=blast_db, fasta=in_file, wordsize=word_size, format=outfmt,
            mts=max_target_seqs, threads=threads)

    print('command to blast: {}'.format(blast_command))
    print('save blast output to: {}'.format(out_file))
    # stitle   --> Subject Title
    # qseqid   --> Query Seq-id    (default)
    # sseqid   --> Subject Seq-id  (default)
    # pident   --> Percentage of identical matches  (default)
    # length   --> Alignment length  (default)
    # evalue   --> Expect value
    # bitscore --> Bit score
    # mismatch --> Number of mismatches (default)
    # gapopen  --> Number of gap openings (default)
    # qstart   --> Start of alignment in query (default)
    # qend     --> End of alignment in query (default)
    # sstart   --> Start of alignment in subject (default)
    # send     --> End of alignment in subject

    # write the column names to file first.
    colnames = blast_format_to_col_names(outfmt)
    shell('echo {}'.format(colnames), outfile=out_file)
    # run the shell command (envoy)
    shell(blast_command, outfile=out_file)
    pass


def pairwise(iterable):
    """
    Take an iterable object (like a list) and return tuple pairs.

    Used for .fasta files to return tuples of (seq_name, sequence), which
    is helpful for downsampling.

    Example: ['a', 1, 'b', 2, 'c', 3] --> [('a', 1), ('b', 2), ('c', 3)]

    ** When used on a .fasta file, it assumes one-line sequences!! **

    :param iterable: The object (e.g. .fasta read in) to lump into pairs
    :return: Iterable of tuples.
    """

    # "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    # http://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    #  for l, d in pairwise(['a', 1, "b", 2, "c", 3]): print l
    a = iter(iterable)
    return itertools.izip(a, a)


def downsample_fasta_islice(fasta_path, n=10):
    """
    BLAST is the slowest step in this analysis.
    This function returns every nth sequence.
    So if fasta_path points to a fasta file with 1000 sequences and n = 10,
    a file with 1000/10 sequences is written.  That file's name is returned.

    NOTE: assumes the sequences are only one line each.

    :param fasta_path: path to fasta file you want to downsample
    :param n: downsampling severity.  Only keep (about) sequences/n sequences.
    :return: filename to downsampled .fasta file.  Has the n appended,
            like .fasta1000
    """
    # make output_filename
    out_name = fasta_path.rstrip('.fasta') + '_{}.fasta'.format(n)
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
    # todo: check that every other line starts with a >
    # If not every other line starts with >, then the sequences might have
    # been multi-line
    # return the resulting filename
    return out_name


def run_pipeline(samples_to_investigate, parent_directory,
                 blast_db,
                 verbose=True, sam_flag='unmapped',
                 downsample_granularity=10000,
                 word_size=24, max_target_seqs=1):
    """
    Run the analysis pipeline for a given set of samples to investigate.

    Doesn't re-make the full length .fasta from .bam if it already exists (
    should come out the same).  This will be bad if you change the samtools
    call!

    :param samples_to_investigate: list of sample names like '57_HOW8'
    :param parent_directory: directory to put the whole analysis in
    :param verbose: print information about envoy commands?
    :param sam_flag: sam flag to filter on.  Can be a string or numerical
    :param downsample_granularity: only keep every n th sample (bigger --> less kept)
    :param word_size: BLAST parameter for initial match size
    :param max_target_seqs: BLAST parameter for number of sequences to keep
    :return:
    """

    # todo: sanatize so parent_directory could be './dirname' or './dirname'
    # or 'dirname' etc.
    create_dir(parent_directory)
    create_dir(parent_directory + '/fasta_files')
    create_dir(parent_directory + '/blast_results')

    for sample in samples_to_investigate:
        if verbose:
            print("start work for sample: {}".format(sample))

        # get the path to the original BAM file
        bam_file = sample_name_to_bam_filepath(sample)
        if verbose:
            print("bam file path: {}".format(bam_file))

        # identify a filepath/name for the output fasta
        sample_fasta = sample_name_to_fasta_path(sample, parent_directory)

        if check_file_exists(sample_fasta):
            print("fasta {} exists already; don't make from .bam".format(
                sample_fasta))
        else:
            print("generate .fasta for {}".format(sample))
            bam_to_fasta(source_bam=bam_file,
                            dest_fasta=sample_fasta,
                            sam_flag=sam_flag)
        # check that the blasted file exists now.
        assert(check_file_exists(sample_fasta))

        # downsample the fasta so BLAST doesn't take *forever*
        # downsample_fasta_islice() returns path to downsampled fasta.
        downsampled_fasta = downsample_fasta_islice(sample_fasta,
                                                    downsample_granularity)

        # todo: the blast step takes the longest.  Only run if the
        # downsampled_fasta I want to blast is recent??
        # blast the results
        sample_blasted = \
            sample_name_to_blasted_path(
                sample + "_" + str(downsample_granularity),
                parent_directory)
        print('blast downsampled fasta.  Store results as {}'.format(
            sample_blasted))
        # do the blasting
        # remove old file if its length is zero
        if check_file_exists(sample_blasted):
            with open(sample_blasted) as f:
                num_lines = len(f.readlines())
            if num_lines != 0:
                print("fasta {} already exists.".format(sample_blasted))
        else:
            print("blast {} and save as {}".format(downsampled_fasta,
                                                   sample_blasted))
            blast_fasta(in_file=downsampled_fasta,
                        out_file=sample_blasted,
                        blast_db=blast_db,
                        word_size=word_size,
                        max_target_seqs=max_target_seqs)
        # check that the blasted file exists now.
        assert(check_file_exists(sample_blasted))


    def downsample_and_blast(input_fasta, output_blast_path,
                             downsample_granularity):
        # todo: write a function to downsample and blast a single file.
        pass
