#!/usr/bin/env python
# This script reads UK facilities, extracts location and metadata, and creates an interactive HTML map.
# It highlights Internet Exchange Points (IXPs) and colocation facilities, drawing bounding rectangles around them.
# Author: Paul McCherry, created in support of RIPE Atlas measurement visualization and infrastructure analysis

# Utility function to convert a list of dictionaries into a dictionary of dictionaries keyed by 'id'
def convert(lst):
    my_dict = {}
    for l in lst:
        id = l['id']
        my_dict[id] = {}
        for key, value in l.items():
            my_dict[id][key] = value
    return my_dict

# Function to write the initial parts of the HTML page, including Leaflet map zoom and tile layer setup
def create_header_html(filename):
    central_lon = -2.23
    central_lat = 52.369

    cmd = 'cp html/head.html ' + filename
    cmd2 = 'chmod 766 ' + filename

    os.system(cmd)
    os.system(cmd2)

    ip = open(filename, 'a')
    ip.write(str(central_lat) + ", " + str(central_lon) + '], 12);\n')
    ip.close()

    # Append tile layer configuration from static file
    cmd = 'cat html/tilelayer.html >> ' + filename
    os.system(cmd)

# Appends closing tags to the HTML file to finish the document

def close_file(filename):
    ip = open(filename, 'a')
    string9 = "    </script>\n  </body>\n</html>"
    ip.write(string9)
    ip.close()

# Draws a rectangle on the map around a facility and adds a popup with detailed information

def create_facility(filename, fac, facility, organisation):
    ip = open(filename, 'a')

    string6 = 'var bounds_'
    stringa = 'var rectangle_'
    stringb = ' = L.rectangle(bounds_'
    stringc = ', {color: "black", fillColor: 0, fillOpacity: 0, weight: 4 }).addTo(map);\n'
    string4 = 'rectangle_'
    string4a = '.bindPopup("<b>IXP '
    string5 = '</b><br /> ");\n'

    fac_str = str(fac)
    fac_organisation = organisation['name']
    fac_address = organisation['address']
    fac_city = organisation['city']
    fac_country = organisation['country']
    fac_website = organisation['website']

    # Define rectangle boundaries for the facility on the map
    rec_lat1 = str(facilitys_uk[fac_str]['latitude'] + .001)
    rec_lat2 = str(facilitys_uk[fac_str]['latitude'] - .001)
    rec_lon1 = str(facilitys_uk[fac_str]['longitude'] - .001)
    rec_lon2 = str(facilitys_uk[fac_str]['longitude'] + .001)

    ip.write('      //  Facility ' + fac_str + '\n')
    ip.write(string6 + fac_str + ' = [[' + rec_lat1 + ',' + rec_lon1 + '],[' + rec_lat2 + ',' + rec_lon2 + ']];\n')
    ip.write(stringa + fac_str + stringb + fac_str + stringc)

    # Create popup content
    ip.write(string4 + fac_str + string4a +
             ' Facility ' + fac_str + "<br />" +
             facilitys_uk[fac_str]['name'] + "<br />" +
             facilitys_uk[fac_str]['address1'] + "<br />" +
             ' Administration by:- <br />' +
             fac_organisation + '<br />' +
             fac_address + '<br />' +
             fac_city + '<br />' +
             fac_country + '<br />' +
             fac_website + string5)

# Main script block
if __name__ == "__main__":
    import os
    import json
    import ipaddress
    import requests
    from geopy.geocoders import Nominatim
    from peeringdb import PeeringDB, resource

    pdb = PeeringDB()
    pdb.update_all()  # Sync local DB with PeeringDB servers

    filename = 'web_files_results/uk_facilities.html'

    # Load UK facilities with extra detail from PeeringDB
    with open('peeringdb_test_results/uk_facilities_and_details_to_networks_and_asns.json') as f:
        facilitys_uk = json.load(f)

    # Add manually-discovered facility that is not in PeeringDB
    facilitys_uk['8628'] = {
        "org_id": 26163,
        "name": 'Datacenta Hosting',
        "address1": "Dorset Innovation Park",
        "address2": "",
        "city": "Winfrith Newburgh",
        "country": "GB",
        "postcode": "DT2 8ZB",
        "latitude": 50.681852,
        "longitude": -2.256535,
        "networks": []
    }

    # Start building the HTML map
    create_header_html(filename)

    # Extract metadata about each facility and draw it on the map
    for facility in facilitys_uk:
        f = pdb.fetch(resource.Facility, facility)
        organisation = {
            'name': f[0]['org']['name'],
            'address': f[0]['org']['address1'],
            'city': f[0]['org']['city'],
            'country': f[0]['org']['country'],
            'website': f[0]['org']['website']
        }
        create_facility(filename, facility, facilitys_uk[facility], organisation)

    # Finish HTML output
    close_file(filename)
    print('Copy', filename, 'upto web server')
