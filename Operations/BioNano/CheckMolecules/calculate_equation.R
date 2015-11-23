#!/fslhome/jtpage/bin/Rscript

data <- read.table('mol_align_stats.txt', header=T, sep="\t", quote="\"'", dec=".", row.names=1, stringsAsFactors=F)
summary(data)
equation <- lm(counts ~ length, data)
summary(equation)
coefficients(equation)
