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

#on télécharge le fichier OSM France
cmd = 'wget http://download.geofabrik.de/europe/france-latest.osm.pbf'
# subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on extrait les arrêts bien taggés d'après le nouveau schéma de transport public
cmd = 'osmosis --read-pbf file="france-latest.osm.pbf" --nkv keyValueList="public_transport.platform" --write-pbf platform.osm.pbf'
#subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on extrait les arrêts de bus taggés à l'ancienne
cmd = 'osmosis --read-pbf file="france-latest.osm.pbf" --nkv keyValueList="highway.bus_stop" --write-pbf bus.osm.pbf'
#subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on extrait les arrêts de tramway taggés à l'ancienne
cmd = 'osmosis --read-pbf file="france-latest.osm.pbf" --nkv keyValueList="railway.tram_stop" --write-pbf tram.osm.pbf'
#subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on fusionne les extractions précédentes
cmd = 'osmosis --read-pbf platform.osm.pbf --read-pbf tram.osm.pbf --read-pbf bus.osm.pbf --merge --merge --write-pbf public_transport_stops.osm.pbf'
#subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on transforme en CSV détaillé
cmd = 'osmconvert public_transport_stops.osm.pbf --csv="@oname @id @lat @lon name railway highway public_transport" --csv-headline --csv-separator="," -o=BATO_OSM_full.csv'
#subprocess.call(['/bin/bash', '-i', '-c', cmd])

#on ne conserve que les colonnes utiles
stops_from_OSM = []
with open('BATO_OSM_full.csv', 'r') as g:
    stop_reader = csv.DictReader(g)
    for a_stop in stop_reader:
        a_stop['source'] = "OpenStreetMap"
        a_stop['longitude'] = a_stop['@lon']
        a_stop['latitude'] = a_stop['@lat']
        a_stop['stop_id'] = a_stop['@oname'] + a_stop['@id']
        stops_from_OSM.append(a_stop)

stop_to_persist = [ dict((k,  stop.get(k, None)) for k in fieldnames) for stop in stops_from_OSM]
with open(outfile, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for a_row in stop_to_persist:
        writer.writerow(a_row)

#on nettoie le répertoire courant
subprocess.call(['rm', 'france-latest.osm.pbf'])
subprocess.call(['rm', 'public_transport_stops.osm.pbf'])
subprocess.call(['rm', 'platform.osm.pbf'])
subprocess.call(['rm', 'bus.osm.pbf'])
subprocess.call(['rm', 'tram.osm.pbf'])
subprocess.call(['rm', 'BATO_OSM_full.csv'])
