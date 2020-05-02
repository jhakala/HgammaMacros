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


