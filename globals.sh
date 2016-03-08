#!/bin/bash

# to be sourced
DB=meta4_bins
HOST=`mysql_host`

# pathes
BWA=/work/software/bwa/bin/bwa
SAMTOOLS=/work/software/samtools/bin/samtools
MYSQL=mysql
MYSQL_HOST=/work/software/bin/mysql_host
HTSEQ_COUNT=/work/software/htseq/bin/htseq-count

# job parameters
QL=walltime=999:99:99,mem=2gb,feature=8core
GROUP_LIST=hyak-lidstrom
EMAIL=dacb@uw.edu,jmatsen@uw.edu
