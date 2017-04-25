#!/bin/bash

#python runHbbGammaSelector.py ~/hbbgamma80X/small3s/HgammaSlimmedData_Oct5.root newerDDs/ddTree_Hgamma_data27fb-1.root compile

#backgroundsAndData=( DYJetsToQQ_HT180 GJets_HT-100To200 GJets_HT-200To400 GJets_HT-400To600 GJets_HT-600ToInf QCD_HT100to200 QCD_HT200to300 QCD_HT300to500 QCD_HT500to700 QCD_HT700to1000 QCD_HT1000to1500 QCD_HT1500to2000 QCD_HT2000toInf RunC  WJetsToQQ_HT-600ToInf )
#backgrounds=( 2016DYJetsToQQ180 2016GJets100-200 2016GJets200-400 2016GJets400-600 2016GJets600-Inf 2016QCD1000-1500 2016QCD1500-2000 2016QCD200-300 2016QCD2000-Inf 2016QCD300-500 2016QCD500-700 2016QCD700-1000 2016WJetsToQQ180 )
#for file in "${backgroundsAndData[@]}"
#do
#  python runHbbGammaSelector.py ~/physics/nTuplizerStep/small3s/small3_${file}.root newerDDs/ddTree_${file}.root load
#done

##########
#  data  #
##########
#data=( 2016Hv3_2 2016Hv3_3 2016Hv3_1 2016Hv3_0 2016G-1_0 2016Hv2-1_0 2016F_0 2016F_3 2016F_2 2016B-0_1 2016Hv2-0_0 2016F_1 2016B-1_1 2016Hv2-0_2 2016B-1_3 2016B-0_0 2016E_1 2016B-1_2 2016Hv2-0_1 2016B-0_2 2016C_0 2016C_3 2016C_2 2016B-1_0 2016E_0 2016G-1_1 2016G-1_2 2016D_3 2016B-0_3 2016Hv2-1_1 2016C_1 2016Hv2-1_3 2016D_1 2016G-1_3 2016E_3 2016E_2 2016Hv2-1_2 2016D_2 2016Hv2-0_3 2016G-0_1 2016D_0 2016G-0_2 2016G-0_0 2016G-0_3 )
#
#
#for file in "${data[@]}"; do python runHbbGammaSelector.py 80XDDs_Mar14/Mar14_dataFrags/Hgamma_Mar14_${file}.root 80XDDs_Mar14/ddTreeFrags/ddTree_Mar14_${file}.root load & done

###########
#  gjets  #
###########
#gjets=( GJets100-200-0_0 GJets100-200-0_1 GJets100-200-0_2 GJets100-200-0_3 GJets200-400-0_0 GJets200-400-0_1 GJets200-400-0_2 GJets200-400-0_3 GJets200-400-1_0 GJets200-400-1_1 GJets200-400-1_2 GJets200-400-1_3 GJets200-400-2_0 GJets200-400-2_1 GJets200-400-2_2 GJets200-400-2_3 GJets200-400-3_0 GJets200-400-3_1 GJets200-400-3_2 GJets200-400-3_3 GJets400-600-0_0 GJets400-600-0_1 GJets400-600-0_2 GJets400-600-0_3 GJets600-Inf-0_0 GJets600-Inf-0_1 GJets600-Inf-0_2 GJets600-Inf-0_3 )
#
#for file in "${gjets[@]}"; do python runHbbGammaSelector.py ~/physics/dec17_ntuples/fragments/gjetsFrags/Hgamma_Dec23_${file}.root 80XDDs_Dec13/gjetsFrags/ddTree_Dec23_${file}.root load & done


#############
#  signals  #
#############
#masses=( 650 750 1000 1250 1500 1750 2000 2500 3000 3500 4000 )
#masses=( 750 1000 1250 1500 1750 2000 2500 3000 3500 4000 )
#
export OUTSIGDIR=80XDDs_Apr17_pruned_sigs
initialMass=650
python runHbbGammaSelector.py ~/physics/80Xsignals/flatTuple_m${initialMass}.root ${OUTSIGDIR}/ddTree_Hgamma_m${initialMass}.root compile
sleep 1

masses=(750 850 1000 1150 1300 1450 1600 1750 1900 2050 2450 2850 3250)
for mass in "${masses[@]}"; do python runHbbGammaSelector.py ~/physics/80Xsignals/flatTuple_m${mass}.root ${OUTSIGDIR}/ddTree_Hgamma_m${mass}.root compile ; done
