import copy
from ROOT import TCut
# functions to define the selection cuts for H(bb)Gamma 
# John Hakala 7/13/16

def getCutValues():
  cutValues = {}
  cutValues["minInvMass"]     = 720.0
  #cutValues["minInvMass"]     = 500.0
  cutValues["phEta"]          = 1.4442
  cutValues["phPt"]           = 200.0
  cutValues["jetAbsEta"]      = 2.2
  cutValues["jetPt"]          = 250.0
  cutValues["deltaR"]         = 1.1
  cutValues["ptOverM"]        = 0.35
  cutValues["DDB"]            = 0.9
  #cutValues["higgsWindow"]    = [110.0, 140.0]
  #cutValues["sidebandWindow"] = [100.0, 110.0]
  #cutValues["sideband5070Window"] = [50.0, 70.0]
  #cutValues["sideband80100Window"] = [80.0, 100.0]
  #cutValues["preselectionWindow"] = [30.0, 99999.9]
  return cutValues


def combineCuts(cutDict):
  combinedCut = TCut()
  for cut in cutDict.keys():
    combinedCut += cutDict[cut]
  return combinedCut

def getVarKeys():
  varKeys = {}
  varKeys["higgsJett2t1"]              = "t2t1"
  varKeys["higgsJet_DDBtag"]           = "btagHolder"
  varKeys["cosThetaStar"]              = "cosThetaStar"
  varKeys["phPtOverMgammaj"]           = "ptOverM"
  varKeys["leadingPhEta"]              = "phEta"
  varKeys["leadingPhPhi"]              = "phPhi"
  varKeys["leadingPhPt"]               = "phPt"
  varKeys["leadingPhAbsEta"]           = "phEta"
  varKeys["phJetInvMass_softdrop_higgs"] = "turnon"
  varKeys["phJetDeltaR_higgs"]         = "deltaR"
  varKeys["higgsJet_abseta"]    = "jetAbsEta"
  varKeys["higgsJet_eta"]       = "jetEta"
  varKeys["higgsJet_phi"]       = "jetPhi"
  varKeys["higgsJet_pt"]        = "jetPt"
  varKeys["higgs_softdropJetCorrMass"]    = "higgsWindow"
  return varKeys

def makeHiggsWindow(sideband=False, windowEdges=[100.0,110.0]):
    #print "makeHiggsWindow got sideband =", sideband, "and windowEdges =", windowEdges
    cutValues = getCutValues()
    cuts = {}
    #window = "higgsWindow"
    #if sideband:
    #  if windowEdges == [100.0,110.0]:
    #    window = "sidebandWindow"
    #  elif windowEdges == [50.0,70.0]:
    #    window = "sideband5070Window"
    #  elif windowEdges == [80.0,100.0]:
    #    window = "sideband80100Window"
    #  elif windowEdges == [30.0,99999.9]:
    #    window = "preselectionWindow"
    cuts["higgsWindowLow"] = TCut( "higgs_softdropJetCorrMass>%f"   % windowEdges[0] )
    cuts["higgsWindowHi"]  = TCut( "higgs_softdropJetCorrMass<%f"   % windowEdges[1] )
    #print "will return combineCuts(cuts)=", combineCuts(cuts)
    return combineCuts(cuts)

def makeTrigger(which = "OR"):
  # TODO TODO fix this "which = OR" business
  cutValues = getCutValues()
  cuts = {}
  if which == "OR":
    #cuts["trigger"] = TCut( "triggerFired_175 > 0.5 || triggerFired_165HE10 > 0.5" )
    cuts["trigger"] = TCut( "triggerFired_200 > 0.5" )
  return combineCuts(cuts)
    

def getDefaultCuts(region, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    cutValues = getCutValues()

    cuts = {} 
    cuts["phEta"]           = TCut( "leadingPhAbsEta<%f"           % cutValues["phEta"]      )
    cuts["ptOverM"]         = TCut( "phPtOverMgammaj>%f"           % cutValues["ptOverM"]    )
    cuts ["phPt"]           = TCut("leadingPhPt>%f"                % cutValues["phPt"]       )
    cuts ["phPhi"]          = TCut()
    cuts ["t2t1"]           = TCut()
    cuts ["jetPhi"]         = TCut()
    cuts ["jetEta"]         = TCut()
    cuts ["btagHolder"]     = TCut()
    cuts ["cosThetaStar"]   = TCut()
    if useTrigger: 
      cuts["trigger"]         = makeTrigger()
    if region is "higgs":
      cuts["turnon"]   = TCut( "phJetInvMass_softdrop_higgs>%f"      % cutValues["minInvMass"]     )
      cuts["deltaR"]   = TCut( "phJetDeltaR_higgs>%f"              % cutValues["deltaR"]         )
      cuts["jetAbsEta"]       = TCut( "higgsJet_abseta<%f"         % cutValues["jetAbsEta"]      )
      cuts["btag"]     = TCut( "higgsJet_DDBtag>%f"                % cutValues["DDB"]            )
      cuts["antibtag"] = TCut( "higgsJet_DDBtag<%f"                % cutValues["DDB"]            )
      cuts ["jetPt"]          = TCut("higgsJet_pt>%f"          % cutValues["jetPt"]      )
      #cuts["higgsWindowLow"] = TCut( "higgsPuppi_softdropJetCorrMass>%f"   % cutValues["higgsWindow"][0] )
      #cuts["higgsWindowHi"]  = TCut( "higgsPuppi_softdropJetCorrMass<%f"   % cutValues["higgsWindow"][1] )
      cuts["higgsWindow"]     = makeHiggsWindow(sideband, windowEdges)
    elif region is "side5070" or region is "side100110":
      if region is "side5070":
        index = "Three"
      else:
        index = "Four"
      cuts["turnon"]   = TCut( "phJetInvMass_softdrop_sideLow%s>%f" % (index, cutValues["minInvMass"] ))
      cuts["deltaR"]   = TCut( "phJetDeltaR_sideLow%s>%f"         % (index, cutValues["deltaR"]     ))
      cuts["jetEta"]   = TCut( "sideLow%sJet_abseta<%f"    % (index, cutValues["jetEta"]     ))
      cuts["btag"]     = TCut( "sideLow%sJet_DDBtag>%f"           % (index, cutValues["DDB"]        ))
      cuts["antibtag"] = TCut( "sideLow%sJet_DDBtag<%f"           % (index, cutValues["DDB"]        ))
    else:
      print "Invalid region!!!"
      quit()
    return cuts
    
def getBtagComboCut(region, useTrigger, sideband=False, scaleFactors=False, windowEdges=[100,110]):
    if windowEdges == "signalRegion":
      windowEdges = [110.0, 140.0]
    btagCuts = copy.deepcopy(getDefaultCuts(region, useTrigger, sideband, windowEdges))
    btagCuts.pop("antibtag")
    if scaleFactors:
      btagCuts.pop("btag")
    return combineCuts(btagCuts)

def getAntiBtagComboCut(region, useTrigger, sideband=False, scaleFactors=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = [110.0, 140.0]
    antibtagCuts = copy.deepcopy(getDefaultCuts(region, useTrigger, sideband, windowEdges))
    antibtagCuts.pop("btag")
    if scaleFactors:
      antibtagCuts.pop("antibtag")
    return combineCuts(antibtagCuts)

def getNoBtagComboCut(region, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = [110.0, 140.0]
    nobtagCuts = copy.deepcopy(getDefaultCuts(region, useTrigger, sideband, windowEdges))
    nobtagCuts.pop("btag")
    nobtagCuts.pop("antibtag")
    return combineCuts(nobtagCuts)

def getNminus1ComboCut(region, popVar, withBtag, useTrigger, sideband=False, windowEdges=[100.0,110.0]):
    if windowEdges == "signalRegion":
      windowEdges = [110.0, 140.0]
    nobtagCuts = copy.deepcopy(getDefaultCuts(region, useTrigger, sideband, windowEdges))
    nobtagCuts.pop("antibtag")
    if not withBtag:
      nobtagCuts.pop("btag")
    if not "SF" in popVar and not "weightFactor" in popVar and not "mcWeight" in popVar:
      nobtagCuts.pop(getVarKeys()[popVar])
    return combineCuts(nobtagCuts)

def getPreselectionComboCut(region, useTrigger, sideband=False, windowEdges=[30.0,99999.9] ):
    preselectionCuts = copy.deepcopy(getDefaultCuts(region, useTrigger, sideband, windowEdges))
    preselectionCuts.pop("phEta")
    preselectionCuts.pop("ptOverM")
    preselectionCuts.pop("turnon")
    preselectionCuts.pop("btag")
    preselectionCuts.pop("antibtag")
    preselectionCuts.pop("jetAbsEta")
    return combineCuts(preselectionCuts)

