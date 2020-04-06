TRASHDIR=trash/`date +%h%d-%y_%H:%M:%S`
mkdir ${TRASHDIR}

if [ $? -eq 0 ]; then
  for OUTPUT in ${OUTPUTS[@]}; do 
    if [ -d $OUTPUT ]; then
      mv ${OUTPUT} ${TRASHDIR}
    fi
  done
fi
