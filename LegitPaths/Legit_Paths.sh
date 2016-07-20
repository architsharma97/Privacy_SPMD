min_points=3000
april_paths_dir='/scratch/user/architsh/PathSegmentsApril2013'
october_paths_dir='/scratch/user/architsh/PathSegmentsOctober2012'
april_path_counts='/home/architsh/Privacy_SPMD/RouteTracing/path_files_counts_april_2013_5_100.txt'
october_path_counts='/home/architsh/Privacy_SPMD/RouteTracing/path_files_counts_october_2012_5_100.txt'
april_legit_paths='/home/architsh/Privacy_SPMD/LegitPaths/LegitPathsApril2013'
october_legit_paths='/home/architsh/Privacy_SPMD/LegitPaths/LegitPathsOctober2012'

python Strong_Paths.py $min_points $april_paths_dir $april_path_counts $april_legit_paths
python Strong_Paths.py $min_points $october_paths_dir $october_path_counts $october_legit_paths


