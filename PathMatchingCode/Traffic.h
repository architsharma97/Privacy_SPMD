// Mason Rumuly
// Updated: 8 October 2016
#include "TrafficSettings.h"

const double pi = 3.141592653589793238462643383279502884;

// Classes //
struct Intersection {
	Intersection(double lat, double lon): latitude(lat), longitude(lon){}
	
	double latitude, longitude;
	};

struct Path {
	Path() {}

		/* List of attributes in order. Use vector for scalability
		avgHeading, avgSpeed, avgAccx, avgAccy,
		stdHeading, stdSpeed, stdAccx, stdAccy,
		closeAvgHeading, closeAvgSpeed, closeAvgAccx, closeAvgAccy,
		closeStdHeading, closestdSpeed, closeStdAccx, closeStdAccy*/
	vector<double> attributes;

	string name;

	string comSepChar() const;
	int attributeNumber() const;
	};

struct PathPoint {
	PathPoint(): deviceID(0), fileID(0), msgCount(0), confidence(0), gentime(0), deciSecond(0) {}

	int deviceID, fileID, msgCount, confidence;
	long gentime, deciSecond;
	double lattitude, longitude, elevation, speed, heading, ax, ay,
		az, yawRate, curveRadius;
};

// Declare Processing functions for BSM // 
void removeSections(stringstream &r, int const &numCommas);
void parsePoint(stringstream &line, PathPoint &point);
bool inIntersection(const double &rLat, const double &rLong, const Intersection &intersection);
double GPSdist(const double &aLat, const double &aLong, const double &bLat, const double &bLong);
void pathFromPoints(const vector<PathPoint> &points, Path &path, const bool &before);
double pathMatch(const Path &pathA, const Path &pathB, const vector<float> &weights);
double pathMisMatch(const Path &pathA, const Path &pathB, const vector<float> &weights);
