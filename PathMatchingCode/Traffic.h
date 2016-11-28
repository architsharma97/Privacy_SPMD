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
	Path(): avgHeading(0), avgSpeed(0), avgAccx(0), avgAccy(0),
		stdHeading(0), stdSpeed(0), stdAccx(0), stdAccy(0) {}
	/*Path(): start(0), earlyI(0), lateI(0), end(0) {}

	long start, earlyI, lateI, end; // store as microseconds*/
	double avgHeading, avgSpeed, avgAccx, avgAccy,
		stdHeading, stdSpeed, stdAccx, stdAccy;
	string name;

	string comSepChar() const;
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
void pathFromPoints(const vector<PathPoint> &points, Path &path);
double pathMatch(const Path &pathA, const Path &pathB);
double pathMisMatch(const Path &pathA, const Path &pathB);
