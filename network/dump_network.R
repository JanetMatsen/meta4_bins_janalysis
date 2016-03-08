library(GeneNet)
library(RColorBrewer)
library(Rgraphviz)

#load('network.R.RData')

#node.labels = colnames(df)
#gr = network.make.graph(net, node.labels, drop.singles=TRUE)

#save.image('network.R.with_gr.RData')
load('network.R.with_gr.RData')

grEdges <- edgeWeights(gr)
nodeNames <- names(grEdges)

write(paste('source', 'target', 'weight', 'association', sep='\t'),
	  'network.txt', append=F)

limitEdges=F
limitEdges=T
limitPrefixes=c('Ga0081641', 'Ga0081629')
limitPrefixes=c('Ga0081607', 'Ga0081629')
limitColors=brewer.pal(n=length(limitPrefixes), 'Dark2')
if (limitEdges)
	write(paste('node', 'color', sep='\t'), 'nodes.txt', append=F)

nodeIter <- function(nodeName) {
	edgeNames <- names(grEdges[[nodeName]])
	valid <- T
	if (limitEdges) {
		splitLT <- strsplit(nodeName, '_', fixed=T)
		idx <- match(splitLT[[1]][1], limitPrefixes, nomatch=0)
		if (idx > 0) {
			write(paste(nodeName, limitColors[idx], sep='\t'), 
				  'nodes.txt', append=T)
		} else
			valid <- F
	}
	if (valid) {
		null <- lapply(setNames(edgeNames, edgeNames), 
			function(edgeName) { 
				includeEdge <- T
				if (limitEdges) {
					splitLT <- strsplit(edgeName, '_', fixed=T)
					idx <- match(splitLT[[1]][1], limitPrefixes, nomatch=0)
					if (idx == 0)
						includeEdge <- F
				}
				if (includeEdge) {
					weight = grEdges[[nodeName]][[edgeName]] 
					if (weight > 0) format = 'positive' else format = 'negative'
					write(paste(nodeName, edgeName, weight, format, sep='\t'),
					  	  'network.txt', append=T)
				}
			}
		)
	}
}

null <- lapply(setNames(nodeNames, nodeNames), nodeIter)
