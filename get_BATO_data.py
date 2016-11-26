# encoding: utf-8
import csv
import subprocess

#on écrase le fichier précédemment créé
fieldnames = ['source','stop_id','latitude','longitude','name']
outfile = 'resultats/BATO.csv'
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#on concatène les fichiers obtenus
#sed pour retirer les headers
#cut pour ne conserver que les premières colonnes
cmd = 'cat resultats/BATO_OSM.csv |sed 1d >> resultats/BATO.csv'
subprocess.call(['/bin/bash', '-i', '-c', cmd])

cmd = 'cat resultats/BATO_GTFS.csv |sed 1d |cut -d , -f 1-5 >> resultats/BATO.csv'
subprocess.call(['/bin/bash', '-i', '-c', cmd])
