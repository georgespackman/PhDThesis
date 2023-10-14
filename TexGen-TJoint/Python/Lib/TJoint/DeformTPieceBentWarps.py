# import math
# from TexGen.Core import *

# def BendWarpSection( Section, Radius ):
	# info = YARN_POSITION_INFORMATION()
	# SectionPoints = Section.GetSection(info, 40)
	# PolygonPoints = XYVector()
	
	# for point in SectionPoints:
		# dx = Radius * math.sin(point.x/Radius) - point.x
		# dy = Radius * (1.0 - math.cos(point.x/Radius))
		# point.x += dx
		# point.y += dy
		# PolygonPoints.push_back( point )

	# PolygonSection = CSectionPolygon( PolygonPoints )
	# return PolygonSection


# def TransformPoint( Point, Origin ):
		
	# OffsetPoint = Point - Origin
	# OffsetPoint.y=OffsetPoint.y
	# Angle = 0.0
	# dy = 0.0
	# dz = 0.0
	# pi = math.pi
	# HalfPi = pi / 2.0
	# IsFillet = False
	
	# if (OffsetPoint.y > 0.0) and (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		# Angle=0
		# dy=0
		# dz=0

	# elif (OffsetPoint.y <= 0.0) and (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		# Angle = OffsetPoint.y / OffsetPoint.z
		# dy = (OffsetPoint.z * math.sin(-math.fabs(Angle)) - OffsetPoint.y)
		# dz = OffsetPoint.z * math.cos(-math.fabs(Angle)) - OffsetPoint.z
		# IsFillet = True


	# elif (OffsetPoint.y <= 0.0) and (math.fabs(OffsetPoint.y) > math.fabs(HalfPi*OffsetPoint.z)):
		# Angle = -HalfPi
		# dy = (-OffsetPoint.z - OffsetPoint.y)
		# dz = (( HalfPi * math.fabs(OffsetPoint.z) - math.fabs(OffsetPoint.y) ) - math.fabs(OffsetPoint.z))

	
	# OffsetPoint.y = (OffsetPoint.y + dy + Origin.y)
	# OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	

	# return OffsetPoint, Angle, IsFillet

	
# def TransformPointUp( Point, Origin ):
		
	# OffsetPoint = -Origin + Point
	# OffsetPoint.y = OffsetPoint.y
	
	
	# Angle = 0.0
	# dy = 0.0
	# dz = 0.0
	# pi = math.pi
	# HalfPi = pi / 2.0
	# IsFillet = False
	
	# if (OffsetPoint.y > 0.0) & (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		# Angle=0
		# dy=0
		# dz=0
	
	
	# elif (OffsetPoint.y <= 0.0) & (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		# Angle = OffsetPoint.y / OffsetPoint.z
		# dy = OffsetPoint.z * math.sin(Angle) - OffsetPoint.y
		# dz = OffsetPoint.z * math.cos(Angle) - OffsetPoint.z
		# IsFillet = True
	
	
	# elif (OffsetPoint.y <= 0.0) & (math.fabs(OffsetPoint.y) > math.fabs(HalfPi*OffsetPoint.z)):
		# Angle = HalfPi
		# dy = OffsetPoint.z - OffsetPoint.y
		# dz = (( HalfPi * OffsetPoint.z - OffsetPoint.y ) - OffsetPoint.z)


	
	# OffsetPoint.x = OffsetPoint.x
	# OffsetPoint.y = OffsetPoint.y + dy + Origin.y
	# OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	

	# return OffsetPoint, -Angle, IsFillet

# def TransformYarn( Yarn, Origin, Up, IsWarp ):
	
	# YarnSection = Yarn.GetYarnSection()
	# SectionConstant = YarnSection.GetSectionConstant()
	# Section = SectionConstant.GetSection()
	
	# Nodes = Yarn.GetMasterNodes()
	# i = 0
	# for Node in Nodes:
		# Point = Node.GetPosition()
		# if i == 0:
			# Radius = math.fabs(Point.z - Origin.z)
			# #print('Radius = ', Radius)
		# if Up == True:
			# Point,Angle,IsFillet = TransformPointUp( Point, Origin )
			# Angle=-Angle
			
			
		# else:
			# Point,Angle,IsFillet = TransformPoint( Point, Origin )
			
		
		# if i == 0:
			# if IsWarp & IsFillet:
				# #print 'Bending warp yarn'
				# if Up == True:
					# Section = BendWarpSection( SectionConstant, Radius )
					# #print(Section, Angle)
					
				# else:
					# Section = BendWarpSection( SectionConstant, -Radius )
                    # #print(Section, Angle)
                # RotatedSection = CSectionRotated( Section, Angle )
		# Node.SetPosition( Point )
		# Yarn.ReplaceNode( i, Node )		
		# i += 1
	# NewSection = CYarnSectionConstant( Section )
	# Yarn.AssignSection( NewSection )

	



# def TransformYarnSection( Yarn, Origin, MaxIndex, Up ):
	# Nodes = Yarn.GetMasterNodes()
	# i = 0
	# for i in range(0, MaxIndex+1):
		# Point = Nodes[i].GetPosition()
		# if Up == True:
			# Point,Angle,IsFillet = TransformPointUp( Point, Origin ) #put minus sign in for angle
			# Angle=-Angle
					
		# else:
			# Point,Angle,IsFillet = TransformPoint( Point, Origin )
		
		# # George - set the yarn tangents if Bezier interpolation
		# PrevPoint = Nodes[i-1].GetPosition()
		# OldTangent=Nodes[i].GetTangent()
		# NewY=OldTangent.y*math.cos(Angle)
		# NewZ=OldTangent.z*math.sin(Angle)
		# Tangent=XYZ(OldTangent.x, NewY, NewZ)
		# Nodes[i].SetTangent( Tangent)
		# Nodes[i].SetPosition( Point )
		# #Nodes[i].Rotate(WXYZ(XYZ(1,0,0), Angle), Origin)
		# Nodes[i].SetUp(XYZ(1,0,0))
		# Yarn.ReplaceNode( i, Nodes[i] )
		# i += 1
		

	
import math
from TexGen.Core import *

def BendWarpSection( Section, Radius ):
	info = YARN_POSITION_INFORMATION()
	SectionPoints = Section.GetSection(info, 40)
	PolygonPoints = XYVector()
	
	for point in SectionPoints:
		dx = Radius * math.sin(point.x/Radius) - point.x
		dy = Radius * (1.0 - math.cos(point.x/Radius))
		point.x += dx
		point.y += dy
		PolygonPoints.push_back( point )

	PolygonSection = CSectionPolygon( PolygonPoints )
	return PolygonSection


def TransformPoint( Point, Origin ):
		
	OffsetPoint = Point - Origin
	OffsetPoint.y=OffsetPoint.y
	Angle = 0.0
	dy = 0.0
	dz = 0.0
	pi = math.pi
	HalfPi = pi / 2.0
	IsFillet = False
	
	if (OffsetPoint.y > 0.0) and (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		Angle=0
		dy=0
		dz=0

	elif (OffsetPoint.y <= 0.0) and (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		Angle = OffsetPoint.y / OffsetPoint.z
		dy = (OffsetPoint.z * math.sin(-math.fabs(Angle)) - OffsetPoint.y)
		dz = OffsetPoint.z * math.cos(-math.fabs(Angle)) - OffsetPoint.z
		IsFillet = True


	elif (OffsetPoint.y <= 0.0) and (math.fabs(OffsetPoint.y) > math.fabs(HalfPi*OffsetPoint.z)):
		Angle = -HalfPi
		dy = (-OffsetPoint.z - OffsetPoint.y)
		dz = (( HalfPi * math.fabs(OffsetPoint.z) - math.fabs(OffsetPoint.y) ) - math.fabs(OffsetPoint.z))

	
	OffsetPoint.y = (OffsetPoint.y + dy + Origin.y)
	OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	

	return OffsetPoint, Angle, IsFillet

	
def TransformPointUp( Point, Origin ):
		
	OffsetPoint = -Origin + Point
	OffsetPoint.y = OffsetPoint.y
	
	
	Angle = 0.0
	dy = 0.0
	dz = 0.0
	pi = math.pi
	HalfPi = pi / 2.0
	IsFillet = False
	
	if (OffsetPoint.y > 0.0) & (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		Angle=0
		dy=0
		dz=0
	
	
	elif (OffsetPoint.y <= 0.0) & (math.fabs(OffsetPoint.y) <= math.fabs(HalfPi*OffsetPoint.z)):
		Angle = OffsetPoint.y / OffsetPoint.z
		dy = OffsetPoint.z * math.sin(Angle) - OffsetPoint.y
		dz = OffsetPoint.z * math.cos(Angle) - OffsetPoint.z
		IsFillet = True
	
	
	elif (OffsetPoint.y <= 0.0) & (math.fabs(OffsetPoint.y) > math.fabs(HalfPi*OffsetPoint.z)):
		Angle = HalfPi
		dy = OffsetPoint.z - OffsetPoint.y
		dz = (( HalfPi * OffsetPoint.z - OffsetPoint.y ) - OffsetPoint.z)


	
	OffsetPoint.x = OffsetPoint.x
	OffsetPoint.y = OffsetPoint.y + dy + Origin.y
	OffsetPoint.z = OffsetPoint.z + dz + Origin.z
	

	return OffsetPoint, -Angle, IsFillet

def TransformYarn( Yarn, Origin, Up, IsWarp ):
	
	YarnSection = Yarn.GetYarnSection()
	SectionConstant = YarnSection.GetSectionConstant()
	Section = SectionConstant.GetSection()
	
	Nodes = Yarn.GetMasterNodes()
	i = 0
	for Node in Nodes:
		Point = Node.GetPosition()
		if i == 0:
			Radius = math.fabs(Point.z - Origin.z)
			#print('Radius = ', Radius)
		if Up == True:
			Point,Angle,IsFillet = TransformPointUp( Point, Origin )
			Angle=-Angle
			
			
		else:
			Point,Angle,IsFillet = TransformPoint( Point, Origin )
			
		
		if i == 0:
			if IsWarp & IsFillet:
				#print 'Bending warp yarn'
				if Up == True:
					Section = BendWarpSection( SectionConstant, Radius )
					#print(Section, Angle)
					
				else:
					Section = BendWarpSection( SectionConstant, -Radius )
                                        #print(Section, Angle)
                RotatedSection = CSectionRotated( Section, Angle )
		Node.SetPosition( Point )
		Yarn.ReplaceNode( i, Node )
		i += 1
	NewSection = CYarnSectionConstant( RotatedSection )
	Yarn.AssignSection( NewSection )

	



def TransformYarnSection( Yarn, Origin, MaxIndex, Up ):
	Nodes = Yarn.GetMasterNodes()
	i = 0
	for i in range(0, MaxIndex+1):
		Point = Nodes[i].GetPosition()
		if Up == True:
			Point,Angle,IsFillet = TransformPointUp( Point, Origin ) #put minus sign in for angle
			Angle=-Angle
					
		else:
			Point,Angle,IsFillet = TransformPoint( Point, Origin )
		
		#George - set the yarn tangents if Bezier interpolation
		PrevPoint = Nodes[i-1].GetPosition()
		OldTangent=Nodes[i].GetTangent()
		NewY=OldTangent.y*math.cos(Angle)
		NewZ=OldTangent.z*math.sin(Angle)
		Tangent=XYZ(OldTangent.x, NewY, NewZ)
		Nodes[i].SetTangent( Tangent)
		Nodes[i].SetPosition( Point )
		Nodes[i].SetUp(XYZ(1,0,0))
		Yarn.ReplaceNode( i, Nodes[i] )
		i += 1
