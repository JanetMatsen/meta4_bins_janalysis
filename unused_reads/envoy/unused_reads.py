import os
import time

import envoy

def write_to_file(text, filename, prepend_datetime=True):
    with open(filename, 'a') as myfile:
            if prepend_datetime:
                myfile.write("Current date & time " +
                             time.strftime("%c") + '\n')
            myfile.write(text)
    pass


def shell(command, outfile=None,
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
    return  './blast_results' + sample_name + '-blasted.tsv'


# def bam_to_fasta(source_path, dest_path, std_out_file,
#                  sam_flag=4, header=True, subsample=0.01):
#     # make sure the .bam file exists
#     print('convert bam to fasta: {}'.format(source_path))
#     assert(os.path.exists(source_path))
#
#     # take an input .bam file, grab reads with flag=sam_flag, subsmple
#     # those results, to the percent specified by subsample, and save a
#     # .fasta with the selected reads
#     # command_1 = "/work/software/samtools/bin/samtools view -f 4 {}".format(
#     #     source_path)
#     # print(command_1)
#     # # can use triple quotes to have mixed ' and " in python.
#     # command_2 = """ | awk '{OFS="\t"; print ">"$1"\n"$10}' """
#     # print(command_2)
#     # command_3 = """ - > ./fasta_files/{}""".format(dest_path)
#     # command_string = command_1 + command_2 + command_3
#
#     # # demo of shell, which wraps envoy, which runs shell.
#     # shell("""tree""", outfile=std_out_file)
#     # shell("""echo "hello Janet" """, outfile=std_out_file)
#     # shell('echo "hello Janet - single quotes"', outfile=std_out_file)
#     # shell("""echo 'Janet says "Hello!". "!' """, outfile=std_out_file)
#
#     #command_string = """ /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\n"$10}' """
#     # don't run the >.  Use envoy, wrapped in shell() to do this.
#     # - > ./fasta_files/112_LOW13_unmapped.fasta """
#
#     print('abcd')
#     print 'abcde'
#     command_string = """ /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam """
#     print("run this shell command: ")
#     print(command_string)
#     shell(command_string, outfile=dest_path, prepend_datetime=False)
#
#     # do the awk part.
#     # I wanted to do this: """awk '{OFS="\t"; print ">"$1"\n"$10}'  """
#     # But it splits on all the spaces.  I tested removing the spaces in shell,
#     # then tried them here.
#     # Motivation to remove spaces came from:
#     # http://stackoverflow.com/questions/15414244/awk-from-python-wrong-subprocess-arguments
#     command_string2a = """awk '{OFS="\t";print">"$1"\n"$10}'"""
#     command_string2 = command_string2a + dest_path
#
#     # print the 5_lines.sam file to the terminal
#     command_string2 = """awk '{OFS="\t";print">"$1"\n"$10}' ./dev/5_lines.sam"""
#     shell('cat ./dev/5_lines.sam')
#     print("command string 2:")
#     print(command_string2)
#     outfile2=dest_path + "2"
#     print(outfile2)
#     shell(command_string2, outfile=outfile2, prepend_datetime=False)


def awk():
    print "can print without call"
    print("but can also print with a call")

    command_string2 = """awk '{OFS="\t";print">"$1"\\n"$10}' ./dev/5_lines.sam"""
    #shell('cat ./dev/5_lines.sam')
    print("command string 2:")
    print(command_string2)
    shell(command_string2, debug=True)
    shell(command_string2, outfile='awked.fasta',
          debug=True, prepend_datetime=False)

    pass


def blast_fasta(in_file, out_file, outfmt=None):
    if not outfmt:
        outfmt = "6 sscinames scomnames sblastnames stitle qseqid sseqid " \
                 "pident length mismatch gapopen qstart qend sstart"

    blast_command = 'blastn -db /work/data/blast_db/nt -query {} ' \
                    '-word_size 24 -ungapped -outfmt {} -show_gis -max_target_seqs 1 ' \
                    '-num_threads 12 > {}'.format(in_file, outfmt, out_file)
    print(blast_command)
    # qseqid   --> Query Seq-id    (default)
    # sseqid   --> Subject Seq-id  (default)
    # pident   --> Percentage of identical matches  (default)
    # length   --> Alignment length  (default)
    # mismatch --> Number of mismatches (default)
    # gapopen  --> Number of gap openings (default)
    # qstart   --> Start of alignment in query (default)
    # qend     --> End of alignment in query (default)
    # sstart   --> Start of alignment in subject (default)
    pass



