# Loop over the bins that we want and make a copy of each in this dir. 
while read line; do
  file_name=$line
  file_path="/work/dacb/extract_isolates/${file_name}"
  ls -l $file_path
	#"/work/dacb/extract_isolates/${file_name}"
  cp $file_path . 
done < isolate_bins_to_get
