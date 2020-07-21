#!/bin/bash

### Modified bash script from /datax/scratch/karenp/turbo_event at the Breakthrough Listen Data Center at UC-Berkeley

for file in /tess_container/seti_tess/x_band/*0000.h5; do
  if [[ "$file" == *"TIC"* ]] || [[ "$file" == *"HIP"* ]]; then
    echo "$file"
   
   time turboSETI "$file" -s 10 -M 4 -o /tess_container/outs_x_band/ 
   
    echo "complete"
  else
    echo "invalid"
  fi
done
