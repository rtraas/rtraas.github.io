### Modified bash scripts from /datax/scratch/karenp/turbo_event
for file in /tess_container/seti_tess/c_band/*0000.h5; do
  if [[ "$file" == *"TIC"* ]] || [[ "$file" == *"HIP"* ]]; then
    echo "$file"
  
   time turboSETI "$file" -s 10 -M 4 -o /tess_container/outs_c_band/ 
   
    echo "complete"
  else
    echo "invalid"
  fi
done
