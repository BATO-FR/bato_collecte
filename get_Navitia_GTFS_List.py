# encoding: utf-8
import csv
import requests

navitia_sources = [
    "https://navitia.opendatasoft.com/explore/dataset/fr-se/download/?format=json&timezone=Europe/Berlin",
    "https://navitia.opendatasoft.com/explore/dataset/fr-sw/download/?format=json&timezone=Europe/Berlin",
    "https://navitia.opendatasoft.com/explore/dataset/fr-ne/download/?format=json&timezone=Europe/Berlin",
    "https://navitia.opendatasoft.com/explore/dataset/fr-nw/download/?format=json&timezone=Europe/Berlin"
]

gtfs_sources = []
for source in navitia_sources:
    json_list = requests.get(source).json()
    for dataset in json_list:
        if dataset['fields']['type_file'] != "provider" : continue
        if dataset['fields']['format'] != "GTFS" : continue
        gtfs = {}
        gtfs["ID"] = dataset['fields']["id"]
        gtfs["Licence"] = dataset['fields']["licence"]
        gtfs["Source link"] = dataset['fields']["source_link"]
        gtfs["Description"] = dataset['fields']["description"]
        gtfs["Download"] = "https://navitia.opendatasoft.com/api/datasets/1.0/{}/images/{}".format(
            dataset["datasetid"],
            dataset["fields"]["download"]["id"]
        )
        gtfs_sources.append(gtfs)
# on ajoute le jeu de données du STIF :
gtfs = {}
gtfs["ID"] = "fr-idf-OIF"
gtfs["Licence"] = "ODbL"
gtfs["Source link"] = "http://opendata.stif.info/explore"
gtfs["Description"] = "Transport in Paris and Suburb"
gtfs["Download"] = "https://navitia.opendatasoft.com/api/datasets/1.0/fr-idf/images/14bd1111dd3d3e845924bb0876e175b1"
gtfs_sources.append(gtfs)


fieldnames = ["ID", "Licence", "Source link", "Description", "Download"]
with open("sources_GTFS.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for g in gtfs_sources:
        writer.writerow(g)
