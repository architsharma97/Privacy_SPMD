// Mason Rumuly
// Updated: 8 October 2016
#include "HungarianAlgorithm.h"
#include "HungarianAlgorithm\munkres.h"
// charactarize paths by time
// Active Filters: No skipped messages

const string pathlist = "path_list.txt"; // Path List File name

int main(int argc, char* argv[])
{
	//----------------------------------------------------------------------------
	// Characterize

	// create constants
	Intersection intersect(intersectLat, intersectLong);
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
	ofstream records{ "MatchingCharacter.txt" }; // for results of sorting
	ofstream splitpathlist{ splitfolder + pathlist }; // for listing the split paths in the folder
	ofstream splitpath; // for creating split path files

	ifstream loadfile{ listFile };
	while (loadfile >> pathname) { // load filenames
		// open path file
		ifstream loadPath{ (folder + pathname) };
		//-----------------------------------------
		
		
		// parse beginning of path
		path = *new vector<PathPoint>;
		temp = *new Path;
		temp.name = pathname.substr(0, pathname.length() - 4) + "_A";
		splitpathlist << temp.name << ".txt" << endl;
		splitpath.open(splitfolder + temp.name + ".txt");
		done = false;
		while (loadPath.good() && !done) {
			getline(loadPath, pointBuffer);
			splitpath << pointBuffer << endl;
			r.str(pointBuffer);
			r.clear();
			parsePoint(r, buff);
			if (buff.fileID != 0) { //make sure line read correctly
				path.push_back(buff);
				done = inIntersection(buff.lattitude, buff.longitude, intersect);
			}
		}
		splitpath.close();
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
		path = *new vector<PathPoint>;
		temp = *new Path;
		temp.name = pathname.substr(0, pathname.length() - 4) + "_B";
		splitpathlist << temp.name << ".txt" << endl;
		splitpath.open(splitfolder + temp.name + ".txt");
		while (loadPath.good()) {
			getline(loadPath, pointBuffer);
			splitpath << pointBuffer << endl;
			r.clear();
			r.str(pointBuffer);
			parsePoint(r, buff);
			if (buff.fileID != 0) { //make sure line read correctly
				path.push_back(buff);
			}
		}
		splitpath.close();
		pathFromPoints(path, temp);

		// save resulting segment
		candidatesEnd.push_back(temp);
		records << temp.comSepChar() << endl;
		cout << temp.comSepChar() << endl;
		//-------------------------
	}

	int bridge[15] = {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0};
	for (int pylon = 0; pylon < 8; pylon++) {

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
				costmatrix(i, j) = pathMisMatch(candidatesStart[i], candidatesEnd[j],
					bridge[pylon + 7], bridge[pylon + 6], bridge[pylon + 5], bridge[pylon + 4],
					bridge[pylon + 3], bridge[pylon + 2], bridge[pylon + 1], bridge[pylon + 0]);
			}
		}

		Munkres<double> m;
		m.solve(costmatrix);

		for (unsigned int i = 0; i < candidatesStart.size(); i++)
			for (unsigned int j = 0; j < candidatesEnd.size(); j++)
				if (costmatrix(i, j) == 0) {
					matchtemp[i] = j;
					strengthtemp[i] = pathMatch(candidatesStart[i], candidatesEnd[j],
						bridge[pylon + 7], bridge[pylon + 6], bridge[pylon + 5], bridge[pylon + 4],
						bridge[pylon + 3], bridge[pylon + 2], bridge[pylon + 1], bridge[pylon + 0]);
				}
		//**********************

		try {
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
	}
	records.close(); // finish output file
	keep_window_open();
}