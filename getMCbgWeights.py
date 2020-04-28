from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getDDPrefix():
  return "ddTree_"

def getSmallPrefix():
  return "smallified_"

def getMCbgSampleKfactors():
  sampleXsects = {}
  sampleXsects[   "gJets100To200.root"   ]   = 1.6*.8
  sampleXsects[   "gJets200To400.root"   ]   = 1.6*.8
  sampleXsects[   "gJets400To600.root"   ]   = 1.4*.8
  sampleXsects[   "gJets600ToInf.root"   ]   = 1.0*.8
  sampleXsects[   "qcd300To500.root"     ]   = .7 *.8
  sampleXsects[   "qcd500To700.root"     ]   = .7 *.8
  sampleXsects[   "qcd700To1000.root"    ]   = .7 *.8
  sampleXsects[   "qcd1000To1500.root"   ]   = .7 *.8
  sampleXsects[   "qcd1500To2000.root"   ]   = .7 *.8
  sampleXsects[   "qcd2000ToInf.root"    ]   = .7 *.8
  #sampleXsects[   "qcd200to300.root"     ]  = 1   
  #sampleXsects[   "dyJetsQQ-180.root"    ]  = 1.23  
  #sampleXsects[ "wJetsQQ-180.root" ]        = 1.21*0.8 
  return sampleXsects

def getMCbgSampleXsects():
  kFactors = getMCbgSampleKfactors()
  sampleXsects = {}
  sampleXsects[   "gJets100To200.root"   ]   = 9238
  sampleXsects[   "gJets200To400.root"   ]   = 2305
  sampleXsects[   "gJets400To600.root"   ]   = 274.4
  sampleXsects[   "gJets600ToInf.root"   ]   = 93.46 
  sampleXsects[   "qcd300To500.root"     ]   = 347700     
  sampleXsects[   "qcd500To700.root"     ]   = 32100      
  sampleXsects[   "qcd700To1000.root"    ]    = 6831       
  sampleXsects[   "qcd1000To1500.root"   ]    = 1207       
  sampleXsects[   "qcd1500To2000.root"   ]    = 119.9      
  sampleXsects[   "qcd2000ToInf.root"    ]    = 25.24      
  #sampleXsects[   "qcd200to300.root"     ]   = 1712000    
  #sampleXsects[   "dyJetsQQ-180.root"    ]    = 1187  
  #sampleXsects[ "wJetsQQ-180.root" ] = 95.14 
  return sampleXsects

def getMCbgSampleEvents(small3Dir):
  sampleXsects=getMCbgSampleXsects()
  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/%s%s" % (small3Dir, getSmallPrefix(), key)
    #print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( mcBGfileName )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetBinContent(1)
    sampleEvents[key]=nEvents;
  return sampleEvents

def getSignalsToInclude():
  return [  "Hg-700.root",
            "Hg-800.root",
            "Hg-1000.root",
            "Hg-1200.root",
            "Hg-1400.root",
            "Hg-1600.root",
            #"Hg-1800.root",
            "Hg-2000.root",
            "Hg-2200.root",
            "Hg-2400.root",
            "Hg-2600.root",
            "Hg-3000.root",
            "Hg-3500.root",
          ]

def getWeightsDict(bkgSmall3Dir):
  sampleKfactors = getMCbgSampleKfactors() 
  sampleXsects   = getMCbgSampleXsects() 
  sampleEvents   = getMCbgSampleEvents(bkgSmall3Dir)

  lumi = 41860

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = sampleKfactors[key]*expectedEvents/sampleEvents[key]
    sampleWeights[key] = (weight, "bkg")
  signalWeight = .5
  #for signalToInclude in getSignalsToInclude():
  #  sampleWeights[signalToInclude] = signalWeight
  sampleWeights["data_2017.root"] = (1 , "data")
  sampleWeights[ "Hg-700.root"   ] = (.8*0.4, "sig")
  sampleWeights[ "Hg-800.root"   ] = (.8*0.4, "sig")
  sampleWeights[ "Hg-1000.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "Hg-1200.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "Hg-1400.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "Hg-1600.root"  ] = (.6*0.4, "sig")
  #sampleWeights[ "Hg-1800.root"  ] = (.6*0.4, "sig")
  sampleWeights[ "Hg-2000.root"  ] = (.5*0.4, "sig")
  sampleWeights[ "Hg-2200.root"  ] = (.5*0.4, "sig")
  sampleWeights[ "Hg-2400.root"  ] = (.4*0.4, "sig")
  sampleWeights[ "Hg-2600.root"  ] = (.4*0.4, "sig")
  sampleWeights[ "Hg-3000.root"  ] = (.4*0.4, "sig")
  sampleWeights[ "Hg-3500.root"  ] = (.4*0.4, "sig")
  return sampleWeights

def getMCbgWeightsDict(bkgSmall3Dir):
 weights = getWeightsDict(bkgSmall3Dir) 
 nonMCbgs = getSignalsToInclude()
 nonMCbgs.append("data_2017.root")
 for nonMCbg in nonMCbgs:
   weights.pop(nonMCbg)
 return weights

def getMCbgOrderedList():
  return [ 
    #"dyJetsQQ-180.root"   ,
    #"wJetsQQ-180.root"    ,
    "qcd2000ToInf.root"     ,
    "qcd1500To2000.root"    ,
    "qcd1000To1500.root"    ,
    "qcd700To1000.root"     ,
    "qcd500To700.root"      ,
    "qcd300To500.root"      ,
    "qcd200to300.root"      ,
    "gJets600ToInf.root"    ,
    "gJets400To600.root"    ,
    "gJets200To400.root"    ,
    "gJets100To200.root"   
  ]

def getMCbgColors():
  color = TColor()
  sampleColors = {}
  #sampleColors["QCD_HT100to200.root"       ] = color.GetColor(.1, 0.3, 0.25)
  sampleColors["gJets100To200.root" ] = color.GetColor(.475*1.1, .6*1.2, 1.0)
  sampleColors["gJets200To400.root" ] = color.GetColor(.475, .6, 1.0)
  sampleColors["gJets400To600.root" ] = color.GetColor(.35, .5, 0.85)
  sampleColors["gJets600ToInf.root" ] = color.GetColor(.225, .3, 0.7) 
  sampleColors["qcd100To200.root"   ] = color.GetColor(.31, 1.0, 0.425)
  sampleColors["qcd200To300.root"   ] = color.GetColor(.31*1.2, 1.0, 0.425*1.2)
  sampleColors["qcd300To500.root"   ] = color.GetColor(.31, .95, 0.425)
  sampleColors["qcd500To700.root"   ] = color.GetColor(.28, .9, 0.4)
  sampleColors["qcd700To1000.root"  ] = color.GetColor(.25, .8, 0.375)
  sampleColors["qcd1000To1500.root" ] = color.GetColor(.22, .7, 0.35)
  sampleColors["qcd1500To2000.root" ] = color.GetColor(.19, .6, 0.325)
  sampleColors["qcd2000ToInf.root"  ] = color.GetColor(.16, .5, 0.3)
  #sampleColors["dyJetsQQ-180.root"  ] = color.GetColor(.6, .2, .2)
  #sampleColors["wJetsQQ-180.root"   ] = color.GetColor(.85, .85, 0.3)
  return sampleColors

def getMCbgLabels():
  color = TColor()
  legendLabels = {}
  legendLabels["gJets100To200.root" ] = "#gamma#plusjets[100,200]"
  legendLabels["gJets200To400.root" ] = "#gamma#plusjets[200,400]"
  legendLabels["gJets400To600.root" ] = "#gamma#plusjets[400,600]"
  legendLabels["gJets600ToInf.root" ] = "#gamma#plusjets[600,#infty]"
  legendLabels["qcd200to300.root"   ] = "QCD[200,300]"
  legendLabels["qcd300To500.root"   ] = "QCD[300,500]"
  legendLabels["qcd500To700.root"   ] = "QCD[500,700]"
  legendLabels["qcd700To1000.root"  ] = "QCD[700,1000]"
  legendLabels["qcd1000To1500.root" ] = "QCD[1000,1500]"
  legendLabels["qcd1500To2000.root" ] = "QCD[1500,2000]"
  legendLabels["qcd2000ToInf.root"  ] = "QCD[2000,#infty]"
  #legendLabels["dyJetsQQ-180.root"  ] = "DY#plusjets[180,#infty]"
  #legendLabels["wJetsQQ-180.root"   ] = "W#plusjets[600,#infty]"
  legendLabels["QCD_HT100to200"       ] = "QCD[100,200]"
  return legendLabels

def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  #s3dd["QCD_HT100to200.root"       ] = "%s/ddTree_QCD_HT100to200.root"%ddDir
  #s3dd["gJets100To200" ] = "%s/ddTree_GJets100-200"  % ddDir
  s3dd["gJets200To400.root" ] = "%s/ddTree_gJets200To400"  % ddDir
  s3dd["gJets400To600.root" ] = "%s/ddTree_gJets400To600"  % ddDir
  s3dd["gJets600ToInf.root" ] = "%s/ddTree_gJets600ToInf"  % ddDir
  #s3dd["qcd200to300.root"   ] = "%s/ddTree_qcd200to300"    % ddDir
  s3dd["qcd300To500.root"   ] = "%s/ddTree_qcd300To500"    % ddDir
  s3dd["qcd500To700.root"   ] = "%s/ddTree_qcd500To700"    % ddDir
  s3dd["qcd700To1000.root"  ] = "%s/ddTree_qcd700To1000"   % ddDir
  s3dd["qcd1000To1500.root" ] = "%s/ddTree_qcd1000To1500"  % ddDir
  s3dd["qcd1500To2000.root" ] = "%s/ddTree_qcd1500To2000"  % ddDir
  s3dd["qcd2000ToInf.root"  ] = "%s/ddTree_qcd2000ToInf"   % ddDir
  #s3dd["dyJetsQQ-180.root"  ] = "%s/ddTree_dyJetsQQ-180"   % ddDir
  #s3dd["wJetsQQ-180.root"   ] = "%s/ddTree_wJetsQQ-180"    % ddDir

  return s3dd
