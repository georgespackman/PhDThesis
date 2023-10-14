import os
import sys
import imp
os.chdir("E:\T-Joint")
cwd = os.getcwd()
sys.path.append(cwd)
from WeavePattern import *
from WeftInsertion import *
from DeformTPieceBentWarps import *
# imp.reload(WeavePattern)
# imp.reload(WeftInsertion)
# imp.reload(DeformTPieceBentWarps)


BinderWidth=0.67
WarpWidth=2.00
ImportWeavePattern(cwd+"\\ortho-wft_crossover+split_withbinders.txt")
#ImportWeavePattern(cwd+"\\3dv8_modified.txt")
#ImportWeavePattern(cwd+"\\Tmodel.txt")

NewDict, EndPositionDict, NumWarps, NumWefts, NumXYarns, BifStack=GetPatternInfo(cwd+"\\ortho-wft_crossover+split_withbinders.txt")
print("BifStack ", BifStack)
print("NumXYarns ", NumXYarns)
BifStack=6

Textile=GetTextile().GetOrthogonalWeave()
Weave3D=Textile.Get3DWeave()
Yarns=Textile.GetYarns()


tol=0.223

#Add nodes to shape yarns around warps
for i in range(70, 90):
	yarnsection = CYarnSectionInterpNode(bool(1), bool(0), bool(1))
	Nodes=Yarns[i].GetMasterNodes()
	for j in range(len(Nodes)):
		NextNodeIndex=j+1
		CurrentNodePosition=Nodes[j].GetPosition()
		CurrentNodeHeight=CurrentNodePosition.z
		UpVector=XYZ(0,0,1)
		if j+1 < len(Nodes):
			NextNodePosition=Nodes[j+1].GetPosition()
			NextNodeHeight=NextNodePosition.z
			PreviousNodePosition=Nodes[j+1].GetPosition()
			PreviousNodeHeight=NextNodePosition.z
			if NextNodeHeight != CurrentNodeHeight:# or j==BifStack:

				NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.2*BinderWidth, CurrentNodePosition.z))
				NewNode2=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.4*BinderWidth, CurrentNodePosition.z))
				NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.5*BinderWidth, CurrentNodePosition.z))
				NewNode1.SetUp( UpVector )
				NewNode2.SetUp( UpVector )
				NewNode3.SetUp( UpVector )
				
				Yarns[i].InsertNode(NewNode1, j+1)
				Yarns[i].InsertNode(NewNode2, j+2)
				Yarns[i].InsertNode(NewNode3, j+3)
				break
	Nodes=Yarns[i].GetMasterNodes()
	# for l in range(len(Nodes)-1, -1, -1):
		# NextNodeIndex=l-1
		# CurrentNodePosition=Nodes[l].GetPosition()
		# CurrentNodeHeight=CurrentNodePosition.z
		# UpVector=XYZ(0,0,1)
		# if l-1 > 0:
			# NextNodePosition=Nodes[l-1].GetPosition()
			# NextNodeHeight=NextNodePosition.z
			# PreviousNodePosition=Nodes[l-1].GetPosition()
			# PreviousNodeHeight=NextNodePosition.z
			# if NextNodeHeight != CurrentNodeHeight or l==NumXYarns-BifStack:# - tol:
				# NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.2*WarpWidth, CurrentNodePosition.z))
				# NewNode2=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.4*WarpWidth, CurrentNodePosition.z))
				# NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.5*WarpWidth, CurrentNodePosition.z))
				# NewNode1.SetUp( UpVector )
				# NewNode2.SetUp( UpVector )
				# NewNode3.SetUp( UpVector )
				# Yarns[i].InsertNode(NewNode1, l)
				# Yarns[i].InsertNode(NewNode2, l)
				# Yarns[i].InsertNode(NewNode3, l)
				# break
	Nodes=Yarns[i].GetMasterNodes()
	for k in range(len(Nodes)):
		#Weave3D.CheckUpVectors(i)
		if k == j+1 or k==j+2 or k==j+3:
		#if k == l or k == l+1 or k == l+2:
			section = CSectionPowerEllipse(0.65, 0.235, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)
		else:
			section = CSectionPowerEllipse(2*0.446, 0.333, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)

	Yarns[i].AssignSection( yarnsection )


for i in range(70, 90):
	yarnsection = CYarnSectionInterpNode(bool(1), bool(0), bool(1))
	# Nodes=Yarns[i].GetMasterNodes()
	# for j in range(len(Nodes)):
		# NextNodeIndex=j+1
		# CurrentNodePosition=Nodes[j].GetPosition()
		# CurrentNodeHeight=CurrentNodePosition.z
		# UpVector=XYZ(0,0,1)
		# if j+1 < len(Nodes):
			# NextNodePosition=Nodes[j+1].GetPosition()
			# NextNodeHeight=NextNodePosition.z
			# PreviousNodePosition=Nodes[j+1].GetPosition()
			# PreviousNodeHeight=NextNodePosition.z
			# if NextNodeHeight != CurrentNodeHeight:# or j==BifStack:

				# NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.2*BinderWidth, CurrentNodePosition.z))
				# NewNode2=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.4*BinderWidth, CurrentNodePosition.z))
				# NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 0.5*BinderWidth, CurrentNodePosition.z))
				# NewNode1.SetUp( UpVector )
				# NewNode2.SetUp( UpVector )
				# NewNode3.SetUp( UpVector )
				
				# Yarns[i].InsertNode(NewNode1, j+1)
				# Yarns[i].InsertNode(NewNode2, j+2)
				# Yarns[i].InsertNode(NewNode3, j+3)
				# break
	Nodes=Yarns[i].GetMasterNodes()
	for l in range(len(Nodes)-1, -1, -1):
		NextNodeIndex=l-1
		CurrentNodePosition=Nodes[l].GetPosition()
		CurrentNodeHeight=CurrentNodePosition.z
		UpVector=XYZ(0,0,1)
		if l-1 > 0:
			NextNodePosition=Nodes[l-1].GetPosition()
			NextNodeHeight=NextNodePosition.z
			PreviousNodePosition=Nodes[l-1].GetPosition()
			PreviousNodeHeight=NextNodePosition.z
			if NextNodeHeight != CurrentNodeHeight or l==NumXYarns-BifStack:# - tol:
				NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.2*WarpWidth, CurrentNodePosition.z))
				NewNode2=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.4*WarpWidth, CurrentNodePosition.z))
				NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y - 0.5*WarpWidth, CurrentNodePosition.z))
				NewNode1.SetUp( UpVector )
				NewNode2.SetUp( UpVector )
				NewNode3.SetUp( UpVector )
				Yarns[i].InsertNode(NewNode1, l)
				Yarns[i].InsertNode(NewNode2, l)
				Yarns[i].InsertNode(NewNode3, l)
				break
	Nodes=Yarns[i].GetMasterNodes()
	for k in range(len(Nodes)):
		#Weave3D.CheckUpVectors(i)
		if k == j+1 or k==j+2 or k==j+3:
		#if k == l or k == l+1 or k == l+2:
			section = CSectionPowerEllipse(0.65, 0.235, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)
		else:
			section = CSectionPowerEllipse(2*0.446, 0.333, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)

	Yarns[i].AssignSection( yarnsection )



# for i in range(0, 70):
	# yarnsection = CYarnSectionInterpNode(bool(1), bool(0), bool(1))
	# Nodes = Yarns[i].GetMasterNodes()
	# for k in range(len(Nodes)):
		# section = CSectionPowerEllipse(0.65, 0.235, 1, 0)
		# yarnsection.AddSection(section)
	# Yarns[i].AssignSection(yarnsection)
	
AddTextile(Textile)
UpperWefts=[]
LowerWefts=[]


k=0
j=0

print(NewDict.values())
for i in range(79, 69, -1):
	print(k, i, NewDict[k])
	
	try:
		if NewDict[k]!=NewDict[k+1]: #((NewDict[k]!=0 and NewDict[k+1]!=0) and NewDict[k]!=NewDict[k+1]):
			print("ADM")
			AddMidSectionNodes(i, k, BifStack, NewDict)
		k=k+1
	except KeyError:
		if NewDict[k]!=0:
			AddMidSectionNodes(i, k, BifStack, NewDict)
		k=k+1
	
	if EndPositionDict[j] < 5:
		print("Upper")
		UpperWefts.append(i)
	else:
		print("Lower")
		LowerWefts.append(i)
	j=j+1
	if j >= NumWefts:
		j=0
		

k=0
j=0
for i in range(89, 79, -1):
	try:
		if ((NewDict[k]!=0 and NewDict[k+1]!=0) and NewDict[k]!=NewDict[k+1]):# and NewDict.values()[k]!=0:
			print("ADM")
			AddMidSectionNodes(i, k, BifStack, NewDict)
		k=k+1
	except KeyError:
		if NewDict[k]!=0:
			AddMidSectionNodes(i, k, BifStack, NewDict)
		k=k+1

	
	if EndPositionDict[j] < 5:
		print("Upper")
		UpperWefts.append(i)
	else:
		print("Lower")
		LowerWefts.append(i)
	j=j+1
	if j >= NumWefts:
		j=0
		

# sort into upper and lower wefts depending on if the weft ends up in the upper or lower position in textile

AddTextile(Textile)




# # This works with no binders
BeforeBifurcationWarps=[]
UpperWarps=[] 
LowerWarps=[]
j=9
StackNumber=0
first=True

# # need to get the warp yarns in the stack before bifurcation (27 - 35)
for i in range(BifStack*(NumWarps+1)+1, BifStack*(NumWarps+1)+1 + (NumWarps+1), 1):
	BeforeBifurcationWarps.append(i)
	
weave3D=Textile.Get3DWeave()
# warps sorted into upper and lower half depending on where the wefts above and below 
for i in range((NumWarps+1)*7):
		
		Level = StackNumber*(NumWarps+1) + (NumWarps/2)
		if first:
			first=False
		elif i > Level and BeforeBifurcationWarps.count(i)==0: # + NumBinders
			UpperWarps.append(i)
		elif BeforeBifurcationWarps.count(i)==0:
			LowerWarps.append(i)
		elif EndPositionDict.values()[j+1] < 5 and EndPositionDict.values()[j] < 5:
			UpperWarps.append(i)
			print("i ", i)
			print(EndPositionDict.values()[j+1])
		elif EndPositionDict.values()[j+1] >= 5 and EndPositionDict.values()[j] >= 5:
			LowerWarps.append(i)
			print("i ", i)
		# weft below warp has same j value
		# else the wefts above and below are in different halves of textile so no bend transform
		
		
		j=j-1
		if j < 0:
			j=9
			first=True
			StackNumber=StackNumber+1
			
UpperBinderYarns=[0,20]
LowerBinderYarns=[10, 30]
BinderYarnsBeforeBifurcation=[40, 50, 60]

LowerWarps=[item for item in LowerWarps if item not in UpperBinderYarns]
LowerWarps=[item for item in LowerWarps if item not in LowerBinderYarns]
LowerWarps=[item for item in LowerWarps if item not in BinderYarnsBeforeBifurcation]
UpperWarps=[item for item in UpperWarps if item not in UpperBinderYarns]
UpperWarps=[item for item in UpperWarps if item not in LowerBinderYarns]
UpperWarps=[item for item in UpperWarps if item not in BinderYarnsBeforeBifurcation]


print("LowerWarps ", LowerWarps)
print("UpperWarps ", UpperWarps)


Weave3D = Textile.Get3DWeave()
Yarns=Textile.GetYarns()

WarpHeight = 0.223
WeftHeight = 0.333
Thickness=10*WeftHeight + 9*WarpHeight
MidTextile=Thickness/2

# get final binder yposition to set origin for lower yarns
Yarn=Textile.GetYarn(35)  #this is a warp yarn before bif
Node=Yarn.GetNode(1)
pos=Node.GetPosition()

# Lower


Origin=XYZ(0, pos.y, pos.z+4) ##check the z position of these so that they are symmetrical

for x in UpperWarps:
	Yarn=Yarns[x]
	TransformYarn( Yarn, Origin, True, True )

for x in UpperBinderYarns:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, True, False ) 

    Nodes=Yarn.GetMasterNodes()
    NumNodes=Yarn.GetNumNodes()

    Tol=0.01
    Weave3D.CheckUpVectors(94, True, True)
    # didn't work for some reason, check TG3 file
    if x<96:
        Weave3D.CheckUpVectors(x, True, True)

 
for x in UpperWefts:
	Yarn=Yarns[x]
	MaxWeftIndex=len(Yarn.GetMasterNodes()) - 1
	TransformYarnSection( Yarn, Origin, MaxWeftIndex, True )
	Yarn.AssignInterpolation( CInterpolationCubic( True, False, False) )
	Weave3D.CheckUpVectors(x, False, True )


# upper

Origin= XYZ(0, pos.y, pos.z-4)
for x in LowerWarps:
	Yarn=Yarns[x]
	TransformYarn( Yarn, Origin, False, True )
	Weave3D.CheckUpVectors(x, True, True )
	
	
for x in LowerBinderYarns:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, False, False ) 

    Nodes=Yarn.GetMasterNodes()
    NumNodes=Yarn.GetNumNodes()

    Tol=0.01
    Weave3D.CheckUpVectors(94, True, True)
    # didn't work for some reason, check TG3 file
    if x<96:
        Weave3D.CheckUpVectors(x, True, True)
	

for x in LowerWefts:
	Yarn=Yarns[x]
	MaxWeftIndex=len(Yarn.GetMasterNodes()) - 1
	TransformYarnSection( Yarn, Origin, MaxWeftIndex, False )
	#Yarn.SetResolution(10)
	Yarn.AssignInterpolation( CInterpolationCubic( True, False, False) )
	Weave3D.CheckUpVectors(x, False, True )


Textile.DeleteYarn(5)
Textile.DeleteYarn(14)
Textile.DeleteYarn(23)

Textile.DeleteYarn(21)
Textile.DeleteYarn(21)

#Textile.BuildTextile()


# Yarns=Textile.GetYarns()
# for index in range(len(Yarns)):
    # Yarns[index].SetYoungsModulusX(174.4, 'GPa')
    # Yarns[index].SetYoungsModulusY(8.9, 'GPa')
    # Yarns[index].SetYoungsModulusZ(8.9, 'GPa')
    # Yarns[index].SetShearModulusXY(4.2, 'GPa')
    # Yarns[index].SetShearModulusXZ(4.2, 'GPa')
    # Yarns[index].SetShearModulusYZ(3, 'GPa')
    # Yarns[index].SetPoissonsRatioX(0.3)
    # Yarns[index].SetPoissonsRatioY(0.3)
    # Yarns[index].SetPoissonsRatioZ(0.3)
    # Yarns[index].SetAlphaX(5.4)
    # Yarns[index].SetAlphaY(5.4)
    # Yarns[index].SetAlphaZ(5.4)



# # Matrix material properties
# Textile.SetMatrixYoungsModulus(3.5, 'GPa')
# Textile.SetMatrixPoissonsRatio(0.35)
# Textile.SetMatrixAlpha(52.7e-6)
# Textile.SetFibreDiameter(0.007, "mm")
# # weave3D.SetFibreDiameter(WEFT, 0.007, "mm")
# # weave3D.SetFibreDiameter(BINDER, 0.007, "mm")
# Textile.SetFibresPerYarn(5000)
# # weave3D.SetFibresPerYarn(WEFT, 8000)
# # weave3D.SetFibresPerYarn(BINDER, 3500)

Textile.Rotate(WXYZ(XYZ(0,0,1),math.radians(90)),XYZ(0,0,0))

points = XYVector()
# values are y and z
points.push_back(XY(-27,0))
points.push_back(XY(-19,0))
points.push_back(XY(-18.4,-0.1))
points.push_back(XY(-17.82,-0.38))
points.push_back(XY(-17.38,-0.82))
points.push_back(XY(-17.1,-1.4))
points.push_back(XY(-17,-2))
points.push_back(XY(-17,-5))
points.push_back(XY(-14,-5))
points.push_back(XY(-14,0))
points.push_back(XY(-14,10))
points.push_back(XY(-17,10))
points.push_back(XY(-17, 6.5))
points.push_back(XY(-17.1,5.9))
points.push_back(XY(-17.38,5.32))
points.push_back(XY(-17.82,4.88))
points.push_back(XY(-18.4,4.6))
points.push_back(XY(-19,4.5))
points.push_back(XY(-27,4.5))
domain = CDomainPrism(points, XYZ(0,0,0), XYZ(0,5,0))

domain.GeneratePlanes()

Textile.AssignDomain(domain)

AddTextile(Textile)

#


NumXVoxels=140
NumYVoxels=70
NumZVoxels=140
FileName=cwd + "\\T-Joint6_" + str(NumXVoxels)
PrismMesh=CPrismVoxelMesh("CPeriodicBoundaries")
# #(CTextile &Textile, string OutputFilename, int XVoxNum, int YVoxNum, int ZVoxNum,
	# #bool bOutputMatrix, bool bOutputYarns, int iBoundaryConditions, int iTJointConditions, int iElementType, int FileType)
#PrismMesh.SaveVoxelMesh(Textile, FileName, NumXVoxels, NumYVoxels, NumZVoxels, True, True, NO_BOUNDARY_CONDITIONS, 0, 0, 0)



# OctMesh = COctreeVoxelMesh("CPeriodicBoundaries")
# OctMesh.SaveVoxelMesh(Textile, FileName, NumXVoxels, NumYVoxels, NumZVoxels, 1, 5, False, 0, 0.0, 0.0, False, False)

from WriteInput import *
WriteToInputExplicit(FileName+".inp")