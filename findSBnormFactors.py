from pprint import pprint
from ROOT import *
from HgCuts import *
import copy


useWeightFactors = True
useTrigger = True
checks = {"mcSig"       : {"window" : [110.0, 140.0], "file" : TFile("organize_mcDDs_btag-nom/allMCbgs_withWeights.root"), 
          "sidebandSetting" : False, "scaleFactorsSetting": True}, 
          "mcSB"       : {"window" : [100.0, 110.0], "file" : TFile("organize_mcDDs_btag-nom/allMCbgs_withWeights.root"), 
          "sidebandSetting" : False, "scaleFactorsSetting": True}, 
          "sideband" : {"window" : [100.0, 110.0], "file" : TFile("organize_DDs_btag-nom/data/ddTree_data2016SinglePhoton.root"), 
          "sidebandSetting" : False, "scaleFactorsSetting": False}}

for kind in checks.keys():
  tree = checks[kind]["file"].Get("higgs")
  hist = TH1F("hist_%s" % kind, "m_{j#gamma}", 500, 0, 5000)
  hist.GetXaxis().SetRangeUser(400, 1400)
  hist.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
  hist.GetYaxis().SetTitle("Events / 10 GeV")
  hist.GetYaxis().SetTitleOffset(1.35)
  
  jetMassWindow = checks[kind]["window"]
  cuts = {}
  hist.SetTitle("m_{j#gamma}, %i GeV < m_{j} < %i GeV" % (int(jetMassWindow[0]), int(jetMassWindow[1])))
  cutNames = ["noPtOverM", "noBtag",  "noPhEta", "noJetEta"]
  defaultCuts = getDefaultCuts("higgs", True, False, checks[kind]["window"])
  defaultCuts.pop("antibtag")
  defaultCuts.pop("btag")
  defaultCuts.pop("ptOverM")
  if "mc" in kind:
    #cuts["noPtOverM"] =  "weightFactor*(mcWeight*(((higgsJet_HbbTag>0.9))*(%s)))" % combineCuts(defaultCuts)
    cuts["noPtOverM"] =  "(weightFactor*mcWeight*((higgsJet_HbbTag>0.9)*(%s)))" % combineCuts(defaultCuts)
  elif "sideband" in kind:
    #cuts["noPtOverM"] = "((higgsJet_HbbTag>0.9)&&(%s))" % combineCuts(defaultCuts)
    cuts["noPtOverM"] = "((higgsJet_HbbTag>0.9)&&(%s))" % combineCuts(defaultCuts)
  cuts["noBtag"] = "mcWeight*(%s)" % combineCuts(defaultCuts)
  print 'cuts["noBtag"]', cuts["noBtag"]
  noPhEtaCuts = copy.deepcopy(defaultCuts)
  noPhEtaCuts.pop("phEta")
  cuts["noPhEta"] = "mcWeight*(%s)" % combineCuts(noPhEtaCuts)
  noJetEtaCuts = copy.deepcopy(defaultCuts)
  print "\n\n noJetEtaCuts :"
  pprint(noJetEtaCuts)
  noJetEtaCuts.pop("jetAbsEta")
  print "\n\n popped noJetEtaCuts :"
  pprint(noJetEtaCuts)
  cuts["noJetEta"] = "mcWeight*(%s)" % combineCuts(noJetEtaCuts)
  print 'cuts["noJetEta"]', cuts["noJetEta"]

  verbose = True
  for cut in cuts.keys():
    checks[kind][cut]={}
    pprint(cuts[cut])
    entries = tree.Draw("phJetInvMass_puppi_softdrop_higgs >>hist_%s" % kind, cuts[cut])
    events = hist.GetSumOfWeights()
    if verbose:
      print "\n-------------------"
      print "cuts:"
      print "got this many entries: ", entries
      print "weighted total: ", events
      print "-------------------\n"
    #events = 0.
    #for iBin in range(0,hist.GetNbinsX()):
    #  events+=hist.GetBinContent(iBin)
    #  print hist.GetBinContent(iBin)
    #checks[kind][cut]["cutString"] = cuts[cut]
    checks[kind][cut]["events"] = events

pprint(checks)
sbScaleFactorsData = {}
sbScaleFactorsMC = {}
for cut in cutNames:
  sbScaleFactorsData[cut] = float(checks["mcSig"][cut]["events"]) / float(checks["sideband"][cut]["events"])
print "current alpha factors"
pprint(sbScaleFactorsData)
for cut in cutNames:
  sbScaleFactorsMC[cut] = float(checks["mcSig"][cut]["events"]) / float(checks["mcSB"][cut]["events"])
print "MC based alpha factors"
pprint(sbScaleFactorsMC)
for cut in cutNames:
  print "percent diff for cutName", cut, " : ", 100*((sbScaleFactorsMC[cut] - sbScaleFactorsData[cut])/sbScaleFactorsMC[cut]), "%"
