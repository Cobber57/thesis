# TODO REMOVE The Safeguard before running again (dont want to create more unneccessary traceroute on ATLAS) at line 94
# TODO Set the probes_measurement_id to the emasurement containg the probes you want to use
# TODO Change the filename below


from datetime import datetime
import json 
import os




# Gets the required measuremnt from RIPE ATLAS and creates the initial dictionary file 

# info from https://ripe-atlas-cousteau.readthedocs.io/_/downloads/en/latest/pdf/
from ripe.atlas.cousteau import Ping, Traceroute, AtlasSource, AtlasRequest, AtlasCreateRequest, AtlasLatestRequest, Probe, Measurement
# Sagans sole purpose is to make RIPE Atlas measurements manageable from within Python.
# https://ripe-atlas-sagan.readthedocs.io/en/latest/use.html#how-to-use-this-library
# Attributes and Methods at https://ripe-atlas-sagan.readthedocs.io/en/latest/types.html



#from ripe.atlas.sagan import Result, TracerouteResult
# Opensource Geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
# A Python library to gather IP address details (ASN, prefix, resource holder, reverse DNS) using the RIPEStat API,
# with a basic cache to avoid flood of requests and to enhance performances. https://pypi.org/project/ipdetailscache/
#from pierky.ipdetailscache import IPDetailsCache
#cache = IPDetailsCache()
#cache.UseIXPs()
#r = cache.GetIPInformation( "193.0.6.139" ) # example use
#print (r)
# target_address = "90 Oxford Street, Randburg"   # sample target address
# Discover the geo cordinates of the target location
#location = geolocator.geocode(target_address)
#print(location)
#latitude = location.latitude
#longitude = location.longitude
#print ("lat is ", location.latitude)
#print ("lon is ", location.longitude)
        
ATLAS_API_KEY = "6f0e691d-056c-497d-9f5b-2297e970ec60"
traceroute_dict = {}                                        # initialis the measuretments dictionary
measurements_list = [49306015,]                               # initialise the measurements list
#from html_create import Html_Create 

#probes = ['178.62.103.82',1000130, '81.187.145.168', 999999,'185.38.36.40', 1000222]



# 

# Get a list of the probes to be used, easiset to get list from first measurement which used all probes in uk.

for measurement in measurements_list:                       # Its unlikely I will ever use more than 1 measurement but just in case
    m = Measurement(id=measurement)                         # get metadata for this measurement
    kwargs = {
    "msm_id": measurement,    
    #"start": datetime(2015, 05, 19), # just testing date filtering
    #"stop": datetime(2015, 05, 20),  # just testing date filtering
    #"probe_ids": [1000070]  # the first probe in the measurement
    }
    is_success, results = AtlasLatestRequest(**kwargs).create()
probes =[]
measurements = []
print(results)
input('wait for results')

print('results type is',type(results))
for probe in results:
    print('PROBE is', probe)
    probes.append(probe['from'] )
    probes.append(probe['prb_id'] )
    
    print ('PROBES is',probes)

input('wait for probes') 

measurement_list = '/home/paul/Documents/UK/measurements/all_uk_probes.json'
f =  open (measurement_list,'r')  
ip_list = []
measure_dict = {}
for ip_row in f:
    ip_r = ip_row.split('\n')[0]
    print('IP_row is',ip_r)
    print('type ip is', type(ip))
    ip = ip_r.split('"')[3]
    print('IP is',ip)
    i = 0
    for this_ip in probes[::2]:
        print('THISIP is',this_ip,type(this_ip))
        print('IP is',ip,type(ip))
        input('wait')    
        if ip == this_ip:
            print (this_ip,probes[i])
            this_probe = probes[i+1]
            print(this_probe)
            print('YES')
            address = ip
            c = ip_r.split('[')[1].split(']')[0]
            coordinates1 = float(c.split(',')[0])
            coordinates2 = float(c.split(',')[1])
            coordinates_list = []
            coordinates_list.append(coordinates1)
            coordinates_list.append(coordinates2)

            measure = int(ip_r.split('"')[8].split(': ')[1].split('}')[0])
            measure_dict[this_probe] = {}
            measure_dict[this_probe]['address'] = address
            measure_dict[this_probe]['coordinates'] = coordinates_list
            measure_dict[this_probe]['measurement'] = measure
            print(measure_dict)
            #input('wait')
        i+=2
    #print('IP list is',ip_list)
    #input('wait')

f.close()

print(measure_dict)
input('wait')
filename = '/home/paul/Documents/UK/measurements/allnew_uk_probes.json'

with open(filename, 'w') as outfile:
    json.dump(measure_dict, outfile)

