import copy
from ROOT import *
from pyrootTools import *
from HgParameters import *
from HgCuts import getDefaultCuts, combineCuts
from os import path
from sys import argv

# macro for plotting post-selection for H(bb)gamma
# John Hakala 7/13/16

samplesDirs = getSamplesDirs()
#dataFileName = samplesDirs["dataDir"]
#mass = "1000"
#sampleFileName=path.join(samplesDirs["dataDDdir"], "ddTree_data2016SinglePhoton.root")
#sampleFileName="testSilver.root"
sampleFileName=argv[1]

#cuts = getDefaultCuts("higgs", True, False, [110., 140.])
cuts = getDefaultCuts("higgs", True, False, [140., 150.])

btagCuts = copy.deepcopy(cuts)
btagCuts.pop("antibtag")
btagComboCut = combineCuts(btagCuts)
print btagComboCut

antibtagCuts = copy.deepcopy(cuts)
antibtagCuts.pop("btag")
antibtagComboCut = combineCuts(antibtagCuts)
print antibtagComboCut

notagCuts = copy.deepcopy(btagCuts)
notagCuts.pop("btag")
notagComboCut = combineCuts(notagCuts)
print notagComboCut

sampleFile = TFile(sampleFileName)
print "sampleFileName %s:" % sampleFileName,
print sampleFile
higgsTree = sampleFile.Get("higgs")
print "higgsTree: ",
print higgsTree
print "\nall cuts, btag cat:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", btagComboCut)
print btagComboCut
print "----------"
print "\nall cuts, antibtag cat:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", antibtagComboCut)
print antibtagComboCut
print "----------"
print "\nno btag cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
print notagComboCut
print "----------"

#print notagComboCut
#print notagCuts

notagCuts.pop("ptOverM")
notagComboCut = combineCuts(notagCuts)
print "\nno pT/M cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)

#print notagComboCut
#print notagCuts

#notagCuts.pop("deltaR")
#notagComboCut = combineCuts(notagCuts)
#print "\nno deltaR cut\n   "
#print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
#
#print notagComboCut
#print notagCuts

notagCuts.pop("phEta")
notagComboCut = combineCuts(notagCuts)
print "\nno phEta cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
print notagComboCut
print "---------"

#print notagComboCut
#print notagCuts

notagCuts.pop("jetAbsEta")
notagComboCut = combineCuts(notagCuts)
print "\nno jetEta cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
print notagComboCut
print "---------"

#print notagComboCut
#print notagCuts

notagCuts.pop("turnon")
notagComboCut = combineCuts(notagCuts)
print "\nno turnon cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
print notagComboCut
print "---------"

#print notagComboCut
#print notagCuts

notagCuts.pop("higgsWindow")
notagComboCut = combineCuts(notagCuts)
print "\nno higgs window cut:   ",
print higgsTree.Draw("phJetInvMass_puppi_softdrop_higgs", notagComboCut)
print notagComboCut
print "---------"


#print notagComboCut
#print notagCuts

