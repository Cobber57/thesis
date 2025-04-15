OU OWN KEY# -------------------------------------------
# SCRIPT PURPOSE:
# -------------------------------------------
# This script automates the creation of traceroute measurements between all active 
# RIPE Atlas probes located in the UK. It helps build a comprehensive dataset 
# showing how packets travel within the UK Internet infrastructure. The measurements 
# are stored for later use in mapping tools that support fine-grained Internet 
# topology analysis (as explored in Chapters 4 and 5 of the thesis).
# 
# -------------------------------------------

from ripe.atlas.cousteau import ProbeRequest, Traceroute, AtlasSource, AtlasRequest, AtlasCreateRequest
from datetime import datetime
import time
import json 
import os
import csv

# -------------------------------------------
# RIPE Atlas API Key (private key to authenticate requests)
# -------------------------------------------
ATLAS_API_KEY = "Get-Your_OWN-KEY"

# -------------------------------------------
# Output and input files
# -------------------------------------------
filename = 'measurements/all_uk_probes.json'        # Stores measurement metadata
target_list = 'target_list.txt'                     # Tracks which targets have been measured
f = open(target_list, 'r')                          # Load targets that are already measured
ip_list = [ip.strip() for ip in f]                  # List of IPs to avoid repeating
f.close()

# -------------------------------------------
# Query RIPE Atlas for all active UK probes
# -------------------------------------------
filters = {"country_code": "gb", "status": "1"}     # Only use UK probes that are currently online
probes = ProbeRequest(**filters)

probe_list = []     # List of probe IDs
uk_probes = {}      # Dictionary of probe ID -> metadata

# -------------------------------------------
# Populate local dictionary with probe IPs and coordinates
# -------------------------------------------
for t_probe in probes:
    probe_list.append(str(t_probe["id"]))
    uk_probes[t_probe["id"]] = {
        "address": t_probe["address_v4"],
        "coordinates": t_probe["geometry"]["coordinates"]
    }

not_work = 0     # Track failures
done = 0         # Count of successful measurements created

# -------------------------------------------
# Iterate through each probe and create traceroute measurements from all others to it
# -------------------------------------------
for target_probe in uk_probes:

    # Limit for testing / batching
    if done == 31:
        break

    source_list = probe_list.copy()
    source_list.remove(str(target_probe))                # Remove the target from the source list
    source_string = ','.join(source_list)                # Convert to comma-separated string

    target = uk_probes[target_probe]['address']

    if target_probe == 55:                               # Skip problematic probe (if known)
        continue

    if target in ip_list:                                # Skip probes already measured
        print('target is in already done list', target)
        continue

    try:
        # -------------------------------------------
        # Define the traceroute measurement
        # -------------------------------------------
        traceroute = Traceroute(
            af=4,                             # IPv4 measurement
            target=target,                   # Target IP address (UK probe)
            description="FULL UK PROBE traceroute",
            protocol="ICMP"                  # Use ICMP traceroute
        )

        # -------------------------------------------
        # Define the measurement sources (all other UK probes)
        # -------------------------------------------
        source = AtlasSource(
            type="probes",
            value=source_string,
            requested=650                   # Number of probes requested to participate
        )

        # -------------------------------------------
        # Submit measurement request to RIPE Atlas
        # -------------------------------------------
        atlas_request = AtlasCreateRequest(
            key=ATLAS_API_KEY,
            measurements=[traceroute],
            sources=[source],
            is_oneoff=True                  # One-time measurement (not recurring)
        )

        (is_success, response) = atlas_request.create()
        print(is_success, response)

        # -------------------------------------------
        # Save successful measurement result
        # -------------------------------------------
        uk_probes[target_probe]['measurement'] = response['measurements'][0]
        
        # Save JSON result for this probe
        with open(filename, 'a') as outfile:
            json.dump(uk_probes[target_probe], outfile)

        # Append target IP to list to prevent future duplication
        with open(target_list, "a") as f:
            f.write('\n' + str(target))

        done += 1
        input('wait', done)

    except:
        # -------------------------------------------
        # Handle errors and log probes that failed
        # -------------------------------------------
        not_work += 1
        print('target is but didnt work', target_probe, target, not_work)
        with open('target_list_not_work.txt', "a") as f:
            f.write('\n' + str(target_probe))
