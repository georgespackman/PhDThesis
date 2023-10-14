#pragma once

#include "materials.h"

namespace TexGen
{

	using namespace std;

	class CTextile;
	class CVoxelMesh;
	class CPrismVoxelMesh;
	class COctreeVoxelMesh;

	///Class used to generate Abaqus output for T-Joint simulations
	class CLASS_DECLSPEC CTJointBoundaries
	{
	public:
		CTJointBoundaries();
		~CTJointBoundaries(void);
		void CreateTJointBoundaries(CPrismVoxelMesh* PrismMesh, ostream &Output, CTextile &Textile, bool bMatrixOnly);
		void CreateTJointBoundaries(COctreeVoxelMesh* OctMesh, ostream &Output, CTextile &Textile, bool bMatrixOnly);
		void SetWebNodes(vector<int> &WebNodes);
		void SetFlangeANodes(vector<int> &Flange_A_Nodes);
		void SetFlangeBNodes(vector<int> &Flange_B_Nodes);
		
	protected:
		void OutputTJointSets(ostream & Output, CPrismVoxelMesh* PrismMesh, CTextile & Textile);
		void OutputTJointSets(ostream & Output, COctreeVoxelMesh* OctMesh, CTextile & Textile);
		void OutputLoadCase(ostream & Output);
		vector<int> m_WebNodes, m_Flange_A_Nodes, m_Flange_B_Nodes;
	};
};	// namespace TexGen