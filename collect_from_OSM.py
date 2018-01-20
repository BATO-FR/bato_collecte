# encoding: utf-8
import csv
import time
import subprocess

#on écrase le fichier précédemment créé
fieldnames = ['source','stop_id','latitude','longitude','name']
outfile = 'resultats/BATO_OSM.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#on ne conserve que les colonnes utiles
stops_from_OSM = []
with open('BATO_OSM_full.csv', 'r') as g:
    stop_reader = csv.DictReader(g)
    for a_stop in stop_reader:
        stop = {}
        stop['source'] = "OpenStreetMap"
        stop['stop_id'] = a_stop['@oname'] + a_stop['@id']
        stop['longitude'] = a_stop['@lon']
        stop['latitude'] = a_stop['@lat']
        stop['name'] = a_stop['name']
        stops_from_OSM.append(stop)

with open(outfile, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for a_row in stops_from_OSM:
        writer.writerow(a_row)
