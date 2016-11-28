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
	return (name + ',' +
		to_string(avgHeading) + ',' + to_string(stdHeading) + ',' +
		to_string(avgSpeed) + ',' + to_string(stdSpeed) + ',' +
		to_string(avgAccx) + ',' + to_string(stdAccx) + ',' +
		to_string(avgAccy) + ',' + to_string(stdAccy));
}

// get average and std for path from the set of points
void pathFromPoints(const vector<PathPoint> &points, Path &path)
{
	// get averages
	for (unsigned int i = 0; i < points.size() / 2; ++i) {
		path.avgHeading += points[i].heading;
		path.avgSpeed += points[i].speed;
		path.avgAccx += points[i].ax;
		path.avgAccy += points[i].ay;
	}
	path.avgHeading /= (points.size() / 2);
	path.avgSpeed /= (points.size() / 2);
	path.avgAccx /= (points.size() / 2);
	path.avgAccy /= (points.size() / 2);

	// get std
	for (unsigned int i = 0; i < points.size() / 2; ++i) {
		path.stdHeading += pow((path.avgHeading - points[i].heading), 2);
		path.stdSpeed += pow((path.avgSpeed - points[i].speed), 2);
		path.stdAccx += pow((path.avgAccx - points[i].ax), 2);
		path.stdAccy += pow((path.avgAccy - points[i].ay), 2);
	}
	path.stdHeading = sqrt(path.stdHeading / points.size());
	path.stdSpeed = sqrt(path.stdSpeed / (points.size() / 2));
	path.stdAccx = sqrt(path.stdAccx / (points.size() / 2));
	path.stdAccy = sqrt(path.stdAccy / (points.size() / 2));
}

//----------------------------------------------------------------



// take percentage match
double match(const double &q1, const double &q2) {
	if (q1 / q2 <= 1 && q1/q2 >= -1)
		return log(abs(q1 / q2));
	else
		return log(abs(q2 / q1));
}

// Find percentage match between the two paths (additive over characteristics)
double pathMatch(const Path &pathA, const Path &pathB) {
	return pow(10,(aHW * match(pathA.avgHeading, pathB.avgHeading) +
		aSW * match(pathA.avgSpeed, pathB.avgSpeed) +
		aXW * match(pathA.avgAccx, pathB.avgAccx) +
		aYW * match(pathA.avgAccy, pathB.avgAccy) +
		sHW * match(pathA.stdHeading, pathB.stdHeading) +
		sSW * match(pathA.stdSpeed, pathB.stdSpeed) +
		sXW * match(pathA.stdAccx, pathB.stdAccx) +
		sYW * match(pathA.stdAccy, pathB.stdAccy)));
}

// Find percentage mismatch between two paths (for hungarian minimization
double pathMisMatch(const Path &pathA, const Path &pathB) {
	return (1 - pathMatch(pathA, pathB));
}

//----------------------------------------------------------------
