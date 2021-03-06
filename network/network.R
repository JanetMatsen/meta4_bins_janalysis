library("GeneNet")

pdf("network.pdf")

df <- read.table('normalized_counts.tsv', row.names=1, header=T, sep='\t')
df.order <- order(rowMeans(df), decreasing=T)
head(df[df.order, ])
df <- head(df[df.order,], 1000)
head(df)
df <- t(df)

# estimate partial correlations using shrinkage
pc <- ggm.estimate.pcor(df)
dim(pc)

# assign p-values for the potential edges
edges <- network.test.edges(pc, direct=TRUE, fdr=TRUE)
dim(edges)

edges[1:5,]

# use local fdr cutoff 0.2 (include all edges with posterior probability of at least .8)
net <- extract.network(edges)
dim(net)

# use local fdr cutoff 0.1 (include all edges with posterior probability of at least .9)
ten.net <- extract.network(edges, cutoff.ggm=0.9, cutoff.dir=0.9)
dim(ten.net)

# use a fixed number of edges, e.g. the top 10 strongest edges
fixed.net <- extract.network(edges, method.ggm="number", cutoff.ggm=10)
dim(fixed.net)

save.image(file='network.R.RData')

library("Rgraphviz") 


node.labels = colnames(df)
gr = network.make.graph(net, node.labels, drop.singles=TRUE)

toDot(gr, 'network.R.dot')

table(  edge.info(gr)$dir )
sort( node.degree(gr), decreasing=TRUE)


#' Set node and edge attributes for more beautiful graph plotting:
globalAttrs = list()
globalAttrs$edge = list(color = "black", lty = "solid", lwd = 1, arrowsize=1)
globalAttrs$node = list(fillcolor = "lightblue", shape = "ellipse", fixedsize = FALSE)
 
nodeAttrs = list()
nodeAttrs$fillcolor = c('sucA' = "yellow")

edi = edge.info(gr)
edgeAttrs = list()
edgeAttrs$dir = edi$dir # set edge directions 
edgeAttrs$lty = ifelse(edi$weight < 0, "dotted", "solid") # negative correlation -> dotted
edgeAttrs$color = ifelse(edi$dir == "none", "black", "red")
edgeAttrs$label = round(edi$weight, 2) # use partial correlation as edge labels

save.image(file='network.R.graphviz.preplot.RData')

#+ fig.width=8, fig.height=7
plot(gr, attrs = globalAttrs, nodeAttrs = nodeAttrs, edgeAttrs = edgeAttrs, "fdp")

dev.off()

save.image(file='network.R.graphviz.RData')
