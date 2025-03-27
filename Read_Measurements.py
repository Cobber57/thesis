import pprint
import os
import time
import collections
import sys
from geopy.distance import geodesic
import xlsxwriter

if __name__ == "__main__":
    import json 
    from ripe.atlas.cousteau import Measurement, AtlasResultsRequest

    # Change working directory to the local folder where the measurement file is stored
    os.chdir('/home/paul/Documents/UK')

    # Load measurement metadata from a previously saved JSON file created using Create_Measurements.py
    with open("latest_measures.json") as file:
        measurements = json.load(file)

    # Dictionary to store all parsed results
    targets = {}

    # Loop through each target probe in the measurements list
    for target_probe in measurements:
        print('Target probe is', target_probe)
        this_measurement_id = measurements[target_probe]['measurement']
        
        # Request traceroute results from the RIPE Atlas API
        kwargs = { "msm_id": this_measurement_id }
        is_success, results = AtlasResultsRequest(**kwargs).create()

        # Prepare dictionary for this measurement
        targets[this_measurement_id] = {
            'target_probe': target_probe,
            'target_address': measurements[target_probe]['address'],
            'target_coordinates': measurements[target_probe]['coordinates'],
            'results': {}
        }

        # Loop over traceroutes received for this measurement
        for traceroute in results:
            source_probe = int(traceroute['prb_id'])  # Source probe ID
            targets[this_measurement_id]['results'][source_probe] = {
                'source_address': traceroute['src_addr'],
                'source_coordinates': measurements[str(source_probe)]['coordinates'],
                'hops': {}
            }

            # Parse hop-by-hop results
            for hop in traceroute['result']:
                h = hop['hop']
                targets[this_measurement_id]['results'][source_probe]['hops'][h] = {}

                # For each hop, extract the lowest RTT of the available attempts
                rtt = 100  # Initialise with high RTT
                for tr in hop['result']:
                    try:
                        if tr['rtt'] < rtt:
                            rtt = tr['rtt']
                            ip_from = tr['from']
                    except:
                        print('Hop has no RTT value or malformed data.')

                # Save best RTT and source IP for this hop
                targets[this_measurement_id]['results'][source_probe]['hops'][h]['rtt'] = rtt
                targets[this_measurement_id]['results'][source_probe]['hops'][h]['ip_from'] = ip_from

            # Save final RTT and max hop count for the route
            targets[this_measurement_id]['results'][source_probe]['final_rtt'] = rtt
            targets[this_measurement_id]['results'][source_probe]['max_hops'] = h

            # Calculate maximum fibre length from RTT (assuming ~60% speed of light in fibre)
            fibre_max_length = (rtt / 2) * ((0.6 * 300000) / 1000)  # in kilometers
            targets[this_measurement_id]['results'][source_probe]['fibre_length'] = fibre_max_length

            # Calculate geodesic (real-world) distance between source and target
            source_coords = targets[this_measurement_id]['results'][source_probe]['source_coordinates']
            dest_coords = targets[this_measurement_id]['target_coordinates']
            distance = float(str(geodesic(source_coords, dest_coords)).split(' ')[0])
            targets[this_measurement_id]['results'][source_probe]['geodistance_to_target'] = distance

            # Diagnostic printout for verification
            print(rtt, fibre_max_length, source_coords, dest_coords, distance)
            print(f"Actual distance from source probe {source_probe} to target probe {target_probe} is {distance} km")
            print(f"RTT-based maximum distance is ~{fibre_max_length:.2f} km")

    # Save processed results to a JSON file
    with open("results/targetslatest.json", 'w') as outfile:
        json.dump(targets, outfile)

    # Create Excel workbook to store analysis results
    workbook = xlsxwriter.Workbook('results/resultslatest.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.set_column(1, 1, 15)

    # Write column headers
    worksheet.write('A1', 'Target Probe', bold)
    worksheet.write('B1', 'Source Probe', bold)
    worksheet.write('C1', 'RTT (ms)', bold)
    worksheet.write('D1', 'Hops', bold)
    worksheet.write('E1', 'Fibre_max_length (km)', bold)
    worksheet.write('F1', 'Geo Distance (km)', bold)
    worksheet.write('G1', 'Error Margin', bold)
    worksheet.write('H1', 'Avg_ms_Hop', bold)
    worksheet.write('I1', 'Avg_km_ms', bold)

    # Optional reverse-path analysis columns
    worksheet.write('K1', 'Target Probe', bold)
    worksheet.write('L1', 'Source Probe', bold)
    worksheet.write('M1', 'RTT (ms)', bold)
    worksheet.write('N1', 'Hops', bold)
    worksheet.write('O1', 'Fibre_max_length (km)', bold)
    worksheet.write('P1', 'Geo Distance (km)', bold)
    worksheet.write('Q1', 'Error Margin', bold)
    worksheet.write('R1', 'Avg_ms_Hop', bold)
    worksheet.write('S1', 'Avg_km_ms', bold)

    # Populate Excel rows
    row = 1
    col = 0
    count = 0

    for measurement in targets:
        target_probe = targets[measurement]['target_probe']
        worksheet.write_string(row, col, target_probe)

        for source_probe in targets[measurement]['results']:
            result = targets[measurement]['results'][source_probe]

            # Write measurement statistics
            worksheet.write_string(row, col + 1, str(source_probe))
            rtt = round(result['final_rtt'], 2)
            hops = round(result['max_hops'], 2)
            fibre_length = round(result['fibre_length'], 2)
            geo_distance = round(result['geodistance_to_target'], 2)

            worksheet.write_number(row, col + 2, rtt)
            worksheet.write_number(row, col + 3, hops)
            worksheet.write_number(row, col + 4, fibre_length)
            worksheet.write_number(row, col + 5, geo_distance)

            error_margin = fibre_length / geo_distance if geo_distance > 0 else 0
            avg_ms_per_hop = rtt / hops if hops > 0 else 0
            avg_km_per_ms = geo_distance / rtt if rtt > 0 else 0

            worksheet.write_number(row, col + 6, error_margin)
            worksheet.write_number(row, col + 7, avg_ms_per_hop)
            worksheet.write_number(row, col + 8, avg_km_per_ms)

            # Reverse path check
            col = 10
            for m in targets:
                if targets[m]['target_probe'] == str(source_probe):
                    for t in targets[m]['results']:
                        if str(t) == target_probe:
                            rev_result = targets[m]['results'][t]
                            worksheet.write_string(row, col, targets[m]['target_probe'])
                            worksheet.write_string(row, col + 1, str(t))

                            rtt_rev = round(rev_result['final_rtt'], 2)
                            hops_rev = round(rev_result['max_hops'], 2)
                            fibre_length_rev = round(rev_result['fibre_length'], 2)
                            geo_distance_rev = round(rev_result['geodistance_to_target'], 2)
                            error_margin_rev = fibre_length_rev / geo_distance_rev if geo_distance_rev > 0 else 0
                            avg_ms_per_hop_rev = rtt_rev / hops_rev if hops_rev > 0 else 0
                            avg_km_per_ms_rev = geo_distance_rev / rtt_rev if rtt_rev > 0 else 0

                            worksheet.write_number(row, col + 2, rtt_rev)
                            worksheet.write_number(row, col + 3, hops_rev)
                            worksheet.write_number(row, col + 4, fibre_length_rev)
                            worksheet.write_number(row, col + 5, geo_distance_rev)
                            worksheet.write_number(row, col + 6, error_margin_rev)
                            worksheet.write_number(row, col + 7, avg_ms_per_hop_rev)
                            worksheet.write_number(row, col + 8, avg_km_per_ms_rev)

            row += 1
            col = 0
            count += 1

    print(f"Processed {count} probe pairs.")
    workbook.close()
