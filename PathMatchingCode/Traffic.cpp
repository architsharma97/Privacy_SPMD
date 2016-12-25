// Mason Rumuly
// Updated: 8 October 2016
#include "Traffic.h"

// Processing functions for BSM // 

// remove sections in a comma-separated list
void removeSections(stringstream &r, int const &numCommas )
{
	char discard;
	for (int i = 0; i < numCommas; ++i) {
		discard = ' ';
		while (discard != ',' && r.good()) {
			r >> discard;
		}
	}
}

// parse a point for time and location
void parsePoint(stringstream &line, PathPoint &point)
{
	try {
		line >> point.deviceID;
		removeSections(line, 1);
		line >> point.fileID;
		removeSections(line, 7);
		/*line >> point.gentime;
		removeSections(line, 2);
		line >> point.msgCount;
		removeSections(line, 1);
		line >> point.deciSecond;*/
		removeSections(line, 1);
		line >> point.lattitude;
		removeSections(line, 1);
		line >> point.longitude;
		removeSections(line, 1);
		line >> point.elevation;
		removeSections(line, 1);
		line >> point.speed;
		removeSections(line, 1);
		line >> point.heading;
		removeSections(line, 1);
		line >> point.ax;
		removeSections(line, 1);
		line >> point.ay;
		removeSections(line, 1);
		line >> point.az;
		removeSections(line, 1);
		line >> point.yawRate;
		removeSections(line, 2);
		line >> point.curveRadius;
		removeSections(line, 1);
		line >> point.confidence;
	}
	catch (...) {} //if device ID is still 0, it failed
}

// converts pair of GPS coordinate points to distance in meters
double GPSdist(const double &aLat, const double &aLong, const double &bLat, const double &bLong)
{
	return (elevRadius * pi * sqrt(pow((aLat - bLat), 2) + pow((aLong - bLong), 2)) / 180);
}

bool inIntersection(const double &rLat, const double &rLong, const Intersection &intersection)
{
	return (minDistance >= GPSdist(rLat, rLong, intersection.latitude, intersection.longitude));
}

// output comma-separated text entry charactarization
string Path::comSepChar() const
{
	stringstream l;
	l << name;
	// assemble string with attributes
	for (unsigned int i = 0; i < attributes.size(); i++)
		l << ',' << to_string(attributes[i]);

	return l.str();
}

int Path::attributeNumber() const
{
	return attributes.size();
}

// get average and std for path from the set of points
void pathFromPoints(const vector<PathPoint> &points, Path &path, const bool &before) // indicate front or back! THEN add split portion
{
		const unsigned int offset = 600; // length of excerpt
		unsigned int mainStart, mainEnd, minuteStart, minuteEnd;
		if (before) {
			mainStart = 0;
			mainEnd = points.size() - offset;
			minuteStart = mainEnd;
			minuteEnd = points.size();
		}
		else {
			mainStart = offset;
			mainEnd = points.size();
			minuteStart = 0;
			minuteEnd = mainStart;
		}

		try {
		// initialize attribute list
		for (unsigned int i = 0; i < 16; ++i)
			path.attributes.push_back(0);

		// get main averages
		for (unsigned int i = mainStart; i < mainEnd; ++i) {
			path.attributes[0] += points[i].heading;
			path.attributes[1] += points[i].speed;
			path.attributes[2] += points[i].ax;
			path.attributes[3] += points[i].ay;
		}
		path.attributes[0] /= (points.size() - offset);
		path.attributes[1] /= (points.size() - offset);
		path.attributes[2] /= (points.size() - offset);
		path.attributes[3] /= (points.size() - offset);

		// get main standard deviations
		for (unsigned int i = mainStart; i < mainEnd; ++i) {
			path.attributes[4] += pow((path.attributes[0] - points[i].heading), 2);
			path.attributes[5] += pow((path.attributes[1] - points[i].speed), 2);
			path.attributes[6] += pow((path.attributes[2] - points[i].ax), 2);
			path.attributes[7] += pow((path.attributes[3] - points[i].ay), 2);
		}
		path.attributes[4] = sqrt(path.attributes[4] / (points.size() - offset));
		path.attributes[5] = sqrt(path.attributes[5] / (points.size() - offset));
		path.attributes[6] = sqrt(path.attributes[6] / (points.size() - offset));
		path.attributes[7] = sqrt(path.attributes[7] / (points.size() - offset));

		// get minute averages
		for (unsigned int i = minuteStart; i < minuteEnd; ++i) {
			path.attributes[8] += points[i].heading;
			path.attributes[9] += points[i].speed;
			path.attributes[10] += points[i].ax;
			path.attributes[11] += points[i].ay;
		}
		path.attributes[8] /= offset;
		path.attributes[9] /= offset;
		path.attributes[10] /= offset;
		path.attributes[11] /= offset;

		// get minute standard deviations
		for (unsigned int i = minuteStart; i < minuteEnd; ++i) {
			path.attributes[12] += pow((path.attributes[0] - points[i].heading), 2);
			path.attributes[13] += pow((path.attributes[1] - points[i].speed), 2);
			path.attributes[14] += pow((path.attributes[2] - points[i].ax), 2);
			path.attributes[15] += pow((path.attributes[3] - points[i].ay), 2);
		}
		path.attributes[12] = sqrt(path.attributes[4] / offset);
		path.attributes[13] = sqrt(path.attributes[5] / offset);
		path.attributes[14] = sqrt(path.attributes[6] / offset);
		path.attributes[15] = sqrt(path.attributes[7] / offset);
	}
	catch (exception e) {
		cerr << endl << e.what() << points.size() << endl << mainStart << endl << mainEnd << endl << minuteStart << endl << minuteEnd << endl;
		keep_window_open();
	}
}

//----------------------------------------------------------------



// take percentage match
double match(const double &q1, const double &q2) {
	if (q1 / q2 <= 1 && q1/q2 >= -1)
		return abs(q1 / q2);
	else
		return abs(q2 / q1);
}

// sum all elements in a vector
template<class T>
T sum(const vector<T> &set) {
	if (set.size() == 0)
		return *new T{};
	else if(set.size() == 1)
		return set[0];
	else {
		T tot = set[0];
		for (unsigned int i = 1; i < set.size(); i++)
			tot += set[i];
		return tot;
	}
}

// Find percentage match between the two paths (additive over characteristics)
double pathMatch(const Path &pathA, const Path &pathB, const vector<float> &weights) {
	double wSum = 0;
	for (unsigned int i = 0; i < weights.size(); i++)
		wSum += weights[i] * match(pathA.attributes[i], pathB.attributes[i]);

	return wSum /sum(weights);
}

// Find percentage mismatch between two paths (for hungarian minimization
double pathMisMatch(const Path &pathA, const Path &pathB, const vector<float> &weights) {
	return (1 - pathMatch(pathA, pathB, weights));
}

//----------------------------------------------------------------
