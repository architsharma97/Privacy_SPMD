// Mason Rumuly
// Updated: 17 November 2016
#include "HungarianAlgorithm.h"
// Solve cost matrix using Hungarian algorithm

// ordered pair
struct Opair {
	Opair();
	Opair(int x, int y) : a(x), b(y) {}
	int a, b;
};

// used for matrix operations, esp. finding lines
struct elcounter {
	// internal class
	struct elcount {
		// Constructor
		elcount(const unsigned int &e, const unsigned int &d) :element(e), count(1), dim(d) {}
		// Repository
		unsigned int element, count, dim;
	};

	// methods
	// add element
	void add_element(const unsigned int &e, const unsigned int &d) {
		for (unsigned int i = 0; i < elements.size(); ++i)
			if (elements[i].element == e && elements[i].dim == d) {
				elements[i].count++; return;
			}
		elements.push_back(elcount(e, d));
	}

	// get mode
	Opair mode() {
		unsigned int m_count = elements[0].count;
		Opair m(elements[0].element, elements[0].dim);
		for (unsigned int i = 1; i < elements.size(); ++i)
			if (m_count < elements[i].count) {
				m.a = elements[i].element; m.b = elements[i].dim;
				m_count = elements[i].count;
			}
		return m;
	}

private:
	vector<elcount> elements;
};

// Matrix Operations ----------------------------------------------------

// Default Constructor
template <class T>
SquareMatrix<T>::SquareMatrix()
{
	msize = 0;
	s_matrix = nullptr;
}

// Constructor based on size
template <class T>
SquareMatrix<T>::SquareMatrix(const unsigned int &size)
{
	msize = size;
	if (size <= 0)
		SquareMatrix();
	else {
		s_matrix = new T*[size];
		for (unsigned int i = 0; i < size; ++i)
			s_matrix[i] = new T[size];
		clear(); // initialize to all-zeros
	}
}

// Copy constructor w/ parentheses
template <class T>
SquareMatrix<T>::SquareMatrix(const SquareMatrix<T> &other)
{
	SquareMatrix(size);
	if (msize > 0)
		for (unsigned int i = 0; i < msize; ++i)
			for (unsigned int j = 0; j < msize; ++j)
				this(i,j) = other(i, j);
}

// copy constructor w/ operator
template <class T>
SquareMatrix<T>& SquareMatrix<T>::operator = (const SquareMatrix<T> &other)
{
	if (s_matrix != nullptr) // don't leak
		for (unsigned int i = 0; i < size; i++)
			delete[] s_matrix[i];
	delete[] 
	SquareMatrix(other);
}

template <class T>
SquareMatrix<T>::~SquareMatrix()
{
	if (s_matrix != nullptr) // don't leak
		for (unsigned int i = 0; i < msize; i++)
			delete[] s_matrix[i];
	s_matrix = nullptr;
}

// get element specified by index where changeable
template <class T>
inline T& SquareMatrix<T>::operator() (const unsigned int &row, const unsigned int &column)
{
	if (row < msize && column < msize)
		return s_matrix[row][column];
	else
		throw exception("Out of Bounds");
}

// Get element specified by index in constant contexts
template <class T>
inline const T& SquareMatrix<T>::operator() (const unsigned int &row, const unsigned int &column) const
{
	if (row < msize && column < msize)
		return &s_matrix[row][column];
	else
		return nullptr;
}

// Get size of matrix
template <class T>
const unsigned int SquareMatrix<T>::size() const
{
	return msize;
}

// Get minimum value in matrix
template <class T>
const T SquareMatrix<T>::min() const
{
	T min;
	if(msize == 0)
		min = NULL;
	else {
		min = s_matrix[0][0];
		if (msize > 1)
			for (unsigned int i = 0; i < msize; i++)
				for (unsigned int j = 0; j < msize; j++)
					if (s_matrix[i][j] < min)
						min = s_matrix[i][j];
	}
	return min;
}

// Get maximum value in matrix
template <class T>
const T SquareMatrix<T>::max() const
{
	T max;
	if (msize == 0)
		max = NULL;
	else {
		max = s_matrix[0][0];
		if (msize > 1)
			for (unsigned int i = 0; i < msize; i++)
				for (unsigned int j = 0; j < msize; j++)
					if (s_matrix[i][j] > max)
						max = s_matrix[i][j];
	}
	return max;
}

// Set to all zeros
template <class T>
void SquareMatrix<T>::clear()
{ // set to all zeros
	if (msize > 0)
		for (unsigned int i = 0; i < msize; ++i)
			for (unsigned int j = 0; j < msize; ++j)
				s_matrix[i][j] = 0;
}

// reduce by columns and by rows. T must have default constructor, comparison, and subtraction.
template <class T>
void SquareMatrix<T>::reduce()
{
	T temp_min;
	
	// by rows
	for (unsigned int i = 0; i < msize; ++i) {
		// find minimum
		temp_min = s_matrix[i][0];
		for (unsigned int j = 1; j < msize; ++j)
			if (s_matrix[i][j] < temp_min)
				temp_min = s_matrix[i][j];
		// subtract
		for (unsigned int j = 0; j < msize; ++j)
			s_matrix[i][j] -= temp_min;
	}

	// by columns
	for (unsigned int j = 0; j < msize; ++j) {
		// find minimum
		temp_min = s_matrix[0][j];
		for (unsigned int i = 1; i < msize; ++i)
			if (s_matrix[i][j] < temp_min)
				temp_min = s_matrix[i][j];
		// subtract
		for (unsigned int i = 0; i < msize; ++i)
			s_matrix[i][j] -= temp_min;
	}
}

// Hungarian Algorithm Solver -----------------------------------
// zero removal functor
struct AccountedFor {
	AccountedFor(Opair c) : comp(c) {}
	bool operator () (const Opair &zero)
	{
		return((comp.b == 0 && zero.a == comp.a) || (comp.b == 1 && zero.b == comp.a));
	}
private:
	Opair comp;
};

// check whether index is covered
bool covered(const unsigned int &index, const unsigned int &dimension, const vector<Opair> &lines) {
	for (unsigned int i = 0; i < lines.size(); ++i)
		if (lines[i].a == index && lines[i].b == dimension)
			return true;
	return false;
}

//meat
void hungarian(const vector<Path> &candidatesStart, const vector<Path> &candidatesEnd, vector<unsigned int> &match, vector<double> &strength)
{
	// working matrix
	SquareMatrix<double> cost_matrix(candidatesStart.size());
	for (unsigned int i = 0; i < candidatesStart.size(); i++) {
		match.push_back(0); strength.push_back(0);
		for (unsigned int j = 0; j < candidatesEnd.size(); j++) {
			cost_matrix(i, j) = pathMisMatch(candidatesStart[i], candidatesEnd[j]);
		}
	}
	cost_matrix.reduce();

	// list zeros and elements
	list<Opair> zeros;
	list<Opair>::iterator it;

	// iterate until complete
	bool done = false;
	while (!done) {
		// Find zeros
		for (unsigned int i = 0; i < candidatesStart.size(); i++)
			for (unsigned int j = 0; j < candidatesEnd.size(); j++) {
				if (cost_matrix(i, j) == 0)
					zeros.push_back(Opair(i, j));
			}

		// list coverage lines
		vector<Opair> lines; // a = index, b = dimension

		// Find Lines
		while (!zeros.empty()) {
			elcounter ec;
			it = zeros.begin();
			// get list of 
			for (unsigned int i = 0; i < zeros.size(); i++) {
				ec.add_element(it->a, 0); ec.add_element(it->b, 1);
				advance(it, 1);
			}
			lines.push_back(ec.mode()); // record line
			zeros.remove_if(AccountedFor(ec.mode())); // remove accounted-for zeros
		} // finish when all zeros accounted for

		done = (lines.size() == candidatesStart.size()); // done when everything is matched

		if (!done) {
			// find minimum uncovered element
			double min = cost_matrix.max();
			for (unsigned int i = 0; i < candidatesStart.size(); i++)
				if (!covered(i, 0, lines))
					for (unsigned int j = 0; j < candidatesEnd.size(); j++)
						if (!covered(j, 1, lines) && cost_matrix(i, j) < min)
							min = cost_matrix(i, j);

			// add to every double-covered element, subtract from every uncovered
			for (unsigned int i = 0; i < candidatesStart.size(); i++)
				if (!covered(i, 0, lines)) {
					for (unsigned int j = 0; j < candidatesEnd.size(); j++)
						if (!covered(j, 1, lines))
							cost_matrix(i, j) -= min; // uncovered here
				}
				else
					for (unsigned int j = 0; j < candidatesEnd.size(); j++)
						if (covered(j, 1, lines))
							cost_matrix(i, j) += min; // double covered here
		}
	}


	// Translate and return results; assumes only one zero in each row/column
	for (unsigned int i = 0; i < candidatesStart.size(); i++) {
		for (unsigned int j = 0; j < candidatesEnd.size(); j++) {
			//cout << cost_matrix(i, j) << '\t';
			if (cost_matrix(i, j) == 0) {
				match[i] = j;
				strength[i] = pathMatch(candidatesStart[i], candidatesEnd[j]);
			}
		}
		//cout << endl;
	}
}