// Mason Rumuly
// Updated: 8 October 2016
#include "HungarianAlgorithm.h"
#include "HungarianAlgorithm\munkres.h"
// charactarize paths by time
// Active Filters: No skipped messages

const string pathlist = "path_list.txt"; // Path List File
const string folder = "sanitizedPathsApril2013\\"; // master folder

int main(int argc, char* argv[])
{
	//----------------------------------------------------------------------------
	// Characterize

	// create constants
	Intersection intersect(42.2821417, -83.748524); // South Main and Huron
	string listFile = folder + pathlist;

	// create working variables
	string result, pathname, pointBuffer;
	stringstream r;
	PathPoint buff;
	vector<PathPoint> path;
	Path temp;
	vector<Path> candidatesStart, candidatesEnd;
	bool done;

	// prepare output file
	ofstream records{ "MatchingCharacter.txt" };

	ifstream loadfile{ listFile };
	while (loadfile >> pathname) { // load filenames
		// open path file
		ifstream loadPath{ (folder + pathname) };
		//-----------------------------------------
		
		
		// parse beginning of path
		temp = *new Path;
		temp.name = pathname + "_A";
		done = false;
		while (loadPath.good() && !done) {
			getline(loadPath, pointBuffer);
			r.str(pointBuffer);
			r.clear();
			parsePoint(r, buff);
			if (buff.fileID != 0) { //make sure line read correctly
				path.push_back(buff);
				done = inIntersection(buff.lattitude, buff.longitude, intersect);
			}
		}
		pathFromPoints(path, temp);

		// save resulting segment
		candidatesStart.push_back(temp);
		records << temp.comSepChar() << endl;
		cout << temp.comSepChar() << endl;
		//-------------------------


		// discard path inside intersection
		done = false;
		while (loadPath.good() && !done) {
			getline(loadPath, pointBuffer);
			r.clear();
			r.str(pointBuffer);
			parsePoint(r, buff);
			done = !inIntersection(buff.lattitude, buff.longitude, intersect);
		}
		//-------------------------


		// parse end of path
		temp = *new Path;
		temp.name = pathname + "_B";
		while (loadPath.good()) {
			getline(loadPath, pointBuffer);
			r.clear();
			r.str(pointBuffer);
			parsePoint(r, buff);
			if (buff.fileID != 0) { //make sure line read correctly
				path.push_back(buff);
			}
		}
		pathFromPoints(path, temp);

		// save resulting segment
		candidatesEnd.push_back(temp);
		records << temp.comSepChar() << endl;
		cout << temp.comSepChar() << endl;
		//-------------------------
	}

	// trailing space
	records << "\n\n\n"; 
	cout << "\n\n\n";

	//----------------------------------------------------------------------------
	// Matching algorithm (using the Hungarian algorithm)
	vector<unsigned int> matchtemp;
	vector<double> strengthtemp;


	//**********************
	Matrix<double> costmatrix(candidatesStart.size(), candidatesStart.size());

	for (unsigned int i = 0; i < candidatesStart.size(); i++) {
		matchtemp.push_back(0); strengthtemp.push_back(0);
		for (unsigned int j = 0; j < candidatesEnd.size(); j++) {
			costmatrix(i, j) = pathMisMatch(candidatesStart[i], candidatesEnd[j]);
		}
	}

	Munkres<double> m;
	m.solve(costmatrix);

	for (unsigned int i = 0; i < candidatesStart.size(); i++) 
		for (unsigned int j = 0; j < candidatesEnd.size(); j++)
			if (costmatrix(i, j) == 0) {
				matchtemp[i] = j;
				strengthtemp[i] = pathMatch(candidatesStart[i], candidatesEnd[j]);
			}
	//**********************



	

	try {
		//hungarian(candidatesStart, candidatesEnd, matchtemp, strengthtemp);


		// Output match results
		bool success = false;
		double successRate = 0;
		for (unsigned int i = 0; i < matchtemp.size(); i++) {
			success = ((candidatesStart[i].name.substr(0, candidatesStart[i].name.size() - 2)) ==
				candidatesEnd[matchtemp[i]].name.substr(0, candidatesEnd[matchtemp[i]].name.size() - 2));
			successRate += success;

			records << candidatesStart[i].name << ',' << candidatesEnd[matchtemp[i]].name << ',' <<
				strengthtemp[i] << ',' << success << endl;
			cout << candidatesStart[i].name << ',' << candidatesEnd[matchtemp[i]].name << ',' <<
				strengthtemp[i] << ',' << success << endl;
		}

		successRate /= (1.0 * matchtemp.size());
		records << '\n' << successRate << endl;
		cout << '\n' << successRate << endl;
	}
	catch (exception e) {
		cerr << e.what();
	}
	catch (...) {
		cerr << "SOMETHING WEIRD";
	}


	records.close(); // finish output file
	keep_window_open();
}