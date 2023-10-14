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

#pragma once
#include "Interpolation.h"

namespace TexGen
{
	using namespace std;

	/// Quadratic spline interpolation for yarn paths
	class CLASS_DECLSPEC CInterpolationQuadratic : public CInterpolation
	{
	public:
		CInterpolationQuadratic(bool bPeriodic = false, bool bForceInPlaneTangent = false, bool bForceMasterNodeTangent = false);
		CInterpolationQuadratic(TiXmlElement &Element);
		~CInterpolationQuadratic(void);

		CInterpolation* Copy() const { return new CInterpolationQuadratic(*this); }
		string GetType() const { return "CInterpolationQuadratic"; }
		//		void PopulateTiXmlElement(TiXmlElement &Element, OUTPUT_TYPE OutputType) const;

				/// Create the spline cubic equations and store them in m_?Cubics
		void Initialise(const vector<CNode> &MasterNodes) const;

		/// Get a node from parametric function where t is specified
		CSlaveNode GetNode(const vector<CNode> &MasterNodes, int iIndex, double t) const;

	protected:
		/// Struct to represent a cubic equation
		struct QUADRATICEQUATION
		{
			QUADRATICEQUATION(double a, double b, double c)
				: m_a(a)
				, m_b(b)
				, m_c(c)
			{}

			double Evaluate(double x) const
			{
				return ((m_c*x) + m_b)*x + m_a;
			}

			double EvaluateDerivative(double x) const
			{
				return (2 * m_c*x) + m_b;
			}

		protected:
			double m_a, m_b, m_c;
		};

		//static void GetPeriodicCubicSplines(const vector<double> &Knots, vector<CUBICEQUATION> &Cubics);
		//static void GetNaturalQuadraticSplines(const vector<double> &x, const vector<double> &y, vector<QUADRATICEQUATION> &Quadratics);
		static void GetNaturalQuadraticSplines(const vector<double> &x, vector<QUADRATICEQUATION> &Quadratics);

		mutable vector<QUADRATICEQUATION> m_XQuadratics;
		mutable vector<QUADRATICEQUATION> m_YQuadratics;
		mutable vector<QUADRATICEQUATION> m_ZQuadratics;
	};

};	// namespace TexGen