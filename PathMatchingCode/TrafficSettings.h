// Mason Rumuly
// Updated: 8 October 2016
#include "std_lib_facilities_4.h"

// modify these to set target files
//const string set = "April2013";
const string set = "October2012";
//const string pathsList = "12";

// modify these to change match parameters
const double minDistance = 50; // 'radius' of intersection
const double iLat = 42.2821417; // intersection latitude
const double iLong = -83.748524; // intersection longitude
const double elevRadius = 256 + 6371000; // elevation above sea level + average sea-level radius
const long tTotal = 0; // min total path time (minutes)
const long tBefore = 1; // min path time before intersection (minutes)
const long tAfter = 1; // min path time after intersection (minutes)

// matching weights
constexpr double aHW = 0, aSW = 2, aXW = 0, aYW = 0, sHW = 0, sSW = 4, sXW = 0, sYW = 4;
constexpr double W = (aHW + aSW + aXW + aYW + sHW + sSW + sXW + sYW);
