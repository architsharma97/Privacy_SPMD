// Mason Rumuly
// Updated: 17 November 2016
#include "Traffic.h"
// Header for function(s) solving Hungarian Algorithm

template <class T>
class SquareMatrix {
public:
	// Constructors
	SquareMatrix();
	SquareMatrix(const unsigned int &size);
	SquareMatrix(const SquareMatrix<T> &other);
	SquareMatrix<T> & operator = (const SquareMatrix<T> &other);

	// Destructor
	~SquareMatrix();

	// Modify matrix
	void clear();
	void reduce();

	// Return values
	T& operator() (const unsigned int &row, const unsigned int &column);
	const T& operator() (const unsigned int &row, const unsigned int &column) const;
	const unsigned int size() const;
	const T min() const;
	const T max() const;

	// Repository
private:
	unsigned int msize;
	T **s_matrix;
};

void hungarian(const vector<Path> &candidatesStart, const vector<Path> &candidatesEnd, vector<unsigned int> &match, vector<double> &matchstrength);