#! /bin/bash

echo -e "Input table name"
read TABLE_NAME

OUTPUT=$GOPATH/src/bitbucket.org/beecomb-grid/grid-ai/gridai_service_common/entities

# Output file name
OUTPUT_FILE_PATH=${OUTPUT}/$(tr '[A-Z]' '[a-z]' <<< ${TABLE_NAME})

# Generate go entity
python generate.py \
  --user=root \
  --host=127.0.0.1 \
  --port=13306 \
  --passwd=gridairoot \
  --database=gridai_contracts \
  --table_name=${TABLE_NAME} > ${OUTPUT_FILE_PATH}.go

# Format file
goimports -w $OUTPUT

