# encoding: utf-8
import csv
import subprocess
import zipfile
import os
import codecs
import pandas as pd

#on écrase le fichier précédemment créé
fieldnames = ['source','stop_id','latitude','longitude','stop_name']
outfile = 'resultats/BATO_GTFS.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#on lit le fichier csv contenant les liens de téléchargements des GTFS
with open('sources_GTFS.csv', 'r') as f:
    dictReader = csv.DictReader(f)
    for a_GTFS in dictReader:
        #on télécharge le GTFS
        subprocess.call(['wget', '-nv', '--output-document=GTFS.zip', a_GTFS['Download']])

        #on extrait le fichier stops.txt de ce GTFS
        stops_from_GTFS = []
        with zipfile.ZipFile('GTFS.zip') as zf:
            stops_file = zf.open('stops.txt')
            stops_data = pd.read_csv(stops_file)
            stops_data["location_type"] = stops_data["location_type"].fillna(0)
            stops_count_before = len(stops_from_GTFS)
            for a_stop in stops_data.iterrows():
                if a_stop[1]['location_type'] == 0 : #on ne conserve que les points d'arrêts
                    stop = {}
                    stop['source'] = "opendata_GTFS_" + a_GTFS['ID']
                    stop['stop_id'] = a_stop[1]['stop_id']
                    stop['longitude'] = a_stop[1]['stop_lon']
                    stop['latitude'] = a_stop[1]['stop_lat']
                    stop['stop_name'] = a_stop[1]['stop_name']
                    stops_from_GTFS.append(stop)
            print("{} : {} stops loaded ({})".format(
                a_GTFS['ID'],
                len(stops_from_GTFS) - stops_count_before,
                a_GTFS['Description']
            ))
        #on supprime les fichiers temporaires
        os.remove('GTFS.zip')

        #on persiste les infos (en csv par exemple)
        with open(outfile, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            for a_row in stops_from_GTFS:
                writer.writerow(a_row)
