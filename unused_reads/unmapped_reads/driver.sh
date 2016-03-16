
# # gather unmapped reads:
# /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam > ./bam_files/112_LOW13_unmapped.bam
# echo "gathered reads for 112_LOW13"
# /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasMet70_HOW9_2/bwa/LakWasMet70_HOW9_2.sorted.bam > ./bam_files/70_HOW9_unmapped.bam
# echo "gathered reads for 70_HOW9"
# /work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasMet32_HOW6_2/bwa/LakWasMet32_HOW6_2.sorted.bam > ./bam_files/32_HOW6_unmapped.bam
# echo "gathered reads for 32_HOW6_2"

# /work/software/samtools/bin/samtools view ./bam_files/112_LOW13_unmapped.bam |awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/112_LOW13_unmapped.fasta
# echo "done with 112_LOW13.  Num lines: "
# wc -l 112_LOW13_unmapped.fasta
# 
# /work/software/samtools/bin/samtools view ./bam_files/32_HOW6_unmapped.bam |awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/32_HOW6_unmapped.fasta
# echo "done with 32_HOW6.  Num lines: "
# wc -l 32_HOW6_unmapped.fasta
# 
# /work/software/samtools/bin/samtools view ./bam_files/70_HOW9_unmapped.bam.bam |awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/70_HOW9_unmapped.bam.fasta
# echo "done with 70_HOW9.  Num lines: "
# wc -l 70_HOW9_unmapped.fasta

# do one more directly: don't store intermediate .bam
/work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/112_LOW13_unmapped.fasta
echo "gathered reads and made .fasta for 112_LOW13"

/work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasMet70_HOW9_2/bwa/LakWasMet70_HOW9_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/70_HOW9_unmapped.fasta
echo "gathered reads and made .fasta for 112_LOW13"

/work/software/samtools/bin/samtools view -f 4 /gscratch/lidstrom/meta4_bins/workspace/LakWasMe82_HOW10_2/bwa/LakWasMe82_HOW10_2.sorted.bam | awk '{OFS="\t"; print ">"$1"\n"$10}' - > ./fasta_files/82_HOW10_unmapped.fasta
echo "gathered reads and made .fasta for 112_LOW13"


# Blast Each of them.

blastn -db /work/data/blast_db/nt -query ./fasta_files/112_LOW13_unmapped.fasta -word_size 24 -ungapped -outfmt 6 -show_gis -max_target_seqs 1 -num_threads 12 > ./blast_output/112_LOW13.tsv
echo "done BLASTing 112_LOW13_unmapped.fasta"
blastn -db /work/data/blast_db/nt -query ./fasta_files/70_HOW9_unmapped.fasta -word_size 24 -ungapped -outfmt 6 -show_gis -max_target_seqs 1 -num_threads 12 > ./blast_output/70_HOW9.tsv
echo "done BLASTing 70_HOW9_unmapped.fasta"
blastn -db /work/data/blast_db/nt -query ./fasta_files/82_HOW10_unmapped.fasta -word_size 24 -ungapped -outfmt 6 -show_gis -max_target_seqs 1 -num_threads 12 > ./blast_output/82_HOW10.tsv
echo "done BLASTing 32_HOW6_unmapped.fasta"

