#!/usr/bin/env bash

set -e

echo "\copy ${6} from '${7}' (delimiter(','), encoding 'Latin1');"

PGPASSWORD="${5}" psql -h "${1}" -p "${2}" -d "${3}" -U "${4}" -c "\copy ${6} from ${7} WITH delimiter as ',' NULL as '' CSV HEADER encoding 'Latin1'"