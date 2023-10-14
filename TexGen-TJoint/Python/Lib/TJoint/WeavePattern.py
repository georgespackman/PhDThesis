# TexGen: Geometric textile modeller.
# Copyright (C) 2014 Louise Brown
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import sys
sys.path.append(os.getcwd())
from TexGen.Core import *
from math import *
from WeftInsertion import *

def SpacedStringToIntVector( Str ):
	Vector = IntVector()
	for s in Str.split():
		if s.isdigit():
			Vector.push_back(int(s))
	return Vector
	
def StringToIntVector( Str ):
	Vector = IntVector()
	for a in Str:
		if a.isdigit():
			Vector.push_back(int(a))
	return Vector
	
def StringToChunks( Str, Num ):
	# needs changing when intro binders, maybe add + 1 
	return [Str[pos:pos+Num+1] for pos in xrange(0, len(Str), Num)]
	
def ListToSummedChunks(List, Size):
	return [sum(List[pos:pos+Size]) for pos in xrange(0, len(List), Size)]
	
def merge(List1, List2): 
    return [[a,b] for (a, b) in zip(List1, List2)] 

	
def SetupBinders( Str ):
    # Sets up vector indicating which warp yarns are binders
	Vector = BoolVector()
	NumBinders = 0
	Str = Str.replace(' ','')
	for i in range( len( Str )-1 ):
		if Str[i] == '1' and ( Str[i+1] == '1' or Str[i+1] == '\n' ):
			Vector.insert( Vector.begin(), True )
			NumBinders += 1
		elif Str[i] == '1':
			#Vector.push_back( False )
			Vector.insert( Vector.begin(), False )
	#for s in Str.split('1'):
	#	if s == '' or s == '\n':
			#Vector.push_back( True )
	#		Vector.insert( Vector.begin(), True )
	#		NumBinders += 1
	#	else:
	#		#Vector.push_back( False )
	#		Vector.insert( Vector.begin(), False )
	return NumBinders, Vector
	
def SetupBinderPositions( NumBinders, NumWarps, Layers ):
	i=len(Layers)/NumBinders
	list=[]
	for i in xrange(NumWarps, len(Layers)+1, i):
		list.append(i)
	return list
	

def ImportWeavePattern( Filename ):
	file = open(Filename,'r')
	Pattern = CPatternDraft()

	firstLine = True
	WeftMatrix = []   # Vector of IntVectors for storing rows of weave pattern
	WeftDensity = 0.0
	Width = 0.0
	TowArea = 0.0
	LinearDensity = 0.0
	FibreDiameter = 0.0
	FibreDensity = 0.0
	FibreCount = 0
	TowWidth = 0.0
	TowHeight = 0.0
	BinderWidth = 0.0
	BinderHeight = 0.0
	tol = 1e-6
	WeftRepeat = False
	Orthogonal = False
	lineCount=0
	WeftStack=0
	BinderPositions=[]
	
	list0=[0, 1, 2, 3, 4, 9, 8, 7, 6, 5]
	list1=[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
	list2=[9, 8, 7, 6, 5, 0, 1, 2, 3, 4]
	list3=[5, 6, 7, 8, 9, 4, 3, 2, 1, 0]
	list7=[4, 3, 2, 1, 0, 9, 8, 7, 6, 5]
	list5=[5, 6, 7, 8, 9, 4, 3, 2, 1, 0]
	list6=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	EndPositionDict={}
	for i in range(len(list6)):
		EndPositionDict[i]=list6[i]
	
	#erase contents of file
	file1=open("patterndraft.txt", "w")
	file1.close()
	
	#start writing new pattern draft

	
	for line in file:
		# First line contains layer data
		if firstLine:
			firstLine = False
			Layers = SpacedStringToIntVector( line )
			NumWarps = line.count('1')  # Sum of number of binders and warp stacks
			
			NumBinders, Binders = SetupBinders( line )
			file1=open("patterndraft.txt", "a")
			file1.write(line + "\n")
			file1.close()
			
			NumWarpLayers = int(max(line))  # Number of warp layers set to size of largest warp stack
		else:  # Read in row matrix
			parts = line.split()
			if not parts:  # empty line
				continue
			
			if parts[0] == 'FIBRE_COUNT':
				FibreCount = int(parts[1])
			elif parts[0] == 'LINEAR_DENSITY':  
				LinearDensity = float(parts[1])
				LinearDensityUnits = parts[2]
			elif parts[0] == 'FIBRE_DIAMETER':
				FibreDiameter = float(parts[1])
				FibreDiameterUnits = parts[2]
			elif parts[0] == 'FIBRE_DENSITY':
				FibreDensity = float(parts[1])
				FibreDensityUnits = parts[2]
			elif parts[0] == 'WIDTH':
				Width = float(parts[1])
				WidthUnits = parts[2]
			elif parts[0] == 'WEFT_DENSITY':
				WeftDensity = float(parts[1])
				WeftDensityUnits = parts[2]
			elif parts[0] == 'TOW_AREA':
				TowArea = float(parts[1])
				TowAreaUnits = parts[2]
			elif parts[0] == 'WEFT_REPEAT':
				WeftRepeat = True
			elif parts[0] == 'ORTHOGONAL':
				Orthogonal = True
			elif parts[0] == 'TOW_WIDTH':
				TowWidth = float(parts[1])
				TowWidthUnits = parts[2]
			elif parts[0] == 'TOW_HEIGHT':
				TowHeight = float(parts[1])
				TowHeightUnits = parts[2]
			elif parts[0] == 'BINDER_WIDTH':
				BinderWidth = float(parts[1])
				BinderWidthUnits = parts[2]
			elif parts[0] == 'BINDER_HEIGHT':
				BinderHeight = float(parts[1])
				BinderHeightUnits = parts[2]
			else:
				allNumeric = True
				for part in parts:
					if not part.isdigit():
						allNumeric = False
						print 'Error in weave pattern line, not all numeric'
						break
				
				if allNumeric == True:	
					
					# Use WeftInsertion function to write each weft to weave pattern
					LineVector = StringToIntVector( line )

					#BinderPositions.append(SetupBinderPositions(NumBinders, LineVector))
					NumXYarns=7
					BifStack=4
					NumWefts=10
					

					line = WeftInsertion(EndPositionDict, lineCount, BifStack, WeftStack, NumXYarns, NumWefts)
					Pattern.AddRow( line )
					
					WeftMatrix.append(LineVector)
					lineCount = lineCount + 1
					if lineCount==10:
						lineCount=0
						WeftStack=WeftStack+1

	file.close()

	NumWefts = len(WeftMatrix)
	
	# Check that number of items in layer info matches the number of warps
	if (len(Layers) != len( WeftMatrix[0])):

		return ''
	
	if ( (fabs(Width) < tol) or (fabs(WeftDensity) < tol) or ((fabs(TowArea) < tol) and ((fabs(TowWidth) < tol) or (fabs(TowHeight) < tol))) ):
		print 'Width, weft density or tow area missing in input file.  Using default values'
		WarpSpacing = 1.0
		WeftSpacing = 1.0
		TowWidth = 0.8
		TowHeight = 0.2
	else:
		WarpSpacing = ConvertUnits( Width, WidthUnits, 'mm' )/NumWarps
		
	
		WeftSpacing = 1/ConvertUnits( WeftDensity, WeftDensityUnits, '/mm' )
		
		
		if ( (fabs(TowWidth) > tol) and (fabs(TowHeight) > tol) ):
			TowWidth = ConvertUnits( TowWidth, TowWidthUnits, 'mm')
			TowHeight = ConvertUnits( TowHeight, TowHeightUnits, 'mm')
		else:
			TowArea = ConvertUnits( TowArea, TowAreaUnits, 'mm^2')
			# Work on 6:1 ratio for width to height of yarn in weave
			TowHeight = 2.0 * sqrt( TowArea / ( 6 * pi ) )
			TowWidth = 6 * TowHeight
			
		if ( (fabs(BinderWidth) > tol) and (fabs(BinderHeight) > tol) ):
			print 'Convert binder'
			BinderWidth = ConvertUnits( BinderWidth, BinderWidthUnits, 'mm')
			BinderHeight = ConvertUnits( BinderHeight, BinderHeightUnits, 'mm')
			
	# Create textile
	if Orthogonal:
		Textile = CTextileOrthogonal(NumWarps, NumWefts, WarpSpacing, WeftSpacing, TowHeight, TowHeight, False, True )
	else:
		Textile = CTextile3DWeave( NumWarps,NumWefts, WarpSpacing, WeftSpacing, TowHeight, TowHeight )
	if Textile == 0:
		return ''
		
	
	if Orthogonal:
		Textile.SetBinderPattern( Binders )
		NumLayers = (NumWarpLayers * 2) + 3 # Num weft layers = num warp layers + 1, then layer at top and bottom for binders  
		#need to setbinderposition
		
		
		
	else:
		Textile.SetWarpRatio( NumWarps )
		Textile.SetBinderRatio( 1 )
		# Need to find max no of layers
		NumLayers = NumWarpLayers + 1  # Just have warps and one binder in stack
		
    # Set up cells for storing yarn configuration, all initialised to PATTERN3D_NOYARN
	for i in range(NumLayers):  
		Textile.AddNoYarnLayer()
		
	Textile.SetXYarnWidths( TowWidth )
	Textile.SetYYarnWidths( TowWidth )
	
	if ( (fabs(BinderWidth) > tol) and (fabs(BinderHeight) > tol) ):
		print 'Setting binder widths'
		Textile.SetBinderYarnWidths( BinderWidth )
		Textile.SetBinderYarnHeights( BinderHeight )
		Textile.SetBinderYarnPower( 0.2 )
	else:
		Textile.SetBinderYarnPower(1.0)
		
	Textile.SetWarpYarnPower(1.0)
	Textile.SetWeftYarnPower(1.0)
	
    # Set whether or not textile will repeat in weft direction
	Textile.SetWeftRepeat( WeftRepeat )

	# Set up weave pattern in textile
	if Orthogonal:
		isBinder=SetupBinderPositions(NumBinders, max(Layers), Layers)
		BinderPositions=[]
		first=True
		for i in range(NumWefts-1, -1, -1):
			Binder=0
			for j in range(0, len(Layers)):
				if j in isBinder:
					
					if first:
						BinderPositions.append([])
					
					BinderPositions[Binder].append(WeftMatrix[i][j])

					Binder+=1
			first=False

		
		BinderPattern=[]
		for i in range(0, len(BinderPositions)):
			chunkedList=ListToSummedChunks(BinderPositions[i], max(Layers)+1)
			#multiply by 2 to fit in cells for warps
			newList=[i*2 for i in chunkedList]
			BinderPattern.append(newList)
		
		
		listoflists=[]
			

			
		for i in range(0, len(BinderPattern[0])):
			Vector=IntVector()
			for j in range(0, len(BinderPattern)):
				Vector.push_back(BinderPattern[j][i])	
			listoflists.append(Vector)
		

		
		j=0
		counter=0
		for i in range(NumWefts-1,-1,-1):
			Textile.SetupWeftRow( Layers, WeftMatrix[i], listoflists[counter], NumWarps, NumWefts-1-i )
			j=j+1
			if j>max(Layers):
				counter=counter+1
				j=0
				
		#if orthogonal move wefts into stacks where possible
		Textile.ConsolidateCells()
		
	else:
		Textile.SetupWeftRow( Layers, WeftMatrix[i], NumWarps, NumWefts-1-i)
	
	
	if fabs(LinearDensity) > tol:
		Textile.SetYarnLinearDensity( WARP, LinearDensity, LinearDensityUnits )
		Textile.SetYarnLinearDensity( WEFT, LinearDensity, LinearDensityUnits )
	if fabs(FibreDiameter) > tol:
		Textile.SetFibreDiameter( WARP, FibreDiameter, FibreDiameterUnits )
		Textile.SetFibreDiameter( WEFT, FibreDiameter, FibreDiameterUnits )
	if fabs(FibreDensity) > tol:
		Textile.SetFibreDensity( WARP, FibreDensity, FibreDensityUnits )
		Textile.SetFibreDensity( WEFT, FibreDensity, FibreDensityUnits )
	if FibreCount != 0:
		Textile.SetFibresPerYarn( WARP, FibreCount )
		Textile.SetFibresPerYarn( WEFT, FibreCount )
	
	
	Textile.SetResolution(40)
	print("Adding Textile")
	TextileName = AddTextile(Textile)
	return TextileName
	
def GetPatternInfo( FileName ):
	#Function to return the order of lateral displacement of weft yarns based on the finishing position after the bifurcation
	
	file=open(FileName, "r")
	FirstLine=True
	SecondLine=True
	YarnIndex=0
	PositionDict={}
	for line in file:
		if FirstLine==True:
			FirstLine=False
			Vector=SpacedStringToIntVector(line)
			NumXYarns=line.count('1')
			NumWarps=max(Vector) #better than using count() because don't want to count binders
			NumWefts=max(Vector)+1
		else:
			EndPosition=line[-NumWarps-2:-2].count('1')
			print("EndPosition ", EndPosition)
			
			PositionDict[YarnIndex]=EndPosition
			YarnIndex=YarnIndex+1
			Stacks=StringToChunks(line, NumXYarns)
			BifStack=Stacks.count(Stacks[0])
			if YarnIndex > NumWefts-1: #The two weft stacks have the same pattern only need to read once
				break
	file.close()

	NewDict={}
	FirstYarn=True
	
	
	for i in PositionDict:
		LatDisplacement=0
		#check end position of previous yarns
		for j in range(0, i+1):
			if PositionDict[i] < PositionDict[i-j]:
				LatDisplacement=LatDisplacement+1
				
		NewDict[i]=LatDisplacement
		
		
	return NewDict, PositionDict, NumWarps, NumWefts, NumXYarns, BifStack


def AddMidSectionNodes(i, k, BifStack, NewDict):

	tol=0.223
	Tex=GetTextile()
	Weave3D=Tex.Get3DWeave()
	Yarns=Tex.GetYarns()
	#Adds and moves mid section nodes to the correct position
	MovedNodeIndex=IntVector()
	yarnsection = CYarnSectionInterpNode( bool(1), bool(0), bool(1))
	# check if next node at same z position
	Nodes=Yarns[i].GetMasterNodes()
	j=0
	for j in range(len(Nodes)):
		NextNodeIndex=j+1
		CurrentNodePosition=Nodes[j].GetPosition()
		CurrentNodeHeight=CurrentNodePosition.z
		UpVector=Nodes[j].GetUp()
		if j+1 < len(Nodes):
			NextNodePosition=Nodes[j+1].GetPosition()
			NextNodeHeight=NextNodePosition.z
			if NextNodeHeight <= CurrentNodeHeight - tol: #down
				NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + (NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z - (CurrentNodePosition.z - NextNodePosition.z)/4))
				NewNode2=CNode(XYZ(CurrentNodePosition.x, (CurrentNodePosition.y + NextNodePosition.y)/2, (CurrentNodePosition.z + NextNodePosition.z)/2))
				NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 3*(NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z - 3*(CurrentNodePosition.z - NextNodePosition.z)/4))
				NewNode1.SetUp( UpVector )
				NewNode2.SetUp( UpVector )
				NewNode3.SetUp( UpVector )
				Yarns[i].InsertNode(NewNode1, j+1)
				Yarns[i].InsertNode(NewNode2, j+2)
				Yarns[i].InsertNode(NewNode3, j+3)
				NextNodeIndex=j+2
				MovedNodeIndex.push_back(j+1)
				MovedNodeIndex.push_back(j+2)
				MovedNodeIndex.push_back(j+3)
				break
			elif NextNodeHeight >= CurrentNodeHeight + tol: #up
				NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + (NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z + (-CurrentNodePosition.z + NextNodePosition.z)/4))
				NewNode2=CNode(XYZ(CurrentNodePosition.x, (CurrentNodePosition.y + NextNodePosition.y)/2, (CurrentNodePosition.z + NextNodePosition.z)/2))
				NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 3*(NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z + 3*(-CurrentNodePosition.z + NextNodePosition.z)/4))
				NewNode1.SetUp( UpVector )
				NewNode2.SetUp( UpVector )
				NewNode3.SetUp( UpVector )
				Yarns[i].InsertNode(NewNode1, j+1)
				Yarns[i].InsertNode(NewNode2, j+2)
				Yarns[i].InsertNode(NewNode3, j+3)
				NextNodeIndex=j+2
				MovedNodeIndex.push_back(j+1)
				MovedNodeIndex.push_back(j+2)
				MovedNodeIndex.push_back(j+3)
				break
			elif j==BifStack+6 and NextNodeHeight==CurrentNodeHeight: #flat
				print("We got here")
				NewNode1=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + (NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z))
				NewNode2=CNode(XYZ(CurrentNodePosition.x, (CurrentNodePosition.y + NextNodePosition.y)/2, CurrentNodePosition.z))
				NewNode3=CNode(XYZ(CurrentNodePosition.x, CurrentNodePosition.y + 3*(NextNodePosition.y-CurrentNodePosition.y)/4, CurrentNodePosition.z))
				NewNode1.SetUp( UpVector )
				NewNode2.SetUp( UpVector )
				NewNode3.SetUp( UpVector )
				Yarns[i].InsertNode(NewNode1, j+1)
				Yarns[i].InsertNode(NewNode2, j+2)
				Yarns[i].InsertNode(NewNode3, j+3)
				NextNodeIndex=j+2
				MovedNodeIndex.push_back(j+1)
				MovedNodeIndex.push_back(j+2)
				MovedNodeIndex.push_back(j+3)
				break
	Nodes=Yarns[i].GetMasterNodes()
	for l in range(len(Nodes)):
		Weave3D.CheckUpVectors(i)
		if l==j+1 or l==j+2 or l==j+3:
			section = CSectionPowerEllipse(0.333, 0.333, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)
		elif l==j or l==j-1 or l==j-2 or l==j-3 or l==j+4 or l==j+5 or l==j+6 or l==j+7:
			section = CSectionPowerEllipse(0.65, 0.31, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)
		else:
			section = CSectionPowerEllipse(2*0.446, 0.223, 1, 0)
			#section = CSectionPowerEllipse(0.45, 0.45, 1, 0)
			yarnsection.AddSection(section)
		
	Yarns[i].AssignSection(yarnsection)
	# # reorder the yarnindex based on position in 
	
	
	
	#AddTextile(Tex)
	# def MoveNodes(MovedNodeIndex, k):
	Diameter = 2*0.54
	Radius=0.54
	Nodes = Yarns[i].GetMasterNodes()
	print(len(Nodes))
	# move the nodes into the correct position based off the pattern draft information - needs parameterisation	
	NodeBefore2 = Nodes[MovedNodeIndex[0]-2]
	NodeBefore1 = Nodes[MovedNodeIndex[0]-1]
	Node1  = Nodes[MovedNodeIndex[0]]
	Node2  = Nodes[MovedNodeIndex[1]]
	Node3  = Nodes[MovedNodeIndex[2]]
	NodeAfter1 = Nodes[MovedNodeIndex[2]+1]
	NodeAfter2 = Nodes[MovedNodeIndex[2]+2]
	NodeBefore2Position = NodeBefore2.GetPosition()
	NodeBefore1Position = NodeBefore1.GetPosition()
	Node1Position  = Node1.GetPosition()
	Node2Position  = Node2.GetPosition()
	Node3Position  = Node3.GetPosition()
	NodeAfter1Position = NodeAfter1.GetPosition()
	NodeAfter2Position = NodeAfter2.GetPosition()
	Diameter = 0.54
	#Radius=0.54*0.5 #yarn 63 needs to wrap around 64 otherwise they will just intersect upon applying the bifurcation
	Radius = 0.4
	xDisplacement = Diameter*NewDict[k]
	scale = 0.25*max(NewDict.values())*0.54
	x = NewDict.values()[k]
		# instead of getting a new node, just update the nodal co-ordinates
	print(xDisplacement)

	if x % 2 == 0:
		if x>0: #x is always greater than 0...
			if x > 2 and x < 7:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2+0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2+0.14, Node3Position.z))
			
			else:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.5*xDisplacement + Radius -1, Node1Position.y + 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.5*xDisplacement + Radius -1, Node1Position.y + 0.2+0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.5*xDisplacement + Radius -1, Node1Position.y + 0.2+0.14, Node3Position.z))
			NewNode1.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode2.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode3.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			print("Node Moved")
		else:
			if x > 2 and x < 7:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2+0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.8*xDisplacement + Radius -1, Node1Position.y + 0.2+0.14, Node3Position.z))
			else:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.5*xDisplacement + Radius-1, Node1Position.y + 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.5*xDisplacement + Radius-1, Node1Position.y + 0.2+0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.5*xDisplacement + Radius-1, Node1Position.y + 0.2+0.14, Node3Position.z))
			
			NewNode1.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode2.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode3.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			print("Node Moved")
	else:
		if x>0:
			if x > 2 and x < 7:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2 + 0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2 + 0.14, Node3Position.z))
			else:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.5*xDisplacement-1, Node1Position.y - 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.5*xDisplacement-1, Node1Position.y - 0.2 + 0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.5*xDisplacement-1, Node1Position.y - 0.2 + 0.14, Node3Position.z))
			NewNode1.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode2.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode3.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			print("Node Moved")
		else:
			if x > 2 and x < 7:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2 + 0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.8*xDisplacement-1, Node1Position.y - 0.2 + 0.14, Node3Position.z))
			else:
				NewNode1 = CNode(XYZ(Node1Position.x + 0.5*xDisplacement -1, Node1Position.y - 0.2, Node1Position.z))
				NewNode2 = CNode(XYZ(Node2Position.x + 0.5*xDisplacement -1, Node1Position.y - 0.2 + 0.07, Node2Position.z))
				NewNode3 = CNode(XYZ(Node3Position.x + 0.5*xDisplacement -1, Node1Position.y - 0.2 + 0.14, Node3Position.z))
			
			NewNode1.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode2.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			NewNode3.SetUp(XYZ(1.000000000000e+00, 2.220446049250e-16, 0.000000000000e+00))
			print("Node Moved")
	NewNode1Position=NewNode1.GetPosition()
	NewNode2Position=NewNode2.GetPosition()
	NewNode3Position=NewNode3.GetPosition()
	Nodes=Yarns[i].GetMasterNodes()
	Yarns[i].ReplaceNode(MovedNodeIndex[0], NewNode1)
	Yarns[i].ReplaceNode(MovedNodeIndex[1], NewNode2)
	Yarns[i].ReplaceNode(MovedNodeIndex[2], NewNode3)
		
	return