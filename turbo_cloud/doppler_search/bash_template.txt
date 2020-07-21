#!/bin/bash

### Modified bash script from /datax/scratch/karenp/turbo_event at the Breakthrough Listen Data Center at UC-Berkeley
#for file in /tess_container/seti_tess/c_band/*0000.h5; do
for file in ABSOLUTE_OR_RELATIVE_PATH_TO_FILES_TO_RUN_TURBO_SETI_ON; do
  if [[ "$file" == *"IDENTIFIER"* ]] || [[ "$file" == *"ANOTHER_IDENTIFIER"* ]]; then
    echo "$file"
  
   time turboSETI "$file" -s 10 -M 4 -o ABSOLUTE_OR_RELATIVE_PATH_TO_DESIRED_OUTPUT_DIRECTORY_FOR_.DAT_FILES
   
    echo "complete"
  else
    echo "invalid"
  fi
done
