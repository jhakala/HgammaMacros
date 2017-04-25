from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getFilePrefix():
  return "ddTree_"

def getMCbgSampleXsects():
  sampleXsects = {}
  ##sampleXsects["GJets_HT-100To200.root"    ] = 9238*1.8
  #sampleXsects["GJets_HT-100To200.root"    ] = 9238*1.8*0.8
  ## sampleXsects["GJets_HT-200To400.root"    ] = 2305*1.8
  #sampleXsects["GJets_HT-200To400.root"    ] = 2305*1.8*0.8
  ## sampleXsects["GJets_HT-400To600.root"    ] = 274.4*1.4
  #sampleXsects["GJets_HT-400To600.root"    ] = 274.4*1.4*0.8
  #sampleXsects["GJets_HT-600ToInf.root"    ] = 93.46*0.8
  #sampleXsects["QCD_HT100to200.root"       ] = 27990000*0.8
  #sampleXsects["QCD_HT200to300.root"       ] = 1712000*0.8
  #sampleXsects["QCD_HT300to500.root"       ] = 347700*0.8
  #sampleXsects["QCD_HT500to700.root"       ] = 32100*0.8
  #sampleXsects["QCD_HT700to1000.root"      ] = 6831*0.8
  #sampleXsects["QCD_HT1000to1500.root"     ] = 1207*0.8
  #sampleXsects["QCD_HT1500to2000.root"     ] = 119.9*0.8
  #sampleXsects["QCD_HT2000toInf.root"      ] = 25.24*0.8
  #sampleXsects["DYJetsToQQ_HT180.root"     ] = 1187*1.23*0.8
  #sampleXsects["WJetsToQQ_HT-600ToInf.root"] = 95.14*1.21*0.8
  #sampleXsects["2016gJets100-200_Nov21.root"]  = 9238*1.8*0.8
  #sampleXsects["2016gJets200-400_Nov21.root"]  = 2305*1.8*0.8
  #sampleXsects["2016gJets400-600_Nov21.root"]  = 274.4*1.4*0.8
  #sampleXsects["2016gJets600-Inf_Nov21.root"]  = 93.46*0.8
  #sampleXsects["2016qcd200-300_Nov21.root"]    = 1712000*0.8
  #sampleXsects["2016qcd300-500_Nov21.root"]    = 347700*0.8
  #sampleXsects["2016qcd500-700_Nov21.root"]    = 32100*0.8
  #sampleXsects["2016qcd700-1000_Nov21.root"]   = 6831*0.8
  #sampleXsects["2016qcd1000-1500_Nov21.root"]  = 1207*0.8
  #sampleXsects["2016qcd1500-2000_Nov21.root"]  = 119.9*0.8
  #sampleXsects["2016qcd2000-Inf_Nov21.root"]   = 25.24*0.8
  #sampleXsects["2016dyJetsToQQ180_Nov21.root"] = 1187*1.23*0.8
  #sampleXsects["2016wJetsToQQ180_Nov21.root"]  = 95.14*1.21*0.8
  sampleXsects[   "2016GJets100-200.root"   ]   = 9238*1.8*0.8   
  sampleXsects[   "2016GJets200-400.root"   ]   = 2305*1.8*0.8   
  sampleXsects[   "2016GJets400-600.root"   ]   = 274.4*1.4*0.8  
  sampleXsects[   "2016GJets600-Inf.root"   ]   = 93.46*0.8      
  sampleXsects[   "2016QCD200-300.root"     ]   = 1712000*0.8    
  sampleXsects[   "2016QCD300-500.root"     ]   = 347700*0.8     
  sampleXsects[   "2016QCD500-700.root"     ]   = 32100*0.8      
  sampleXsects[   "2016QCD700-1000.root"    ]    = 6831*0.8       
  sampleXsects[   "2016QCD1000-1500.root"   ]    = 1207*0.8       
  sampleXsects[   "2016QCD1500-2000.root"   ]    = 119.9*0.8      
  sampleXsects[   "2016QCD2000-Inf.root"    ]    = 25.24*0.8      
  sampleXsects[   "2016DYJetsToQQ180.root"  ]    = 1187*1.23*0.8  
  sampleXsects[   "2016WJetsToQQ180.root"   ]    = 95.14*1.21*0.8 
  return sampleXsects

def getMCbgSampleEvents(small3Dir):
  sampleXsects=getMCbgSampleXsects()
  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/%s" % (small3Dir, key)
    print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( "%s/%s" % (small3Dir, key) )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetBinContent(1)
    sampleEvents[key]=nEvents;
  return sampleEvents

def getSignalsToInclude():
  return [  #"Hgamma_m650.root",
            #"Hgamma_m750.root",
            #"Hgamma_m1000.root",
            #"Hgamma_m1250.root",
            #"Hgamma_m1500.root",
            #"Hgamma_m1750.root",
            #"Hgamma_m2000.root",
            #"Hgamma_m2500.root",
            #"Hgamma_m3000.root",
            #"Hgamma_m3500.root",
            #"Hgamma_m4000.root"
            #"signal_m650.root",
            "signal_m750.root",
            "signal_m850.root",
            "signal_m1000.root",
            "signal_m1150.root",
            "signal_m1300.root",
            "signal_m1450.root",
            "signal_m1600.root",
            "signal_m1750.root",
            "signal_m1900.root",
            "signal_m2050.root",
            "signal_m2450.root",
            "signal_m2850.root",
            "signal_m3250.root",
          ]

def getWeightsDict(small3Dir):
  sampleXsects = getMCbgSampleXsects() 
  sampleEvents = getMCbgSampleEvents(small3Dir)

  lumi = 36420

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = expectedEvents/sampleEvents[key]
    sampleWeights[key] = weight
  signalWeight = .5
  #for signalToInclude in getSignalsToInclude():
  #  sampleWeights[signalToInclude] = signalWeight
  sampleWeights["SilverJson.root"] = 1
#  sampleWeights[ "signal_m650.root"   ] = .8*10
  sampleWeights[ "signal_m750.root"   ] = .8*10
  sampleWeights[ "signal_m850.root"   ] = .8*10
  sampleWeights[ "signal_m1000.root"  ] = .7*10
  sampleWeights[ "signal_m1150.root"  ] = .7*10
  sampleWeights[ "signal_m1300.root"  ] = .7*10
  sampleWeights[ "signal_m1450.root"  ] = .6*10
  sampleWeights[ "signal_m1600.root"  ] = .6*10
  sampleWeights[ "signal_m1750.root"  ] = .6*10
  sampleWeights[ "signal_m1900.root"  ] = .5*10
  sampleWeights[ "signal_m2050.root"  ] = .5*10
  sampleWeights[ "signal_m2450.root"  ] = .5*10
  sampleWeights[ "signal_m2850.root"  ] = .4*10
  sampleWeights[ "signal_m3250.root"  ] = .4*10
  return sampleWeights

def getMCbgWeightsDict(small3Dir):
 weights = getWeightsDict(small3Dir) 
 nonMCbgs = getSignalsToInclude()
 nonMCbgs.append("SilverJson.root")
 for nonMCbg in nonMCbgs:
   weights.pop(nonMCbg)
 return weights

def getMCbgOrderedList():
  return [ 
    #"WJetsToQQ_HT-600ToInf.root",
    #"DYJetsToQQ_HT180.root"     ,
    #"QCD_HT2000toInf.root"      ,
    #"QCD_HT1500to2000.root"     ,
    #"QCD_HT1000to1500.root"     ,
    #"QCD_HT700to1000.root"      ,
    #"QCD_HT500to700.root"       ,
    #"QCD_HT300to500.root"       ,
    #"QCD_HT200to300.root"       ,
    #"QCD_HT100to200.root"       ,
    #"GJets_HT-600ToInf.root"    ,
    #"GJets_HT-400To600.root"    ,
    #"GJets_HT-200To400.root"    ,
    #"GJets_HT-100To200.root"    
    #"2016dyJetsToQQ180_Nov21.root",
    #"2016wJetsToQQ180_Nov21.root" ,
    #"2016qcd2000-Inf_Nov21.root"  ,
    #"2016qcd1500-2000_Nov21.root" ,
    #"2016qcd1000-1500_Nov21.root" ,
    #"2016qcd700-1000_Nov21.root"  ,
    #"2016qcd500-700_Nov21.root"   ,
    #"2016qcd300-500_Nov21.root"   ,
    #"2016qcd200-300_Nov21.root"   ,
    #"2016gJets600-Inf_Nov21.root" ,
    #"2016gJets400-600_Nov21.root" ,
    #"2016gJets200-400_Nov21.root" ,
    #"2016gJets100-200_Nov21.root" ,
    "2016DYJetsToQQ180.root"   ,
    "2016WJetsToQQ180.root"    ,
    "2016QCD2000-Inf.root"     ,
    "2016QCD1500-2000.root"    ,
    "2016QCD1000-1500.root"    ,
    "2016QCD700-1000.root"     ,
    "2016QCD500-700.root"      ,
    "2016QCD300-500.root"      ,
    "2016QCD200-300.root"      ,
    "2016GJets600-Inf.root"    ,
    "2016GJets400-600.root"    ,
    "2016GJets200-400.root"    ,
    "2016GJets100-200.root"   
  ]

def getMCbgColors():
  color = TColor()
  sampleColors = {}
  #sampleColors["QCD_HT100to200.root"       ] = color.GetColor(.1, 0.3, 0.25)
  sampleColors["2016GJets100-200.root" ] = color.GetColor(.475*1.1, .6*1.2, 1.0)
  sampleColors["2016GJets200-400.root" ] = color.GetColor(.475, .6, 1.0)
  sampleColors["2016GJets400-600.root" ] = color.GetColor(.35, .5, 0.85)
  sampleColors["2016GJets600-Inf.root" ] = color.GetColor(.225, .3, 0.7) 
  sampleColors["2016QCD200-300.root"   ] = color.GetColor(.31*1.2, 1.0, 0.425*1.2)
  sampleColors["2016QCD300-500.root"   ] = color.GetColor(.31, .95, 0.425)
  sampleColors["2016QCD500-700.root"   ] = color.GetColor(.28, .9, 0.4)
  sampleColors["2016QCD700-1000.root"  ] = color.GetColor(.25, .8, 0.375)
  sampleColors["2016QCD1000-1500.root" ] = color.GetColor(.22, .7, 0.35)
  sampleColors["2016QCD1500-2000.root" ] = color.GetColor(.19, .6, 0.325)
  sampleColors["2016QCD2000-Inf.root"  ] = color.GetColor(.16, .5, 0.3)
  sampleColors["2016DYJetsToQQ180.root"] = color.GetColor(.6, .2, .2)
  sampleColors["2016WJetsToQQ180.root" ] = color.GetColor(.85, .85, 0.3)
  return sampleColors

def getMCbgLabels():
  color = TColor()
  legendLabels = {}
  legendLabels["2016GJets100-200" ] = "#gamma#plusjets[100,200]"
  legendLabels["2016GJets200-400" ] = "#gamma#plusjets[200,400]"
  legendLabels["2016GJets400-600" ] = "#gamma#plusjets[400,600]"
  legendLabels["2016GJets600-Inf" ] = "#gamma#plusjets[600,#infty]"
  legendLabels["2016QCD200-300"   ] = "QCD[200,300]"
  legendLabels["2016QCD300-500"   ] = "QCD[300,500]"
  legendLabels["2016QCD500-700"   ] = "QCD[500,700]"
  legendLabels["2016QCD700-1000"  ] = "QCD[700,1000]"
  legendLabels["2016QCD1000-1500" ] = "QCD[1000,1500]"
  legendLabels["2016QCD1500-2000" ] = "QCD[1500,2000]"
  legendLabels["2016QCD2000-Inf"  ] = "QCD[2000,#infty]"
  legendLabels["2016DYJetsToQQ180"] = "DY#plusjets[180,#infty]"
  legendLabels["2016WJetsToQQ180" ] = "W#plusjets[600,#infty]"
  #legendLabels["QCD_HT100to200"       ] = "QCD[100,200]"
  return legendLabels

def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  #s3dd["QCD_HT100to200.root"       ] = "%s/ddTree_QCD_HT100to200.root"%ddDir
  s3dd["2016GJets100-200" ] = "%s/ddTree_2016GJets100-200"  % ddDir
  s3dd["2016GJets200-400" ] = "%s/ddTree_2016GJets200-400"  % ddDir
  s3dd["2016GJets400-600" ] = "%s/ddTree_2016GJets400-600"  % ddDir
  s3dd["2016GJets600-Inf" ] = "%s/ddTree_2016GJets600-Inf"  % ddDir
  s3dd["2016QCD200-300"   ] = "%s/ddTree_2016QCD200-300"    % ddDir
  s3dd["2016QCD300-500"   ] = "%s/ddTree_2016QCD300-500"    % ddDir
  s3dd["2016QCD500-700"   ] = "%s/ddTree_2016QCD500-700"    % ddDir
  s3dd["2016QCD700-1000"  ] = "%s/ddTree_2016QCD700-1000"   % ddDir
  s3dd["2016QCD1000-1500" ] = "%s/ddTree_2016QCD1000-1500"  % ddDir
  s3dd["2016QCD1500-2000" ] = "%s/ddTree_2016QCD1500-2000"  % ddDir
  s3dd["2016QCD2000-Inf"  ] = "%s/ddTree_2016QCD2000-Inf"   % ddDir
  s3dd["2016DYJetsToQQ180"] = "%s/ddTree_2016DYJetsToQQ180" % ddDir
  s3dd["2016WJetsToQQ180" ] = "%s/ddTree_2016WJetsToQQ180"  % ddDir

  return s3dd
