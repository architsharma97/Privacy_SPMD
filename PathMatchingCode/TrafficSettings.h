// Mason Rumuly
// Updated: 8 October 2016
#include "std_lib_facilities_4.h"
//18th on 

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

// matching weights - consider making arrays
//constexpr double aHW = 0, aSW = 0, aXW = 0, aYW = 0, sHW = 0, sSW = 0, sXW = 0, sYW = 1;
//constexpr double W = (aHW + aSW + aXW + aYW + sHW + sSW + sXW + sYW);

// ---------------------------------------------------------
// Data Set info
/*
// Main and Huron April
const string folder = "sanitizedPathsApril2013\\"; // master folder
const string splitfolder = "SplitPaths4thLibertyApril\\"; // folder for split paths
const double intersectLat = 42.2821417;
const double intersectLong = -83.748524;
*/
/*
// State and Huron April
const string folder = "StateHuronApril2013\\"; // master folder
const string splitfolder = "SplitPathsStateHuronApril\\"; // folder for split paths
const double intersectLat = 42.2811913;
const double intersectLong = -83.7430864;
*/
/*
// State and Huron October
const string folder = "StateHuronOctober2012\\"; // master folder
const string splitfolder = "SplitPathsStateHuronOctober\\"; // folder for split paths
const double intersectLat = 42.2811913;
const double intersectLong = -83.7430864;
*/
/*
// 4th and Liberty April
const string folder = "4thLibertyApril2013\\"; // master folder
const string splitfolder = "SplitPaths4thLibertyApril\\"; // folder for split paths
const double intersectLat = 42.2795373; // Main and Huron
const double intersectLong = -83.7495362;
*/
/*
// 4th and Liberty October
const string folder = "4thLibertyOctober2012\\"; // master folder
const string splitfolder = "SplitPaths4thLibertyOctober\\"; // folder for split paths
const double intersectLat = 42.2795373; // Main and Huron
const double intersectLong = -83.7495362;
*/
