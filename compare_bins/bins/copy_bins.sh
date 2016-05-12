mkdir -p fasta_files

rm fasta_files/*

./get_dave_bins/get_dave_bins.sh
./get_fauzi_bins/copy_fauzi_bins.sh
./get_isolate/get_isolate_bins.sh

# change all bin names from .fasta to .fna, which Dave seems to prefer
for file in ./fasta_files/*.fasta ; do mv $file `echo $file | sed 's/\(.*\.\)fasta/\1fna/'` ; done
