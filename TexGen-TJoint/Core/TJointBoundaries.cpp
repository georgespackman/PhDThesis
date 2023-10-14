#include "PrecompiledHeaders.h"
#include "TJointBoundaries.h"
#include "TexGen.h"

using namespace TexGen;
using namespace std;

CTJointBoundaries::CTJointBoundaries()
{
}

CTJointBoundaries::~CTJointBoundaries(void)
{
}

void CTJointBoundaries::CreateTJointBoundaries(CPrismVoxelMesh* PrismMesh, ostream& Output, CTextile & Textile, bool bMatrixOnly)
{
	Output << "**TJoint Sets**" << endl;
	OutputTJointSets(Output, PrismMesh, Textile);
	return;
}


void CTJointBoundaries::CreateTJointBoundaries(COctreeVoxelMesh* OctMesh, ostream& Output, CTextile& Textile, bool bMatrixOnly)
{
	Output << "**TJoint Sets**" << endl;
	OutputTJointSets(Output, OctMesh, Textile);
	return;
}


void CTJointBoundaries::OutputTJointSets(ostream& Output, CPrismVoxelMesh* PrismMesh,  CTextile& Textile)
{
	/*//Get Domain points
	CDomainPrism* Domain = Textile.GetDomain()->GetPrismDomain();
	vector<XY> PrismPoints = Domain->GetPoints();

	vector<double> Points;
	//Separate the XY into an X and Y (transpose onto y and z co-ods for T)
	for (auto i = begin(PrismPoints); i != PrismPoints.end(); i++)
	{
		Points.push_back(i->x);
	}
	auto Min_yPoint = *min_element(Points.begin(), Points.end());
	int  Min_yPoint_Pos = distance(Points.begin(), min_element(Points.begin(), Points.end()));

	//Nodes = Textile.Ge
	*/

	int NumNodes = PrismMesh->GetNumberofNodes();
	for (int i = 0; i < 3; ++i)
	{
		Output << "*NSet, Nset = ConstraintsDriver" << i << ", instance=PART-1-1" << endl;
		Output << NumNodes + (i + 1) << endl;
	}


	vector<int> WebNodes = PrismMesh->GetWebNodes();
	vector<int> FlangeANodes = PrismMesh->GetFlangeANodes();
	vector<int> FlangeBNodes = PrismMesh->GetFlangeBNodes();

	//Need to find nodes closest to this y value
	Output << "*NSet, NSet = WebNodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, WebNodes, 16);

	Output << "*NSet, NSet = FlangeANodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, FlangeANodes, 16);

	Output << "*NSet, NSet = FlangeBNodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, FlangeBNodes, 16);
	//WriteValues(Output, m_, 16)

	return;
}

void CTJointBoundaries::OutputTJointSets(ostream& Output, COctreeVoxelMesh* OctMesh, CTextile& Textile)
{
	//Get Domain points
	/*CDomainPrism* Domain = Textile.GetDomain()->GetPrismDomain();
	vector<XY> PrismPoints = Domain->GetPoints();

	vector<double> Points;
	//Separate the XY into an X and Y (transpose onto y and z co-ods for T)
	for (auto i = begin(PrismPoints); i != PrismPoints.end(); i++)
	{
		Points.push_back(i->x);
	}
	auto Min_yPoint = *min_element(Points.begin(), Points.end());
	int  Min_yPoint_Pos = distance(Points.begin(), min_element(Points.begin(), Points.end()));

	//Nodes = Textile.Ge
	

	//CDomainPrism* Domain = Textile.GetDomain()->GetPrismDomain();
	//CMesh Mesh = Domain->GetMesh().GetAABB();

	//Need to find nodes closest to this y value
	//Need to find nodes closest to this y value
	*/

	int NumNodes = OctMesh->getNumNodes();
	for (int i = 0; i < 3; ++i)
	{
		Output << "*NSet, Nset = ConstraintsDriver" << i << ", instance=PART-1-1" << endl;
		Output << NumNodes + (i + 1) << endl;
	}


	Output << "*NSet, NSet = WebNodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, m_WebNodes, 16);

	Output << "*NSet, NSet = FlangeANodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, m_Flange_A_Nodes, 16);

	Output << "*NSet, NSet = FlangeBNodes";
	Output << ", Unsorted" << endl;
	WriteValues(Output, m_Flange_B_Nodes, 16);

	return;
}

void CTJointBoundaries::OutputLoadCase(ostream& Output)
{
	return;
}

void TexGen::CTJointBoundaries::SetWebNodes(vector<int> &WebNodes)
{
	m_WebNodes = WebNodes;
	return;
}

void TexGen::CTJointBoundaries::SetFlangeANodes(vector<int> &Flange_A_Nodes)
{
	m_Flange_A_Nodes = Flange_A_Nodes;
	return;
}

void TexGen::CTJointBoundaries::SetFlangeBNodes(vector<int> &Flange_B_Nodes)
{
	m_Flange_B_Nodes = Flange_B_Nodes;
	return;
}
