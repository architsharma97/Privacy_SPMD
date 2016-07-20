radius=1500
april_legit_paths='/home/architsh/Privacy_SPMD/LegitPaths/LegitPathsApril2013'
october_legit_paths='/home/architsh/Privacy_SPMD/LegitPaths/LegitPathsOctober2012'
april_path_segments='/scratch/user/architsh/PathSegmentsApril2013'
october_path_segments='/scratch/user/architsh/PathSegmentsOctober2012'
april_city_path_list='/home/architsh/Privacy_SPMD/CityPaths/April2013'
october_city_path_list='/home/architsh/Privacy_SPMD/CityPaths/October2012'

python City_Paths.py $radius $april_legit_paths $april_path_segments $april_city_path_list
python City_Paths.py $radius $october_legit_paths $october_path_segments $october_city_path_list
