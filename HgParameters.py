# functions to centrally store Hgamma parameters
# John Hakala -  May 16, 2016
from ROOT import *

def getSamplesDirs():
  response = {}
  response["HgammaFlatTuples"] = "~/physics/80Xsignals"
  response["small3sDir"]       = "~/physics/nov21_ntuples"
  response["ddDir"]            = "~/WZgammaMacros/80XDDs_Mar9/"
  response["sigDDdir"]         = "~/WZgammaMacros/80XDDs_Mar9_sigs"
  response["dataDir"]          = "~/WZgammaMacros/80XDDs_Mar9/ddTree_SilverJson.root"
  return response

def getNormalizations():
  normalizations = {}
  #normalizations["650"]  = 1.0
  normalizations["750"]  = 1.0
  normalizations["850"]  = 1.0
  normalizations["1000"] = 0.8
  normalizations["1150"] = 0.8
  normalizations["1300"] = 0.4
  normalizations["1450"] = 0.4
  normalizations["1600"] = 0.4
  normalizations["1750"] = 0.4
  normalizations["1900"] = 0.2
  normalizations["2050"] = 0.2
  normalizations["2450"] = 0.2
  normalizations["2850"] = 0.2  
  normalizations["3250"] = 0.2  
  return normalizations

def getMassWindows():
  # TODO: this needs updating for the new signals
  massWindows = {}
  #massWindows[650]  = [600,   700]
  massWindows[750]  = [700,   800]
  massWindows[850]  = [800,   900]
  massWindows[1000] = [900,  1100]
  massWindows[1150] = [1050, 1250]
  massWindows[1300] = [1175, 1425]
  massWindows[1450] = [1300, 1600]
  massWindows[1600] = [1400, 1800]
  massWindows[1750] = [1550, 1950]
  massWindows[1900] = [1700, 2100]
  massWindows[2050] = [1850, 2250]
  massWindows[2450] = [2200, 2700]
  massWindows[2850] = [2600, 3100]
  massWindows[3250] = [3000, 3500]
  return massWindows

def getSigNevents():
  sigNevents = {}
  for mass in getNormalizations().keys():
    flattuple = TFile("%s/flatTuple_m%s.root"%(getSamplesDirs()["HgammaFlatTuples"], mass))
    hCounter = flattuple.Get("ntuplizer/hCounter")
    sigNevents[mass] = hCounter.GetEntries()
  return sigNevents

def getVariableDict():
  varDict = {}
  varDict["higgsJet_pruned_abseta"]    = "#||{#eta_{J}}"
  varDict["leadingPhEta"]              = "#eta_{#gamma}"
  varDict["higgsJet_HbbTag"]           = "Hb#bar{b} tagger discriminant"
  varDict["phJetDeltaR_higgs"]         = "#DeltaR(#gamma, jet)"
  varDict["leadingPhPt"]               = "p_{T}^{#gamma} (GeV)"
  varDict["higgsJett2t1"]              = "#tau_{21}"
  varDict["leadingPhAbsEta"]           = "#||{#eta_{#gamma}}"
  varDict["phPtOverMgammaj"]           = "p_{T}^{#gamma}/m_{#gammaJ}  "
  varDict["leadingPhPhi"]              = "#phi_{#gamma}"
  varDict["cosThetaStar"]              = "#||{cos(#theta*)}"
  varDict["phJetInvMass_pruned_higgs"] = "m_{#gammaJ} (GeV)"
  varDict["higgsPrunedJetCorrMass"]    = "m_{J}^{pruned} (GeV)"
  return varDict


