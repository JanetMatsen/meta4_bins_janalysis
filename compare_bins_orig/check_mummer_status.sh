# The number of completed runs:
COMPLETED=`find ./results/mummer_results/ -type f -name '*.tsv' | wc -l`
echo "completed: $COMPLETED"

NUM_BINS=($(wc -l support_files/bin_summary.csv))
echo "number of bins: $NUM_BINS"

NUM_RUNS=`expr $NUM_BINS \* $NUM_BINS`
echo "number of runs: $NUM_RUNS"

RUNS_LEFT=`expr $NUM_RUNS - $COMPLETED`

echo "number of runs left: $RUNS_LEFT"

#FRAC_COMP=`expr $COMPLETED / $NUM_RUNS`
#echo "fraction completed: $FRAC_COMP"

