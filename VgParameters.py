# functions to centrally store Hgamma parameters
# John Hakala -  May 16, 2016
from ROOT import *

def getSamplesDirs(analysis):
  response = {}
  response["signalsSmall3sDir"] = "/Users/jhakala/HgammaMacros/organize_smallifications/signals"
  response["bkgSmall3sDir"]       = "/Users/jhakala/HgammaMacros/organize_smallifications/backgrounds"
  response["dataSmall3Dir"]       = "/Users/jhakala/HgammaMacros/organize_smallifications/data"
  response["dataSmall3File"]       = "/Users/jhakala/HgammaMacros/organize_smallifications/data/smallified_data_2017.root"

  response["bkgDDdir"]            = "/Users/jhakala/HgammaMacros/organize_%s_DDs_btag-nom_phSF-nom/backgrounds" % analysis
  response["sigDDdir"]            = "/Users/jhakala/HgammaMacros/organize_%s_DDs_btag-nom_phSF-nom/signals" % analysis
  response["dataDDdir"]           = "/Users/jhakala/HgammaMacros/organize_%s_DDs_btag-nom_phSF-nom/data/" % analysis
  response["dataDDFile"]          = "/Users/jhakala/HgammaMacros/organize_%s_DDs_btag-nom_phSF-nom/data/ddTree_data_2017.root" % analysis
  return response

def getNormalizations():
  normalizations = {}
  normalizations["700"]  = 1.0
  normalizations["800"]  = 1.0
  normalizations["900"]  = 1.0
  normalizations["1000"] = 0.8
  normalizations["1200"] = 0.8
  normalizations["1400"] = 0.4
  normalizations["1600"] = 0.4
  #normalizations["1800"] = 0.4
  normalizations["2000"] = 0.2
  normalizations["2200"] = 0.2
  normalizations["2600"] = 0.2
  normalizations["3000"] = 0.2  
  normalizations["3500"] = 0.2  
  return normalizations

def getMassWindows():
  # TODO: this needs updating for the new signals
  massWindows = {}
  massWindows[700]  = [650,   750]
  massWindows[800]  = [750,   850]
  massWindows[900] =  [825,   975]
  massWindows[1000] = [900,  1100]
  massWindows[1200] = [1100, 1300]
  massWindows[1400] = [1300, 1600]
  massWindows[1600] = [1400, 1800]
  #massWindows[1800] = [1600, 2000]
  massWindows[2000] = [1800, 2200]
  massWindows[2400] = [2100, 2700]
  massWindows[2600] = [2300, 2900]
  massWindows[3000] = [2600, 3400]
  massWindows[3500] = [2800, 4200]
  return massWindows

def getSigNevents(analysis):
  sigNevents = {}
  for mass in getNormalizations().keys():
    flattuple = TFile("%s/smallified_%s-%s.root"%(getSamplesDirs()["signalsSmall3sDir"], analysis, mass))
    hCounter = flattuple.Get("ntuplizer/hCounter")
    sigNevents[mass] = hCounter.GetBinContent(1)
  return sigNevents

def getVariableDict():
  varDict = {}
  varDict["bJet_abseta"]    = "#||{#eta_{J}}"
  varDict["bJet_eta"]       = "#eta_{J}"
  varDict["bJet_phi"]       = "#phi_{J}"
  varDict["bJet_pt"]        = "p_{T}^{J}"
  varDict["leadingPhEta"]              = "#eta_{#gamma}"
  varDict["bJet_DDBtag"]           = "DDB discriminant"
  varDict["phJetDeltaR"]         = "#DeltaR(#gamma, jet)"
  varDict["leadingPhPt"]               = "p_{T}^{#gamma} (GeV)"
  varDict["bJett2t1"]              = "#tau_{21}"
  varDict["leadingPhAbsEta"]           = "#||{#eta_{#gamma}}"
  varDict["phPtOverMgammaj"]           = "p_{T}^{#gamma}/m_{#gammaJ}  "
  varDict["leadingPhPhi"]              = "#phi_{#gamma}"
  varDict["cosThetaStar"]              = "#||{cos(#theta*)}"
  varDict["phJetInvMass_softdrop"] = "m_{#gammaJ} (GeV)"
  varDict["softdropJetCorrMass"]    = "m_{J}^{PUPPI+SD} (GeV)"
  varDict["mcWeight"]    = "weight on MC background event"
  return varDict

def isVarTagger(varName):

  label =   "b" # stands for "boost"
  taggers = [
      "%sJet_DDBtag"%label,
      "%sJet_decDDBtag"%label,
      "%sJet_csvbb"%label,
      "%sJet_akx_probHbb"%label,
      "%sJet_akx_HbbvsQCD"%label,
      "%sJet_akx_H4qvsQCD"%label,
      "%sJet_akx_probZbb"%label,
      "%sJet_akx_probZqq"%label,
      "%sJet_akx_probZcc"%label,
      "%sJet_akx_ZvsQCD"%label,
      "%sJet_akx_ZbbvsQCD"%label,
      "%sJet_akx_probWcq"%label,
      "%sJet_akx_probWqq"%label,
      "%sJet_akx_WvsQCD"%label
      ]
  if varName in taggers:
    return True
  else:
    return False


def getHiggsRangesDict(fineBinning=False):
  rangesDict = {}
  rangesDict["mcWeight"]                 = [[-9999999., 9999999.]]
  rangesDict["cosThetaStar"]                 = [[0., 1.]]
  rangesDict["phPtOverMgammaj"]              = [[0., 1.2]]
  rangesDict["leadingPhPhi"]                 = [[-3.5, 3.5]]
  rangesDict["leadingPhPt"]                  = [[0., 3000.]]
  rangesDict["leadingPhAbsEta"]              = [[0.,2.5]]
  rangesDict["leadingPhEta"]                 = [[-2.8,2.8]]
  rangesDict["antibtagSF"]                   = [[0.0, 1.0]]
  rangesDict["btagSF"]                       = [[0.0, 1.0]]
  rangesDict["weightFactor"]                 = [[0.0, 2.0]]
  label =   "b" # stands for "boost"
  rangesDict["%sJet_DDBtag"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_decDDBtag"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_csvbb"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probHbb"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_HbbvsQCD"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_H4qvsQCD"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probZbb"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probZqq"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probZcc"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_ZvsQCD"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_ZbbvsQCD"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probWcq"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_probWqq"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_akx_WvsQCD"%label]           = [[-1. , 1.]]
  rangesDict["%sJet_abseta"%label]=[[0., 3]]
  rangesDict["%sJet_eta"%label]       = [[-3., 3.]]
  rangesDict["%sJet_phi"%label]       = [[-3.5, 3.5]]
  rangesDict["%sJet_pt"%label]        = [[0., 4000.]]
  rangesDict["%sJett2t1"%label]              = [[0.0, 1.0]]
  #rangesDict["%sPrunedJetCorrMass"%label]    = [[0.,200.], [0.,1000.]]
  #rangesDict["%sPuppi_softdropJetCorrMass"%label]=[[50.,150.]]
  rangesDict["softdropJetCorrMass"]    = [[0.,1000.]]
  rangesDict["phJetDeltaR"]         = [[0.,6.]]
  if fineBinning:
    rangesDict["phJetInvMass_softdrop"]=[[700., 4700.]]
  else:
    rangesDict["phJetInvMass_softdrop"]=[[0., 10000.]]
  return rangesDict

def getRangesDict(fineBinning=False):
  rangesDict = {}
  higgsRangesDict = getHiggsRangesDict(fineBinning)
  for key in higgsRangesDict.keys():
    rangesDict[key]=higgsRangesDict[key]
  return rangesDict
