#!/usr/bin/env python
# create_html16_facilities_map
# This script creates an HTML map that visualizes Internet exchange points (IXPs) and colocation facilities in the UK.
# It processes PeeringDB data, extracts facility and organization details, and generates a Leaflet.js-compatible HTML page.

# Function to create the initial HTML header and set the map center and zoom level.
def create_header_html(filename):           
        central_lon = -2.23  # Longitude to center the map on (UK)
        central_lat = 52.369  # Latitude to center the map on (UK)

        # Copy a base HTML header to the new file and set file permissions
        cmd = 'cp html/head.html ' + filename
        cmd2 = 'chmod 766 ' + filename
        os.system(cmd)
        os.system(cmd2)

        # Append the initial Leaflet map view (center coordinates and zoom level)
        ip = open(filename, 'a')
        ip.write(str(central_lat) + ", " + str(central_lon) + '], 12);\n')
        ip.close()

        # Append tile layer information (map background)
        cmd = 'cat html/tilelayer.html >> ' + filename
        os.system(cmd)

# Function to finalize the HTML file

def close_file(filename):
        ip = open(filename, 'a')
        string9 = "    </script>\n  </body>\n</html>"
        ip.write(string9)
        ip.close()

# Function to create a rectangle on the map representing a colocation facility, with popup details

def create_facility(filename, fac, facility, organisation):
    ip = open(filename, 'a')

    fac_str = str(fac)

    # Extract organization details
    fac_organisation = organisation['name']
    fac_address = organisation['address']
    fac_city = organisation['city']
    fac_country = organisation['country']
    fac_website = organisation['website']

    # Define rectangle bounds around facility (approx. 100m buffer)
    rec_lat1 = str(facilitys_uk[fac_str]['latitude'] + .001)
    rec_lat2 = str(facilitys_uk[fac_str]['latitude'] - .001)
    rec_lon1 = str(facilitys_uk[fac_str]['longitude'] - .001)
    rec_lon2 = str(facilitys_uk[fac_str]['longitude'] + .001)

    # Write Leaflet.js rectangle for facility and bind popup with facility info
    ip.write('      //  Facility ' + fac_str + '\n')
    ip.write('var bounds_' + fac_str + ' = [[' + rec_lat1 + ',' + rec_lon1 + '],[' + rec_lat2 + ',' + rec_lon2 + ']];\n')
    ip.write('var rectangle_' + fac_str + ' = L.rectangle(bounds_' + fac_str + ', {color: "black", fillColor: 0, fillOpacity: 0, weight: 4 }).addTo(map);\n')
    ip.write('rectangle_' + fac_str + '.bindPopup("<b>IXP Facility ' + fac_str + '</b><br />' +
             facilitys_uk[fac_str]['name'] + '<br />' +
             facilitys_uk[fac_str]['address1'] + '<br />Administration by:- <br />' +
             fac_organisation + '<br />' + fac_address + '<br />' + fac_city + '<br />' + fac_country + '<br />' + fac_website + '<br />");\n')

# Helper function to convert a list of dictionaries to a dictionary keyed by 'id'
def convert(lst):
    my_dict = {}
    for l in lst:
        id = l['id']
        my_dict[id] = {key: value for key, value in l.items()}
    return my_dict

# Main logic to generate HTML visualization
if __name__ == "__main__":
    from Htmlcreate15 import Html_Create
    from ripe.atlas.cousteau import ProbeRequest, Traceroute, AtlasSource, AtlasRequest, AtlasCreateRequest
    from datetime import datetime
    import time
    import json 
    import os
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    import great_circle_calculator.great_circle_calculator as gcc
    import prsw
    import ipwhois
    import re
    import ipaddress
    import requests
    from peeringdb import PeeringDB, resource, config

    pdb = PeeringDB()
    pdb.update_all()  # Make sure the local PeeringDB cache is current

    filename = 'web_files_results/uk_facilities.html'
    ripe = prsw.RIPEstat()  # For RIPE data queries (ASN, IP info)
    ripe_url = 'https://rest.db.ripe.net/search.json'

    # Define a dictionary of known remote peering locations (optional mapping aid)
    colocation = {
        'bso1': 'manchester', 'bso2': 'edinburgh', 'bso3': 'london',
        'bics1': 'london', 'epsilon1': 'london',
        'telia1': 'manchester', 'telia2': 'london', 'telia3': 'slough'
    }

    # Define private IP address prefixes (used to exclude local hops)
    local_subnets = [
        '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.',
        '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.',
        *['100.' + str(i) + '.' for i in range(64, 128)]
    ]

    # Load facility data from disk
    with open('peeringdb_test_results/uk_facilities_and_details_to_networks_and_asns.json') as f:
        facilitys_uk = json.load(f)

    # Add a manually discovered facility that wasn't in PeeringDB
    facilitys_uk['8628'] = {
        "org_id": 26163,
        "name": "Datacenta Hosting",
        "address1": "Dorset Innovation Park",
        "address2": "",
        "city": "Winfrith Newburgh",
        "country": "GB",
        "postcode": "DT2 8ZB",
        "latitude": 50.681852,
        "longitude": -2.256535,
        "networks": []
    }

    organisation = {}

    # Start HTML creation
    create_header_html(filename)

    # Iterate through all UK facilities and generate rectangles for each
    for facility in facilitys_uk:
        f = pdb.fetch(resource.Facility, facility)

        organisation['name'] = f[0]['org']['name']
        organisation['address'] = f[0]['org']['address1']
        organisation['city'] = f[0]['org']['city']
        organisation['country'] = f[0]['org']['country']
        organisation['website'] = f[0]['org']['website']

        create_facility(filename, facility, facilitys_uk[facility], organisation)

    # Finalize HTML file
    close_file(filename)
    print('Copy', filename, 'upto web server')
