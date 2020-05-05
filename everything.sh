PDF="python tdrAllStacks.py"
DDOPTS="python plotOpts_dd.py"
if [ "$1" != "jump" ]; then
  echo "not jumping!"
  CLEANUP=1 
  export OUTPUTS=( weightedMCbgHists_preselection_sideband5070 weightedMCbgHists_preselection_sideband100110 weightedMCbgHists_preselection stackplots_preselection_sideband5070 stackplots_preselection_sideband100110 stackplots_preselection weightedMCbgHists_nMinus1_withBtag_sideband100110_SF weightedMCbgHists_nMinus1_withBtag_sideband100110 weightedMCbgHists_nMinus1_withBtag_sideband5070_SF weightedMCbgHists_nMinus1_withBtag_sideband5070 weightedMCbgHists_nMinus1_withBtag_SF weightedMCbgHists_nMinus1_withBtag weightedMCbgHists_btag_sideband100110 weightedMCbgHists_btag_sideband5070 weightedMCbgHists_btag stackplots_nMinus1_withBtag_sideband100110_SF stackplots_nMinus1_withBtag_sideband100110 stackplots_nMinus1_withBtag_SF stackplots_nMinus1_withBtag stackplots_btag_sideband100110 stackplots_nMinus1_withBtag_sideband5070_SF stackplots_nMinus1_withBtag_sideband5070 stackplots_btag weightedMCbgHists_nMinus1_noBtag_sideband100110_SF weightedMCbgHists_nMinus1_noBtag_sideband100110 stackplots_btag_sideband5070 weightedMCbgHists_nMinus1_noBtag_sideband5070_SF weightedMCbgHists_nMinus1_noBtag_sideband5070 weightedMCbgHists_nMinus1_noBtag_SF weightedMCbgHists_nMinus1_noBtag weightedMCbgHists_antibtag_sideband100110 stackplots_nMinus1_noBtag_sideband5070_SF stackplots_nMinus1_noBtag_sideband5070 stackplots_nMinus1_noBtag_sideband100110_SF stackplots_nMinus1_noBtag_sideband100110 stackplots_nMinus1_noBtag_SF stackplots_nMinus1_noBtag weightedMCbgHists_btag_sideband5070_SF weightedMCbgHists_btag_sideband100110_SF weightedMCbgHists_btag_SF weightedMCbgHists_antibtag_sideband5070 weightedMCbgHists_antibtag stackplots_btag_sideband100110_SF stackplots_btag_SF stackplots_antibtag_sideband5070 stackplots_antibtag_sideband100110 stackplots_antibtag stackplots_btag_sideband5070_SF weightedMCbgHists_antibtag_SF stackplots_antibtag_SF weightedMCbgHists_antibtag_sideband100110_SF stackplots_antibtag_sideband100110_SF weightedMCbgHists_antibtag_sideband5070_SF stackplots_antibtag_sideband5070_SF pdf_stackplots_antibtag pdf_stackplots_preselection_sideband5070 pdf_stackplots_preselection_sideband100110 pdf_stackplots_preselection pdf_stackplots_nMinus1_withBtag_sideband100110_SF pdf_stackplots_nMinus1_withBtag_sideband100110 pdf_stackplots_nMinus1_withBtag_SF pdf_stackplots_nMinus1_withBtag pdf_stackplots_btag_sideband100110 pdf_stackplots_nMinus1_withBtag_sideband5070_SF pdf_stackplots_nMinus1_withBtag_sideband5070 pdf_stackplots_btag pdf_stackplots_btag_sideband5070 pdf_stackplots_nMinus1_noBtag_sideband5070_SF pdf_stackplots_nMinus1_noBtag_sideband5070 pdf_stackplots_nMinus1_noBtag_sideband100110_SF pdf_stackplots_nMinus1_noBtag_sideband100110 pdf_stackplots_nMinus1_noBtag_SF pdf_stackplots_nMinus1_noBtag pdf_stackplots_btag_sideband100110_SF pdf_stackplots_btag_SF pdf_stackplots_antibtag_sideband5070 pdf_stackplots_antibtag_sideband100110 pdf_stackplots_btag_sideband5070_SF pdf_stackplots_antibtag_SF pdf_stackplots_antibtag_sideband100110_SF pdf_stackplots_antibtag_sideband5070_SF optplots_nMinus1_withBtag_dd optplots_nMinus1_noBtag_dd optplots_nMinus1_withBtag_dd_sb100110 optplots_nMinus1_withBtag_dd_sb5070 optplots_nMinus1_noBtag_dd_sb100110 optplots_nMinus1_noBtag_dd_sb5070 ) 
#  if [ $CLEANUP -eq 1 ]; then
#    echo "cleaning up..."
#    source cleanup.sh
#  fi
  STACK="python makeStacks.py -a Zg"
  MCOPTS="python plotOpts.py -a Zg"
  
  ${STACK} -c preselection 
  (${STACK} -c preselection ; ${STACK} -c preselection -s &  ${STACK} -c preselection -s -e 5070) &
  (${STACK} -c nobtag ;  ${STACK} -c nobtag -s &  ${STACK} -c nobtag -s -e 5070) &
  (${STACK} -c nMinus1;  ${STACK} -c nMinus1 -s &  ${STACK} -c nMinus1 -s -e 5070) &
  (${STACK} -c nMinus1 -w ;  ${STACK} -c nMinus1 -w -s & ${STACK} -c nMinus1 -w -s -e 5070) &
  (${STACK} -c nMinus1 -f ;  ${STACK} -c nMinus1 -s -f &   ${STACK} -c nMinus1 -s -f -e 5070) &
  (${STACK} -c nMinus1 -w -f ;  ${STACK} -c nMinus1 -w -s -f &  ${STACK} -c nMinus1 -w -s -f -e 5070) &
  (${STACK} -c btag ;  ${STACK} -c btag -s &  ${STACK} -c btag -s -e 5070) &
  (${STACK} -c btag -f ;  ${STACK} -c btag -s -f &  ${STACK} -c btag -s -f -e 5070) &
  (${STACK} -c antibtag ;  ${STACK} -c antibtag -s &   ${STACK} -c antibtag -s -e 5070)  &
  (${STACK} -c antibtag -f ;  ${STACK} -c antibtag -s -f &  ${STACK} -c antibtag -s -f -e 5070) 
  (${STACK} -c preselection ; ${STACK} -c preselection -s &  ${STACK} -c preselection -s -e 100110) &
  (${STACK} -c nobtag ;  ${STACK} -c nobtag -s &  ${STACK} -c nobtag -s -e 100110) &
  (${STACK} -c nMinus1;  ${STACK} -c nMinus1 -s &  ${STACK} -c nMinus1 -s -e 100110) &
  (${STACK} -c nMinus1 -w ;  ${STACK} -c nMinus1 -w -s & ${STACK} -c nMinus1 -w -s -e 100110) &
  (${STACK} -c nMinus1 -f ;  ${STACK} -c nMinus1 -s -f &   ${STACK} -c nMinus1 -s -f -e 100110) &
  (${STACK} -c nMinus1 -w -f ;  ${STACK} -c nMinus1 -w -s -f &  ${STACK} -c nMinus1 -w -s -f -e 100110) &
  (${STACK} -c btag ;  ${STACK} -c btag -s &  ${STACK} -c btag -s -e 100110) &
  (${STACK} -c btag -f ;  ${STACK} -c btag -s -f &  ${STACK} -c btag -s -f -e 100110) &
  (${STACK} -c antibtag ;  ${STACK} -c antibtag -s &   ${STACK} -c antibtag -s -e 100110)  &
  (${STACK} -c antibtag -f ;  ${STACK} -c antibtag -s -f &  ${STACK} -c antibtag -s -f -e 100110) 
  (${STACK} -c -f antibtag -v & ${STACK} -c -f btag -v)
  ####################3
  #(${STACK} -c preselection ; ${STACK} -c preselection -s ;   
  #${STACK} -c nobtag ;  ${STACK} -c nobtag -s ; 
  #${STACK} -c nMinus1;  ${STACK} -c nMinus1 -s ; 
  #${STACK} -c nMinus1 -w ;  ${STACK} -c nMinus1 -w -s ;
  #${STACK} -c nMinus1 -f ;  ${STACK} -c nMinus1 -s -f ;
  #${STACK} -c nMinus1 -w -f ;  ${STACK} -c nMinus1 -w -s -f ;
  #${STACK} -c btag ;  ${STACK} -c btag -s ; 
  #${STACK} -c btag -f ;  ${STACK} -c btag -s -f ; 
  #${STACK} -c antibtag ;  ${STACK} -c antibtag -s ; 
  #${STACK} -c antibtag -f ;  ${STACK} -c antibtag -s -f ; 
  ##(${STACK} -c preselection ; ${STACK} -c preselection -s ;
  #${STACK} -c nobtag ;  ${STACK} -c nobtag -s ;  ${STACK} -c nobtag -s -e 100110 ;
  #${STACK} -c nMinus1;  ${STACK} -c nMinus1 -s ;  ${STACK} -c nMinus1 -s -e 100110 ;
  #${STACK} -c nMinus1 -w ;  ${STACK} -c nMinus1 -w -s ; ${STACK} -c nMinus1 -w -s -e 100110 ;
  #${STACK} -c nMinus1 -f ;  ${STACK} -c nMinus1 -s -f ;   ${STACK} -c nMinus1 -s -f -e 100110 ;
  #${STACK} -c nMinus1 -w -f ;  ${STACK} -c nMinus1 -w -s -f ;  ${STACK} -c nMinus1 -w -s -f -e 100110 ;
  #${STACK} -c btag ;  ${STACK} -c btag -s ;  ${STACK} -c btag -s -e 100110 ;
  #${STACK} -c btag -f ;  ${STACK} -c btag -s -f ;  ${STACK} -c btag -s -f -e 100110 ;
  #${STACK} -c antibtag ;  ${STACK} -c antibtag -s ;   ${STACK} -c antibtag -s -e 100110  ;
  #${STACK} -c antibtag -f ;  ${STACK} -c antibtag -s -f ;  ${STACK} -c antibtag -s -f -e 100110 
  #${STACK} -c -f antibtag -v ; ${STACK} -c -f btag -v

  for STACK in ${STACKS[@]}
    do ${PDF} -i ${STACK} -o pdf_${STACK} 
  done

else
  echo "jumping!"
fi
export STACKS=( stackplots_nobtag_sideband5070 stackplots_nobtag_sideband100110 stackplots_nobtag stackplots_preselection_sideband5070 stackplots_preselection_sideband100110 stackplots_preselection stackplots_nMinus1_withBtag_sideband100110_SF stackplots_nMinus1_withBtag_sideband100110 stackplots_nMinus1_withBtag_SF stackplots_nMinus1_withBtag stackplots_btag_sideband100110 stackplots_nMinus1_withBtag_sideband5070_SF stackplots_nMinus1_withBtag_sideband5070 stackplots_btag stackplots_btag_sideband5070 stackplots_nMinus1_noBtag_sideband5070_SF stackplots_nMinus1_noBtag_sideband5070 stackplots_nMinus1_noBtag_sideband100110_SF stackplots_nMinus1_noBtag_sideband100110 stackplots_nMinus1_noBtag_SF stackplots_nMinus1_noBtag stackplots_btag_sideband100110_SF stackplots_btag_SF stackplots_antibtag_sideband5070 stackplots_antibtag_sideband100110 stackplots_antibtag stackplots_btag_sideband5070_SF stackplots_antibtag_SF stackplots_antibtag_sideband100110_SF stackplots_antibtag_sideband5070_SF ) 
##${MCOPTS} 
echo ${DDOPTS} withBtag 100110
${DDOPTS} withBtag 100110
echo ${DDOPTS} withBtag 5070
${DDOPTS} withBtag 5070
echo ${DDOPTS} noBtag 100110
${DDOPTS} noBtag 100110
echo ${DDOPTS} noBtag 5070
${DDOPTS} noBtag 5070

echo -e '\n\n\n------------------------------\nDone with validation plots!\n------------------------------'
echo -e '\n\n\n------------------------------\nNow making vgHists!\n------------------------------'
python makeVgHists.py
echo -e '\n\n\n------------------------------\nDone!\n------------------------------'
