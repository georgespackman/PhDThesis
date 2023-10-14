/*=============================================================================
TexGen: Geometric textile modeller.
Copyright (C) 2021 George Spackman

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
=============================================================================*/

#include <cmath>
#include "PrecompiledHeaders.h"
#include "InterpolationQuadratic.h"
#include "Matrix.h"
using namespace TexGen;

CInterpolationQuadratic::CInterpolationQuadratic(bool bPeriodic, bool bForceInPlaneTangent, bool bForceMasterNodeTangent)
: CInterpolation(bPeriodic, bForceInPlaneTangent, bForceMasterNodeTangent)
{
}

CInterpolationQuadratic::~CInterpolationQuadratic(void)
{
}

CInterpolationQuadratic::CInterpolationQuadratic(TiXmlElement &Element)
: CInterpolation(Element)
{
	// TODO: IMPLEMENT ME
}

/*
void CInterpolationQuadratic::PopulateTiXmlElement(TiXmlElement &Element, OUTPUT_TYPE OutputType) const
{
}*/

CSlaveNode CInterpolationQuadratic::GetNode(const vector<CNode> &MasterNodes, int iIndex, double t) const
{
	assert(iIndex >= 0 && iIndex < int(MasterNodes.size() - 1));
	// Errors may occur here if the Initialise function was not called before
	// calling this function. For performance reasons it is necessary to call
	// initialise once at the start before making calls to this function
	assert(m_XQuadratics.size() == MasterNodes.size() - 1);
	assert(m_YQuadratics.size() == MasterNodes.size() - 1);
	assert(m_ZQuadratics.size() == MasterNodes.size() - 1);

	XYZ Pos, Tangent;

	Pos.x = m_XQuadratics[iIndex].Evaluate(t);
	Pos.y = m_YQuadratics[iIndex].Evaluate(t);
	Pos.z = m_ZQuadratics[iIndex].Evaluate(t);

	Tangent.x = m_XQuadratics[iIndex].EvaluateDerivative(t);
	Tangent.y = m_YQuadratics[iIndex].EvaluateDerivative(t);
	Tangent.z = m_ZQuadratics[iIndex].EvaluateDerivative(t);

	if (m_bForceInPlaneTangent)
		Tangent.z = 0;

	Normalise(Tangent);

	CSlaveNode NewNode(Pos, Tangent);

	InterpolateUp(MasterNodes[iIndex], MasterNodes[iIndex + 1], NewNode, t);
	InterpolateAngle(MasterNodes[iIndex], MasterNodes[iIndex + 1], NewNode, t);

	NewNode.SetIndex(iIndex);
	NewNode.SetT(t);

	return NewNode;
}

void CInterpolationQuadratic::Initialise(const vector<CNode> &MasterNodes) const
{
	vector<double> X;
	vector<double> Y;
	vector<double> Z;
	vector<CNode>::const_iterator itNode;
	for (itNode = MasterNodes.begin(); itNode != MasterNodes.end(); ++itNode)
	{
		X.push_back(itNode->GetPosition().x);
		Y.push_back(itNode->GetPosition().y);
		Z.push_back(itNode->GetPosition().z);
	}
	GetNaturalQuadraticSplines(X, m_XQuadratics);
	GetNaturalQuadraticSplines(Y, m_YQuadratics);
	GetNaturalQuadraticSplines(Z, m_ZQuadratics);

}

/*void CInterpolationQuadratic::GetNaturalQuadraticSplines(const vector<double> &x, const vector<double> &y, vector<QUADRATICEQUATION> &Quadratics)
{
	Quadratics.clear();
	int N = x.size() - 1;

	if (N <= 0)
		return;

	CMatrix Right(3*N, 1);
	CMatrix Left(3*N, 3*N);
	CMatrix Coeff(3*N, 1);

	int j = 0;
	int f = 0;
	//Populate left and right matrix
	for (int i = 1; i < 2 * N; i = i + 2)
	{
		Left(i, f) = pow(x[j],2);
		Left(i, f + 1) = x[j];
		Left(i, f + 2) = 1;
		Right(i, 0) = y[j];
		j = j + 1;
		
		Left(i+1, f) = pow(x[j], 2);
		Left(i+1, f + 1) = x[j];
		Left(i+1, f + 2) = 1;
		Right(i + 1,0) = y[j];
		f = f + 3;
	}
	
	j = 0;
	int l = 1;
	for (int i = (2 * N) + 1; i < 3 * N; i++)
	{
		Left(i, j) = 2 * x[l];
		Left(i, j + 1) = 1;
		Left(i, j+3) = -2 * x[l];
		Left(i, j+4) = -1;
		Right(i, 0) = 0;
		j = j + 3;
		l = l + 1;
	}

	for (int i = 0; i < Right.GetHeight(); i++)
	{
		TGLOG("Right " << Right(i, 0) << endl;)
	}

	Left(0, 0) = 1;

	for (int i = 0; i < Left.GetHeight(); i++)
	{
		for (int j = 0; j < Left.GetWidth(); j++)
		{
			TGLOG(i, j);
			TGLOG("Left " << Left(i, j) << endl;)
		}

	}
	// Get the Inverse of the left matrix
	double det = Left.GetDeterminant();

	if (!isnan(det))
	{
		CMatrix LeftInverse;
		Left.GetInverse(LeftInverse);
		Coeff = LeftInverse * Right;

		for (int i = 0; i < Left.GetHeight(); i++)
		{
			for (int j = 0; j < Left.GetWidth(); j++)
			{
				TGLOG(i, j);
				TGLOG("LeftInverse " << LeftInverse(i, j) << endl;)
			}

		}
		for (int i = 0; i < Coeff.GetHeight(); i++)
		{
			//TGLOG("LeftInverse " << LeftInverse(i, 0) << endl);
			TGLOG("Coeff " << Coeff(i, 0) << endl;);
		}
		///Coeff now contains the coefficients

		double a, b, c;

		// Calculate the coefficients of the Quadratics
		for (int i = 0; i < 3 * N; i = i + 3)
		{
			a = Coeff(i, 0);
			b = Coeff(i + 1, 0);
			c = Coeff(i + 2, 0);
			Quadratics.push_back(QUADRATICEQUATION(a, b, c));
			TGLOG("coeffs " << a << endl;)
		}

	}
	else
	{
		for (int i = 0; i<Left.GetHeight(); i++)
		{
			Coeff(i, 0) = 0;
		}

		double a, b, c;
		// Calculate the coefficients of the Quadratics
		for (int i = 0; i < 3 * N; i = i + 3)
		{
			a = Coeff(i, 0);
			b = Coeff(i + 1, 0);
			c = Coeff(i + 2, 0);
			Quadratics.push_back(QUADRATICEQUATION(a, b, c));
			TGLOG("coeffs " << a << endl;)
		}
	}
	//TGLOG("coeffs " << a, b, c << endl;)
	
	/*int i= N-1
	a = coeff(i, 1);
	b = coeff(i + 1, 1);
	c = coeff(i + 2, 1);
	Quadratics.push_back(QUADRATICEQUATION(a, b, c));
	
}*/



void CInterpolationQuadratic::GetNaturalQuadraticSplines(const vector<double> &x, vector<QUADRATICEQUATION> &Quadratics)
{
	Quadratics.clear();
	int N = int(x.size());

	if (N <= 0)
		return;

	CMatrix Left(N, N);
	CMatrix Right(N, 1);
	CMatrix D;

	int i;

	// Populate Left Matrix as shown above
	for (i = 1; i < N-1 ; ++i)
	{
		Left(i, i) = 1;
		//Left(i + 1, i) = 1;
		Left(i, i + 1) = 1;
	}
	Left(0, 0) = 2;
	Left(N - 1, N - 2) = 0;
	Left(N - 1, N - 1) = 1;

	/*for (i = 0; i < Left.GetHeight(); ++i)
	{
		for (int j = 0; j < Left.GetWidth(); ++j)
		{
			TGLOG(" LEFT " << i << ", " << j << " " << Left(i, j) << endl;)
		}
	}*/

	// Populate the Right Matrix as shown above
	Right(0, 0) = 2 * (x[1] - x[0]);
	for (i = 1; i < N-1; ++i)
	{
		Right(i, 0) = 2 * (x[i + 1] - x[i]);
	}
	Right(N-1, 0) = 2 * (x[N-1] - x[N-2]);

	// Get the Inverse of the left matrix
	CMatrix LeftInverse;
	Left.GetInverse(LeftInverse);
	D.EqualsMultiple(LeftInverse, Right);

	// D now contains the derivatives at the knots

	double a, b, c, d;

	// Calculate the coefficients of the cubics
	for (i = 0; i < N-1; ++i)
	{
		a = x[i];
		b = D(i, 0);
		c = x[i + 1] - x[i] - D(i, 0);
		
		Quadratics.push_back(QUADRATICEQUATION(a, b, c));
	}
}
