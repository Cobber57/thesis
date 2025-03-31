from peeringdb import PeeringDB, resource, config
# Table Names
#peeringdb_network         
#peeringdb_facility          peeringdb_network_contact 
#peeringdb_ix                peeringdb_network_facility
#peeringdb_ix_facility       peeringdb_network_ixlan   
#peeringdb_ixlan             peeringdb_organization    
#peeringdb_ixlan_prefix    

# 
# import django
import peeringdb
import json
import os
from geopy.geocoders import Nominatim
import requests
os.chdir('/home/paul/Documents/UK')
del os 
geolocator = Nominatim(user_agent="p.mccherry@lancaster.ac.uk")

print( 'NOTE BE CAREFUL RUnNING THIS NOW, as I have added 16 facs that couldnt be found by noinatum')
input('See list below')
'''
 "438": {
    "org_id": 782,
    "name": "Synergy House Manchester",
    "address1": "Pencroft Way",
    "address2": "1 Synergy House, Manchester Science Park",
    "city": "Manchester",
    "country": "GB",
    "postcode": "M15 6SY",
    "latitude": 53.462386,
    "longitude": -2.2369371
  },
  "1009": {
    "org_id": 11051,
    "name": "Reliance Skewjack",
    "address1": "B3315, ",
    "address2": "",
    "city": "St Levant",
    "country": "GB",
    "postcode": "TR 19 6NB",
    "latitude": 50.0421534,
    "longitude": -5.660741
  },
  "1027": {
    "org_id": 3844,
    "name": "VIRTUS LONDON1 (Enfield)",
    "address1": "Unit 3, Trade City, Crown Road",
    "address2": "Enfield",
    "city": "London",
    "country": "GB",
    "postcode": "EN1 1TX",
    "latitude": 51.6516657,
    "longitude": -0.0535249
  },
  "1548": {
    "org_id": 8100,
    "name": "NGD Newport",
    "address1": "Celtic Way",
    "address2": "Duffryn",
    "city": "Newport",
    "country": "GB",
    "postcode": "NP10 8BE",
    "latitude": 51.5534127,
    "longitude": -3.0373415
  },
  "1683": {
    "org_id": 24568,
    "name": "ANS - MAN5",
    "address1": "Unit 19 Blackmore Road",
    "address2": "Cobra Court",
    "city": "Manchester",
    "country": "GB",
    "postcode": "M32 0QY",
    "latitude": 53.460558,
    "longitude": -2.3238893
  },
  "1684": {
    "org_id": 24568,
    "name": "ANS - MAN6",
    "address1": "Unit 20a & 20b Blackmore Road",
    "address2": "Cobra Court",
    "city": "Manchester",
    "country": "GB",
    "postcode": "M32 0QY",
    "latitude": 53.460558,
    "longitude": -2.3238893
  },
  "1793": {
    "org_id": 73,
    "name": "Interxion London (Redhill)",
    "address1": "3 Foxboro Business Park",
    "address2": "St. Anne\u2019s Boulevard",
    "city": "Redhill",
    "country": "GB",
    "postcode": "RH1 1AX",
    "latitude": 51.247171071625274, 
    "longitude": -0.15898130608029076
  },
  "1872": {
    "org_id": 9566,
    "name": "Colocker",
    "address1": "Interchange Park",
    "address2": "",
    "city": "Milton Keynes",
    "country": "GB",
    "postcode": "MK16 9PY",
    "latitude": 52.0863864,
    "longitude": -0.7237341
  },
  "2384": {
    "org_id": 1813,
    "name": "aql DC5",
    "address1": "Canon House, Apex Way",
    "address2": "",
    "city": "Leeds",
    "country": "GB",
    "postcode": "",
    "latitude": 53.79243172343359, 
    "longitude": -1.5404289947695775
  },
  "3213": {
    "org_id": 4921,
    "name": "Six Degrees Birmingham Central",
    "address1": "Garrison Technology Park",
    "address2": "Westley Street",
    "city": "Birmingham",
    "country": "GB",
    "postcode": "B9 4ER",
    "latitude": 52.4772548,
    "longitude": -1.876782
  },
  "4798": {
    "org_id": 73,
    "name": "Interxion London (Crawley)",
    "address1": "North Building, Power Avenue",
    "address2": "Manor Royal, Principal Park Campus",
    "city": "Crawley",
    "country": "GB",
    "postcode": "RH10 9BE",
    "latitude": 51.1294884,
    "longitude": -0.1780575
  },
  "5441": {
    "org_id": 16352,
    "name": "Serverfarm LON1 London",
    "address1": "Unit 4, Westgate Industrial Estate",
    "address2": "",
    "city": "Feltham",
    "country": "GB",
    "postcode": "TW14 8RS",
    "latitude": 51.44666085,
    "longitude": -0.4541237779476987
  },
  "8078": {
    "org_id": 12974,
    "name": "Ark Data Centres - Cody Park - A9, A101, A102, A103, A104, A105",
    "address1": "Old Ively Rd",
    "address2": "",
    "city": "Farnborough",
    "country": "GB",
    "postcode": "GU14 OLL",
    "latitude": 51.280921086339156, 
    "longitude": -0.7918778372948029
  },
  "11899": {
    "org_id": 7431,
    "name": "Angel House",
    "address1": "Angel House",
    "address2": "Chester Le Street",
    "city": "Durham",
    "country": "GB",
    "postcode": "DH2 1AQ",
    "latitude": 54.873193900000004,
    "longitude": -1.5862850003348075
  },
  "11978": {
    "org_id": 31498,
    "name": "EXA Edge DC Wherstead",
    "address1": "Park Farm",
    "address2": "",
    "city": "Wherstead",
    "country": "GB",
    "postcode": "IP9 2AF",
    "latitude": 52.0222998,
    "longitude": 1.14246
  },
  "12221": {
    "org_id": 32362,
    "name": "Cloud Innovation Poole Data Center",
    "address1": "Unit 6, The Concept Center",
    "address2": "Innovation Close",
    "city": "Poole",
    "country": "GB",
    "postcode": "BH12 4QD",
    "latitude": 50.7431027,
    "longitude": -1.9529965
  }
  '''


# couldnt get django working (config.yaml, peeringdb.django, virtualenv)and when i use  peeringdb.pythons PDB keeps aacessing the online database which then creates too many requests and 
# I am stopped from accessing the database so have had to resort to using sqlite3 module to access the local sqlite3 file.
# which complicates things but hopefully i can create dictionaries from the sqlite3 databases and just work with them

import sqlite3

pdb = PeeringDB()
# pdb.update_all() # unmark this to update the sqllite3 database with changes
from pprint import pprint
def get_location(address,city,postcode):
    '''
    Example:
    location = geolocator.geocode("Chicago Illinois")
    return:
    Chicago, Cook County, Illinois, United States of America
    location.address    location.altitude   location.latitude   location.longitude  location.point      location.raw
    '''
    mysearch = address+" "+city+" "+postcode
    print(mysearch)
    location = geolocator.geocode(mysearch, timeout=1000)
    return location
def get_coords(street,city,country,postcode):
    street = street.split(' ')
    city = city.split(' ')
    if country == 'GB':
        country = 'United Kingdom'
    country = country.split(' ')
    postcode = postcode.split(' ')
    street_search_string =''
    city_search_string =''
    country_search_string =''
    postcode_search_string =''
    for a in street:
        if street_search_string != '':
            street_search_string = street_search_string +'+'
        street_search_string = street_search_string + a
        print(street_search_string)
    
    for a in city:
        if city_search_string != '':
            city_search_string = city_search_string +'+'
        city_search_string = city_search_string + a
        print(city_search_string)
    for a in country:
        
        if country_search_string != '':
            country_search_string = country_search_string +'+'
        country_search_string = country_search_string + a
        print(country_search_string)
    for a in postcode:
        if postcode_search_string != '':
            postcode_search_string = postcode_search_string +'+'
        postcode_search_string = postcode_search_string + a
        print(postcode_search_string)
    
    
    url = f'https://nominatim.openstreetmap.org/search?street={street_search_string}&city={city_search_string}&country={country_search_string}&postalcode={postcode_search_string}'
    print(url)
    input('wait')
    a = 0
    if a == 0:
        result = requests.get(url=url,)
        print('status_code',result.status_code)
        if result:
            result_text = result.text
            print('TEXT', result_text)
            result_json = result.json()
            print('RESULTS',result_json)
        else:
            print(result.status_code)
        input('wait')
        return result_json
    if a ==1:
        return None

 # read from SQLlite3 database and create UK Internet Exchange Dictionary

def get_ixps():
    con = sqlite3.connect("peeringdb.sqlite3")
    cur = con.cursor()

    #cur.execute("select * from peeringdb_ix where status = 'deleted'")
    #uk_ixs = cur.fetchone()

    

    # get Internet Exchange info
    cur.execute("select * from peeringdb_ix where country = 'GB'")
    uk_ixs = cur.fetchall()
    colnames = cur.description
    #print(colnames)

   



    # con.close()

    uk_ix_dict ={}
    ixp_dict ={}
    number = 0
   
    for ix in uk_ixs:
        number += 1
        # print('\n')
        # print('********* ix', ix,'**************************************\n')
        i = 0
        uk_ix_dict[ix[0]] = {}
        ixp_dict [ix[0]] = {} # this will be the dictionary that is returned and is similar to how pdb formats the dictionary
        ix_id = (ix[0],)
        # get facilities that this ixp is peered at info
        cur.execute('select * from peeringdb_ix_facility where ix_id =?',ix_id) 
        facilities = cur.fetchall()
        
        ixp_dict[ix[0]]["fac_set"] = []
       
        fac_list = []
        for fac in facilities:
            fac_list.append(fac[5])
        ixp_dict[ix[0]]["fac_set"].append(fac_list)
        print('IXP dict fac set is',ixp_dict[ix[0]]["fac_set"])
        # input('WAIT')
        cur.execute('select * from peeringdb_ixlan where ix_id =?',ix_id) 
        ix_lan = cur.fetchall() 
        
        # get lans that belong to this ixp ( I think theres usually only one ixlan but to keep it consistent with PDB I have tuned it into a list of lists)
        ixp_dict[ix[0]]["ixlan_set"] = []       
        for lan in ix_lan:
            lan_list = [lan[0]]
            ixp_dict[ix[0]]["ixlan_set"].append(lan_list)
        
        print(ixp_dict[ix[0]])
        print (ix_lan)



        for column in colnames:
            print (ix[0],ix[i],column[0])
            uk_ix_dict[ix[0]][column[0]] = ix[i]
            i += 1

            '''
            print('this column is',column[0],'and its value is',ix[j])           
            print('this part of the dict is',uk_ix_dict[ix[0]])         
            input('wait')
            '''
        
        ixp_dict[ix[0]]["name"] = [uk_ix_dict[ix[0]]["name"]]
        ixp_dict[ix[0]]["org-id"] = [uk_ix_dict[ix[0]]["org_id"]]
        

        print('\n*******************************************')
        print('Entire dictionary is',uk_ix_dict)
        print('\n*******************************************')
       
       
        
        # get prefixes that belong to this
        cur.execute('select * from peeringdb_ixlan_prefix where ixlan_id =?',ix_id) 
        ix_prefix = cur.fetchall() 
        for prefix in ix_prefix:
            if prefix[1] == 'ok':
                if prefix[6] == 'IPv4':
                    ixp_dict[ix[0]]["ipv4_prefix"] = prefix[7]
                if prefix[6] == 'IPv6':
                    ixp_dict[ix[0]]["ipv6_prefix"] = prefix[7]
        
        # print(ix_prefix) 
        # colnames = cur.description
        # print(colnames)
        
        print('ipx-dict is',ixp_dict)
        
    con.close()
    with open('peeringdb_test_results/uk_ixps.json', 'w') as outfile:
            json.dump(ixp_dict, outfile)
    outfile.close()
    print(number)
    
    
    return ixp_dict

def get_facilities():
    con = sqlite3.connect("peeringdb.sqlite3")
    cur = con.cursor()

    #cur.execute("select * from peeringdb_ix where status = 'deleted'")
    #uk_ixs = cur.fetchone()

    

    # get Internet Exchange info
    cur.execute("select * from peeringdb_facility where country = 'GB'")
    uk_fac = cur.fetchall()
    fac_no=0
    fac_no_none =0
    fac_no_nom = 0
    uk_fac_dict ={}
    uk_fac_dict_none ={}
    for fac in uk_fac:
        uk_fac_dict[fac[0]] = {}
        uk_fac_dict[fac[0]]['org_id'] = fac[19]
        uk_fac_dict[fac[0]]['name'] = fac[13]
        uk_fac_dict[fac[0]]['address1'] = fac[5]
        uk_fac_dict[fac[0]]['address2'] = fac[6]
        uk_fac_dict[fac[0]]['city'] = fac[7]
        uk_fac_dict[fac[0]]['country'] = fac[10]
        uk_fac_dict[fac[0]]['postcode'] = fac[9]
        uk_fac_dict[fac[0]]['latitude'] = fac[11]
        uk_fac_dict[fac[0]]['longitude'] = fac[12]
        fac_no +=1
        
        if fac[11] == None :
            full_address = fac[5]+','+fac[6]+','+fac[7]
            #location = geolocator.geocode(full_address)
            #this_result =get_coords(fac[5],fac[7],fac[10],fac[9])
            location = get_location(fac[5],fac[7],fac[9])

            
            if location != None:
                uk_fac_dict[fac[0]]['latitude'] = location.latitude
                uk_fac_dict[fac[0]]['longitude'] = location.longitude
                fac_no_nom +=1
            else:
                fac_no_none +=1
                uk_fac_dict_none[fac[0]] = {}
                uk_fac_dict_none[fac[0]]['org_id'] = fac[19]
                uk_fac_dict_none[fac[0]]['name'] = fac[13]
                uk_fac_dict_none[fac[0]]['address1'] = fac[5]
                uk_fac_dict_none[fac[0]]['address2'] = fac[6]
                uk_fac_dict_none[fac[0]]['city'] = fac[7]
                uk_fac_dict_none[fac[0]]['country'] = fac[10]
                uk_fac_dict_none[fac[0]]['postcode'] = fac[9]
                uk_fac_dict_none[fac[0]]['latitude'] = fac[11]
                uk_fac_dict_none[fac[0]]['longitude'] = fac[12]
        
    print('Number of facilities is',fac_no)
    print('Number of none facilities is',fac_no_none)
    print('Number of nominatum facilities is',fac_no_nom)
   
    with open('peeringdb_test_results/uk_facilities_new.json', 'w') as outfile:
            json.dump(uk_fac_dict, outfile)
    outfile.close()
    with open('peeringdb_test_results/uk_facilities_none.json', 'w') as outfile:
            json.dump(uk_fac_dict_none, outfile)
    outfile.close()



    con.close()
    print(uk_fac_dict)
    input('wait')

# Return first result of query
#cur.fetchone()

#df = pd.read_sql_query("select * from peeringdb_facility where country = 'GB'", con)
#print(df.head())

#print(peeringdb.get_backend_info()[1])
#n1 = pdb.get(resource.Network, 1)
#print(n1)

if __name__ == "__main__":

    #ix_dict = get_ixps()
    get_facilities()
    input('NOW CREATED A NEW UK_FACILITIES JSON FILE peeringdb_test_results/uk_facilities_new.json AND A NEW UK_ips FILE')

'''
pprint(dir(peeringdb))
'''
'''
• ixlan
• Describes the LAN of an IX
• One IX may have multiple ixlan
• May go away with PeeringDB 3.0
• ixpfx
• Describes the IP range (IPv4 and IPv6) for an ixlan
• One ixlan may have multiple ixpfx, both for IPv4 and IPv6
• netixlan
• Describes the presence of a network at an IX
• netfac
• Describes the presence of a network at a facility
'''
'''
# https://github.com/grizz/pdb-examples
# EXAMPLE SCRIPT lookup network by ASN
#pdb.update_all()
#print ("TAGS")
#pprint(dir(pdb.tags.ix.all))


'''

'Class',
'Facility',
'InternetExchange',
'InternetExchangeFacility',
'InternetExchangeLan',
'InternetExchangeLanPrefix',
'Meta',
'Network',
'NetworkContact',
'NetworkFacility',
'NetworkIXLan',
'OrderedDict',
'Organization',
'RESOURCES_BY_TAG',

'''
ixes = 1
exc = pdb.fetch_all(resource.InternetExchange)
fac_id = pdb.fetch_all(resource.InternetExchangeFacility)
facility = pdb.fetch_all(resource.Facility)
number = 0
for ix in exc:
    number += 1
    if ix['country'] == 'GB':
        
        
        print('===========================================')
        print(ixes,ix['name'], ix['org_id'])

        print(ix)
        print('===========================================')
        #exchanges[ixes] = ix
        ixes += 1
        facs = 1
        input("wait")

        # Print each of the facilities info that belongs to this IX
        for fac in ix['fac_set']:
            print(fac)
            f = pdb.fetch(resource.Facility, fac)
            print('Facility',facs,f)
            
            facs += 1
        ixs = 1

        # print a list of networks that peer at this IX
        for ix_lan in ix['ixlan_set']:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(ix_lan)
            i = pdb.fetch(resource.InternetExchangeLan, ix_lan)
            print('Ix Lan',ixs,i)
            nets = 1
            print(i[0]['net_set'])
            input("wait")

            # Print each networks detailed info at this IX
            for net in i[0]['net_set']:
    
                print('---------------------------------------------------------')
                print(net)
                n = pdb.fetch(resource.Network, net)
                print('Network',nets,n)
                print('---------------------------------------------------------')
                nfacs = 1
                input("wait")
                # print each facility where this network peers
                for nf in n[0]['netfac_set']: # ties the facility into the network
                    print('fffffffffffffffffffffffffffffffffffffffffffffff')
                    print(nf)
                    nfac = pdb.fetch(resource.NetworkFacility, nf)
                    print('Network Facilities',nfacs,nfac)
                    print('ffffffffffffffffffffffffffffffffffffffffffffffff')
                    nfacs += 1
                    
                ixlans = 1
                
                for ixl in n[0]['netixlan_set']: 
                    print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
                    print(ixl)
                    ixlan = pdb.fetch(resource.NetworkIXLan, ixl)
                    print('Network IXLAN',ixlans,ixlan)
                    print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
                    ixlans += 1
                    input("wait")
                nets += 1
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
            ixs += 1

#print(exc[287])
print(fac[0])
'''



        
