try:
    from xml.etree import cElementTree as ET
except ImportError, e:
    from xml.etree import ElementTree as ET

def get_intersections(osm, input_type='file'):
    """
    This method reads the passed osm file (xml) and finds intersections (nodes that are shared by two or more roads)

    :param osm: An osm file or a string from get_osm()
    """
    intersection_coordinates = []
    if input_type == 'file':
        tree = ET.parse(osm)
        root = tree.getroot()
        children = root.getchildren()
    elif input_type == 'str':
        tree = ET.fromstring(osm)
        children = tree.getchildren()

    counter = {}
    for child in children:
        if child.tag == 'way':
            # Check if the way represents a "highway (road)"
            # If the way that we are focusing right now is not a road,
            # continue without checking any nodes
            road = False
            road_types = ('primary', 'secondary', 'residential', 'tertiary', 'service') 
            for item in child:
                if item.tag == 'tag' and item.attrib['k'] == 'highway' and item.attrib['v'] in road_types: 
                    road = True

            if not road:
                continue

            for item in child:
                if item.tag == 'nd':
                    nd_ref = item.attrib['ref']
                    if not nd_ref in counter:
                        counter[nd_ref] = 0
                    counter[nd_ref] += 1

    # Find nodes that are shared with more than one way, which
    # might correspond to intersections
    intersections = filter(lambda x: counter[x] > 1,  counter)


    # Extract intersection coordinates
    # You can plot the result using this url.
    # http://www.darrinward.com/lat-long/
    for child in children:
        if child.tag == 'node' and child.attrib['id'] in intersections:
            coordinate = child.attrib['lat'] + ',' + child.attrib['lon']
            intersection_coordinates.append(coordinate)
    return intersection_coordinates

def main():
	intersections=get_intersections('./ann_arbor_v2.osm')
    
	# print intersections
	intersections_file=open('./ann_arbor_v2_intersections_coordinates.txt','a')
	for entry in intersections:
		intersections_file.write(entry+'\n')
	intersections_file.close()

if __name__ == '__main__':
	main()
