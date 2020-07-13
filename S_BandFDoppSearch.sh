#/bin/bash

#for file in /datax/scratch/karenp/SETI_events/HIP91699_Danny/*fine.h5; do
#for file in /home/raffytraas14/seti_tess/l_band/*0000.h5; do
for file in /tess_container/seti_tess/s_band/*0000.h5; do
  if [[ "$file" == *"TIC"* ]] || [[ "$file" == *"HIP"* ]]; then
    echo "$file"
   # subdir=${file%%.*}
   # [ ! -d "$subdir" ] && mkdir -- "$subdir"
   # time turboSETI  "$file" -s 10 -M 4 -n 64 -o "$subdir"
   time turboSETI "$file" -s 10 -M 4 -o /tess_container/outs_s_band/ 
   #time python /home/bryanb/turbo_seti/turbo_seti/findoppler/seti_event.py "$file" -s 20 -M 4 -o /datax/scratch/karenp/SETI_events
    echo "complete"
  else
    echo "invalid"
  fi
done
