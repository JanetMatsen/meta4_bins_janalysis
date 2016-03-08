library(DESeq2)

# Load in the un-normalized table with all samples and all organisms.  
tsvFile <- '../assemble_summaries/summary_genome.dat'

print(tsvFile)

masterD <- read.table(tsvFile, sep="\t", header=T, quote="", row.names=1)

countData <- masterD
head(countData)
# remove all 0 rows
countData <- countData[rowSums(countData[, -1]) > 0, ]
head(countData)


# Read in the experiment info; imperative for DESeq's normalization scheme. 
# ---------FIX: added sample_info to current dir for development on local computer-----------------
colData <- read.table("../sample_info.xls", sep="\t", header=T, quote="", row.names=1)
#colData <- read.table("./sample_info.xls", sep="\t", header=T, quote="", row.names=1)
head(colData)

dds <- DESeqDataSetFromMatrix(countData = countData,
                              colData = colData,
                              design = ~ week + O2)
# remove rows with all zeros before applying DESeq. 
dds <- dds[ rowSums(counts(dds)) > 1, ]
#dds <- DESeq(dds)
#res <- results(dds)
#rld <- rlog(dds)
#head(assay(rld), 3)
vsd <- varianceStabilizingTransformation(dds)
head(assay(vsd), 3)
normCounts <- assay(vsd)

write.table(normCounts, file='genome_normalized_counts.tsv', quote=FALSE, sep='\t')
