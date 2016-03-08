library(DESeq2)
# Drop XLConnect: Java memory error.
# library(XLConnect)
# Use openxls, not XLConnect.  Uses C and no java. 
library('openxlsx')


# Get all arguments after --args
args <- commandArgs(trailingOnly=TRUE)
print(args)


# Load in the un-normalized table with all samples and all genomes.  
tsvFile <- args[1]  
# from: 
# /gscratch/lidstrom/meta4/analysis/assemble_summaries (master) $ head summary.dat

# we will restrict to normalizing all rows of the 88 samples for 1 genome at a time. 
genome <- args[2] 

print(tsvFile)
print(genome)

normalize_genome <- function(genome,dirname,workbook){
    print(paste("begin normalize_genome for", genome))    
    # Select just the data for the genome of interest. 
    countData <- masterD[masterD$genome == genome, ]
    
    # remove all 0 rows
    print("countData[, 1:10]: BEFORE removing zero rows.")
    print(head(countData[,1:10]))
    countData <- countData[rowSums(countData[, -(1:2)]) > 0, ]
    print("countData[, 1:10]: after removing zero rows.")
    print(head(countData[,1:10]))
    
    # save the genome, product info to merge back on at the end.
    print("head(countData): pre define of geneinfo")
    print(head(countData))
    geneInfo <- countData[c("genome", "product")]
    print("head(geneInfo)")
    print(head(geneInfo))
    
    # Delete the genome and product columns; they aren't read counts and DESeq doesn't want them. 
    countData$genome <- NULL
    countData$product <- NULL

    # use colData imported below
    print("colData[,1:6]:")
    print(head(colData[,1:6]))
    
    # build the experimental design table used for normalization
    print('do DESeqDataSetFromMatrix')
    dds <- DESeqDataSetFromMatrix(countData = countData,
    			      colData = colData,
    			      design = ~ week + O2) 	
    #dds <- DESeq(dds)
    #res <- results(dds)
    #print(paste('calculate rlog for', genome))
    #rld <- rlog(dds)
    #head(assay(rld), 3)
    print(paste('calculate varianceStabilizingTransformation for', genome))
    vsd <- varianceStabilizingTransformation(dds)
    normCounts <- assay(vsd)
    print("head(normCounts[3,1:6])")
    print(head(normCounts[3,1:6]))
    
    # join geneinfo with normCounts
    print("nrow(geneInfo)")
    print(nrow(geneInfo))
    print("nrow(normCounts)")
    print(nrow(normCounts))
    print("head(geneInfo[1:3,])")
    print(head(geneInfo[1:3,]))
    result = cbind(geneInfo, normCounts)

    print("head(result[, 1:6]")
    print(head(result[, 1:6]))

    
    write_norm_to_file(norm_data=result, dirname=dirname, name=name_cleanse(genome))
    #OLD: save_to_xls(workbook=workbook, data=result, name=organism)
    write_xls(workbook=workbook, data=result, name=genome)
    }

name_cleanse <- function(x){
    print(x)
    x = gsub(' ', '_', x) 
    x = gsub('/', '-', x)
    return(x)
    }
# test: 
print("test name_cleanse() on Methylobacter tundripaludum 21/22")
print(name_cleanse('Methylobacter tundripaludum 21/22'))

write_norm_to_file <- function(norm_data, dirname, name){
    print(paste('saving to txv: name = ', name))
    name = name_cleanse(name)
    # write to tsv
    dir.create(dirname, showWarnings =FALSE)
    # concatenate the dirname and filename
    filename = paste0(dirname, "/", name, ".tsv")
    print(paste('filename:', filename)) 
    write.table(norm_data, file=filename, quote=FALSE, sep='\t', col.names = NA)
    print(paste(filename, "written"))
    }
# test write_norm_to_file()
#write_norm_to_file(norm_data = data.frame('bina'=c(1,2,3), 'tina'=c(4,5,6)), 
#                    dirname = "test_fun", 
#                    name = 'test_fun')


substrRight <- function(x, n){
  return(substr(x, nchar(x)-n+1, nchar(x)))
}


#save_to_xls <- function(workbook, data, name){
#    print(paste('saving to excel: name = ', name))
#    name = name_cleanse(name)
#    createSheet(workbook, name)
#    writeWorksheet(workbook,data,name)
#    }

# test save_to_xls()
# test save_to_xls()
#wb_test = loadWorkbook("test.xlsx",create=T)
#save_to_xls(workbook=wb_test, data=data.frame('bina'=c(1,2,3), 'tina'=c(4,5,6)), name='test 21/22')

write_xls <- function(workbook, data, name){
    print(paste('begin write_xls for', name))
    sheet_name = name_cleanse(name)
    # max sheet name is 31 char
    sheet_name = substrRight(sheet_name, 31)
    print(paste('cleansed name:', name))
    addWorksheet(wb=workbook, sheetName = sheet_name, gridLines = TRUE)
    writeDataTable(wb=workbook, sheet = sheet_name, x = data, colNames = TRUE, rowNames = FALSE, tableStyle = 'none')
    }
#wb_test = createWorkbook()
#write_xls(workbook=wb_test, data=data.frame('bina'=c(1,2,3), 'tina'=c(4,5,6)), name='test 21/22')
#saveWorkbook(wb_test, "function_test.xlsx", overwrite = TRUE) ## save to working directory

masterD <- read.table(tsvFile, sep="\t", header=T, quote="", row.names=2)
# stringsAsFactors=F
# DOES DESeq2 need factors??
# if strings aren't converted to factors, we can loop over the unique genome names. 
    # I think so.
# remove zero rows, which make DESEq2 sad. 
masterD <- masterD[rowSums(masterD[, -(1:2)]) > 0, ]
# drop some columns in masterD and d
# second locus_tag column came from merging in SQL twice: SQL has a 61 table limit!                	
masterD$locus_tag.2 <- NULL           	

# Read in the experiment info; imperative for DESeq's normalization scheme. 
# get the unique genome names for looping
colData <- read.table("../sample_info.xls", sep="\t", header=T, quote="", row.names=1)            
#colData <- read.table("./sample_info.xls", sep="\t", header=T, quote="", row.names=1)    
# convert week column to factors (a preference specified by DESeq2 output in terminal)
colData$week <- as.factor(colData[, 'week'])
# show it is in the list of columns that are factors now:
print("Show week and O2 are both in the list of columns that are factors: ")
print(names(Filter(is.factor, colData)))          
print(head(colData,3))


# try it once:
#normalize_genome("Methylotenera mobilis JLW8")
#debug(normalize_genome)

# initialize a .xls notebook:
# OLD: wb = loadWorkbook("gene_reads_normalized_by_organism.xlsx",create=T)
wb <- createWorkbook()


dirname = "read_counts_per_gene--normalized_by_genome"

genomes = unique(masterD$genome)
print(genomes)

# test known problem genome(s): 
for(g in c("Methylophilaceae-8 (UID203) ") ){

#for(g in unique(masterD$genome)){
	print(g)
	try(normalize_genome(genome=g, dirname=dirname, workbook=wb))        
	}

# save the .xls with one sheet per genome. 
# OLD: saveWorkbook(wb)
saveWorkbook(wb, "read_counts_per_gene--normalized_by_genome.xlsx", overwrite = TRUE) ## save to working directory
