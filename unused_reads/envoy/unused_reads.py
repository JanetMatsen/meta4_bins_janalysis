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


def sample_name_to_fasta_name(sample_name):
    return './fasta_files/' + sample_name + '.fasta'


def sample_name_to_blasted_name(sample_name):
    return './blast_results/' + sample_name + '-blasted.tsv'


def bam_to_fasta(source_bam, dest_fasta, sam_flag=4, subsample=0.01,
                 debug=False, intermediate_file=False):
    if not intermediate_file:
        return "ERROR: I haven't proven this function works without writing " \
               "an intermediates .sam file"
    # make sure the .bam file exists
    #print('convert bam to fasta: {}'.format(source_bam))
    assert(os.path.exists(source_bam))

    # take an input .bam file, grab reads with flag=sam_flag, subsmple
    # those results, to the percent specified by subsample, and save a
    # .fasta with the selected reads
    # todo: implement subsampling with -s command.

    if intermediate_file:
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

    if intermediate_file:
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
        command_1 = \
            "/work/software/samtools/bin/samtools view -f {} {}".format(
                sam_flag, source_bam)
        command_string = command_1 + " | " + command_2
        print("run this shell command that takes .bam to .fasta: ")
        print(command_string)
        print("save standard out to: {}".format(dest_fasta))
        # run the command.
        shell(command_string, outfile=dest_fasta, debug=debug)

    # WORKS:
    # command_string = """ /work/software/samtools/bin/samtools view -f 4
    # /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\\n"$10}' """
    #     # don't run the >.  Use envoy, wrapped in shell() to do this.
    #     # - > ./fasta_files/112_LOW13_unmapped.fasta """

    pass


def blast_fasta(in_file, out_file, outfmt=None):
    # TODO: I don't elive the triple quote wrapped lines below work.
    if not outfmt:
        outfmt = '"6 stitle qseqid sseqid ' \
                 'pident length mismatch gapopen qstart qend sstart" '
    print("blast output format: {}".format(outfmt))

    blast_command = \
        "blastn -db /work/data/blast_db/nt -query {}" \
        "-word_size 24 -ungapped -outfmt {}" \
        "-show_gis -max_target_seqs 1 -num_threads 12".format(in_file, outfmt)
        # 'blastn -db /work/data/blast_db/nt -query {} '.format(in_file) + \
        # '-word_size 24 -ungapped -outfmt {}'.format(outfmt) + \
        # '-show_gis -max_target_seqs 1 -num_threads 12 > {}'
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




