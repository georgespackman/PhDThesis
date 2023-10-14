

def WeftInsertion(EndPositionDict, WeftInsertionNumber, BifStack, WeftStack, NumXYarns, NumWefts):
	
	i=WeftInsertionNumber
	NumWarps=9
	BeforeBifurcation = ("1"*(EndPositionDict.keys()[i]) + "0"*(NumWefts - 1 - EndPositionDict.keys()[i]) + str(WeftStack))*BifStack
	AfterBifurcation = ("1"*(EndPositionDict.values()[i]) + "0"*(NumWefts - 1 - (EndPositionDict.values()[i])) + str(WeftStack))*(NumXYarns - BifStack)
	
	file=open("patterndraft.txt", "a")
	file.write(BeforeBifurcation + AfterBifurcation + "\n")
	file.close()
	
	return (BeforeBifurcation + AfterBifurcation)
	


