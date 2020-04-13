#! /bin/bash

echo -e "Input table name"
read TABLE_NAME

OUTPUT=$GOPATH/src/bitbucket.org/beecomb-grid/renewable-energy-institute-api/entities

# Output file name
OUTPUT_FILE_PATH=${OUTPUT}/$(tr '[A-Z]' '[a-z]' <<< ${TABLE_NAME})

# Generate go entity
python generate.py \
  --user=rei_user \
  --host=127.0.0.1 \
  --port=3306 \
  --passwd=rei_pass \
  --database=renewable_energy_institute \
  --table_name=${TABLE_NAME} > ${OUTPUT_FILE_PATH}.go

# Format file
goimports -w $OUTPUT

