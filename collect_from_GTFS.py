# encoding: utf-8
import csv
import subprocess
import zipfile
import os

#on écrase le fichier précédemment créé
fieldnames = ['source','stop_id','latitude','longitude','stop_name','stop_desc','stop_code']
outfile = 'resultats/BATO_GTFS.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#on lit le fichier csv contenant les liens de téléchargements des GTFS
with open('sources_GTFS.csv', 'r') as f:
    dictReader = csv.DictReader(f)
    for a_GTFS in dictReader:
        if a_GTFS['active'] == "yes":
            print(a_GTFS['Description'])

            #on télécharge le GTFS
            subprocess.call(['wget', '-nv', '--output-document=GTFS.zip', a_GTFS['Download']])

            stops_from_GTFS = []

            #on extrait le fichier stops.txt de ce GTFS
            zf = zipfile.ZipFile('GTFS.zip')
            zf.extract('stops.txt')
            with open('stops.txt', 'r') as g:
                stop_reader = csv.DictReader(g)
                for a_stop in stop_reader:
                    if a_stop['location_type'] == '0' : #on ne conserve que les points d'arrêts
                        a_stop['source'] = "opendata_GTFS_" + a_GTFS['ID']
                        a_stop['longitude'] = a_stop['stop_lon']
                        a_stop['latitude'] = a_stop['stop_lat']
                        stops_from_GTFS.append(a_stop)


            #on persiste les infos (en csv par exemple)

            stop_to_persist = [ dict((k,  stop.get(k, None)) for k in fieldnames) for stop in stops_from_GTFS]
            with open(outfile, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for a_row in stop_to_persist:
                    writer.writerow(a_row)

            #on supprime les fichiers temporaires
            subprocess.call(['rm', 'GTFS.zip'])
            subprocess.call(['rm', 'stops.txt'])
