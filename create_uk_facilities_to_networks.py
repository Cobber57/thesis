# Reads all networks from PeeringDB and associates them with UK-based
# Internet exchange facilities, enriching each facility with geographic data.
# This mapping is later used to create a geolocated view of ASNs in the UK.

import peeringdb
from peeringdb import PeeringDB, resource
from geopy.geocoders import Nominatim
import ipaddress
import json

# Initialize the PeeringDB API and geolocation service
pdb = PeeringDB()
geolocator = Nominatim(user_agent="aswindow")

# Set country filter to Great Britain
area = 'GB'

# Download all PeeringDB records of interest
networks = pdb.fetch_all(resource.Network)
facilities = pdb.fetch_all(resource.Facility)
netfac = pdb.fetch_all(resource.NetworkFacility)

# Create data structures to hold facility info and mappings
uk_facilitys = {}        # Store GB facilities with full details
uk_asns = []             # List of ASNs peering in GB
fac_list = []            # List of GB facility IDs
nets = {}                # Dictionary mapping each facility to list of ASNs

# Counters for debug
net_n = 0
facs_n = 0

# Iterate over every NetworkFacility entry
for n in netfac:
    if n['country'] == 'GB':  # Only process UK facilities
        net_n += 1
        fac = n['fac_id']
        asn = n['local_asn']
        net = n['net_id']

        # If this is the first time encountering this facility, fetch full data
        if fac not in uk_facilitys:
            f = pdb.fetch(resource.Facility, fac)
            uk_facilitys[fac] = {}
            nets[fac] = []
            facs_n += 1

            # Extract facility details into dictionary
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

            # If no coordinates, use geopy to fetch approximate location
            if uk_facilitys[fac]['latitude'] is None:
                full_address = f"{f[0]['address1']},{f[0]['address2']},{f[0]['city']}"
                location = geolocator.geocode(full_address)
                if location is not None:
                    uk_facilitys[fac]['latitude'] = location.latitude
                    uk_facilitys[fac]['longitude'] = location.longitude
                else:
                    # Manually assign fallback coordinates for known problem entries
                    manual_coords = {
                        1548: (51.5548, -3.0382),
                        438: (53.4617, -2.2384),
                        1027: (51.6523, -0.0550),
                        1684: (53.4608, -2.3238),
                        1793: (51.2477, -0.1571),
                        2384: (53.7924, -1.5404),
                        3213: (52.4773, -1.8771),
                        5441: (51.4468, -0.4542)
                    }
                    if fac in manual_coords:
                        uk_facilitys[fac]['latitude'], uk_facilitys[fac]['longitude'] = manual_coords[fac]
                    else:
                        print(f"Missing coordinates for facility {fac}: {uk_facilitys[fac]}")
                        input('wait')

        # Track ASN and Network for this facility
        if asn not in uk_asns:
            uk_asns.append(asn)
        nets[fac].append(net)
        nets[fac].append(asn)
        uk_facilitys[fac]['networks'] = nets[fac]

        # Debug output
        print('Number of facilities =', len(uk_facilitys), facs_n)
        print('List of facilities =', len(fac_list), fac_list)
        print('Number of unique ASNs =', len(uk_asns))

# Optionally write results to disk
# with open('peeringdb_test_results/uk_facilities_and_details_to_networks_and_asns_new.json', 'w') as outfile:
#     json.dump(uk_facilitys, outfile)
