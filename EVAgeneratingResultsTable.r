setwd("C:/Users/User/AppData/Local/Packages/11888HuanLab.EVAanalysistool_8tmgtde19meca/LocalState")
featureTable <- read.csv("featureTable.csv", header = T, stringsAsFactors = F)
prediction <- read.csv("outcome.csv", header = T, stringsAsFactors = F)
featureTable <- featureTable[order(featureTable[,1], decreasing = F ),]
prediction <- prediction[order(prediction[,1], decreasing = F ),]

featureTable <- as.data.frame(cbind(featureTable$X, featureTable$mz, featureTable$rt, featureTable$maxo, prediction$prediction))
colnames(featureTable) <- c("ID", "mz", "rt", "intensity", "prediction")
featureTable$mz <- as.numeric(featureTable$mz)
featureTable$rt <- as.numeric(featureTable$rt)
featureTable$intensity <- as.numeric(featureTable$intensity)
featureTable$mz <- format(round(featureTable$mz, digits=4), nsmall = 4)
featureTable$rt <- format(round(featureTable$rt, digits=0), nsmall = 0)
featureTable$intensity <- format(round(featureTable$intensity, digits=0), nsmall = 0)
featureTable <- featureTable[order(featureTable[,2], decreasing = F ),]

write.csv(featureTable, file = "ResultsTable.csv", quote = F, row.names = F, col.names = T)
