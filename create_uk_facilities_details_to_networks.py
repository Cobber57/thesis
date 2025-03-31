# This script queries the PeeringDB database to find all UK-based facilities
# and networks that peer at those facilities. It builds a structured dictionary
# of facilities, each containing geolocation and organizational metadata, as well
# as the list of networks and ASNs associated with them.

import peeringdb
from pprint import pprint
import django
from peeringdb import PeeringDB, resource, config
from geopy.geocoders import Nominatim
import ipaddress
import json

# Initialize geolocation service
geolocator = Nominatim(user_agent="aswindow")

# Connect to the PeeringDB API
pdb = peeringdb.PeeringDB()

# Set the target country
area = 'GB'

# Fetch data from PeeringDB
networks = pdb.fetch_all(resource.Network)
facility = pdb.fetch_all(resource.Facility)
netfac = pdb.fetch_all(resource.NetworkFacility)

# Initialize data structures
uk_facilitys = {}
uk_asns = []
fac_list = []
nets = {}
net_n = 0
facs_n = 0

# Loop through all NetworkFacility entries and filter for UK-based facilities
for n in netfac:
    if n['country'] == 'GB':
        net_n += 1
        fac = n['fac_id']
        asn = n['local_asn']
        net = n['net_id']

        # If this facility hasn't been seen before, fetch its metadata
        if fac not in uk_facilitys:
            f = pdb.fetch(resource.Facility, fac)
            uk_facilitys[fac] = {}
            nets[fac] = []
            facs_n += 1

            # Store facility metadata
            uk_facilitys[fac]['org_id'] = f[0]['org_id']
            uk_facilitys[fac]['name'] = f[0]['name']
            uk_facilitys[fac]['address1'] = f[0]['address1']
            uk_facilitys[fac]['address2'] = f[0]['address2']
            uk_facilitys[fac]['city'] = f[0]['city']
            uk_facilitys[fac]['country'] = f[0]['country']
            uk_facilitys[fac]['postcode'] = f[0]['zipcode']
            uk_facilitys[fac]['latitude'] = f[0]['latitude']
            uk_facilitys[fac]['longitude'] = f[0]['longitude']
            fac_list.append(fac)

            # If coordinates are missing, try to geocode them from the address
            if uk_facilitys[fac]['latitude'] is None:
                full_address = uk_facilitys[fac]['address1'] + ',' + uk_facilitys[fac]['address2'] + ',' + uk_facilitys[fac]['city']
                location = geolocator.geocode(full_address)
                if location:
                    uk_facilitys[fac]['latitude'] = location.latitude
                    uk_facilitys[fac]['longitude'] = location.longitude
                else:
                    # Manual override for known facilities without geolocation
                    manual_coords = {
                        1548: (51.5548, -3.0382),
                        438: (53.461739, -2.238477),
                        1027: (51.652331, -0.055062),
                        1684: (53.460799, -2.323801),
                        1793: (51.247689, -0.157146),
                        2384: (53.792418, -1.540472),
                        3213: (52.477300, -1.877104),
                        5441: (51.446798, -0.454169)
                    }
                    if fac in manual_coords:
                        uk_facilitys[fac]['latitude'], uk_facilitys[fac]['longitude'] = manual_coords[fac]
                    else:
                        print('OOps no coordinates')
                        print(fac, uk_facilitys[fac])
                        input('wait')

        # Track unique ASNs
        if asn not in uk_asns:
            uk_asns.append(asn)

        # Append the network and ASN to the facility
        nets[fac].append(net)
        nets[fac].append(asn)
        uk_facilitys[fac]['networks'] = nets[fac]

        # Print progress
        print('number of facilities = ', len(uk_facilitys), facs_n)
        print('length', len(fac_list), fac_list)
        print('number of asns/networks = ', len(uk_asns))

# Optional: Write the full facility data to a JSON file
# with open('peeringdb_test_results/uk_facilities_and_details_to_networks_and_asns_new.json', 'w') as outfile:
#     json.dump(uk_facilitys, outfile)
