#!/bin/bash
FILE_PATH=$1
EXPECTED_LINE_NUMBERS=$2
FOUND_LINE_NUMBERS=`cat "$1" |wc -l`

echo "Nombre minimal de lignes attendues pour le fichier $1 : $2 ; Nombre de lignes trouvées : $FOUND_LINE_NUMBERS"
test $FOUND_LINE_NUMBERS -ge $EXPECTED_LINE_NUMBERS

