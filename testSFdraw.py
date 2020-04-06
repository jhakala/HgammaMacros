from ROOT import *
from HgCuts import *
cat = "antibtag"
#testFile = TFile("organize_DDs/backgrounds/ddTree_qcd1000to2000.root")
testFile = TFile("organize_DDs/backgrounds/ddTree_gJets600ToInf.root")
testTree = testFile.Get("higgs")
testCan = TCanvas()
testCan.cd()

if cat=="antibtag":
  noSFcuts = getAntiBtagComboCut("higgs", True)
elif cat=="btag":
  noSFcuts = getBtagComboCut("higgs", True)
noSFhist = TH1F("noSFhist", "noSFhist", 100, 0, 0)
testTree.Draw("leadingPhPt >> noSFhist", noSFcuts)

nobtagCuts = getNoBtagComboCut("higgs", True)
withSFhist = TH1F("withSFhist", "withSFhist", 100, 0, 0)
#cutString = "%sSF*%s" % (cat, nobtagCuts)
cutString = "%sSF*(%s)" % (cat, nobtagCuts)
print "cutString is: ", cutString
testTree.Draw("leadingPhPt>>withSFhist", cutString)

noSFhist.Draw()
noSFhist.SetLineColor(kRed+1)
withSFhist.Draw("SAME")
withSFhist.SetLineColor(kGreen+2)

tcan2 = TCanvas()
tcan2.cd()
testTree.Draw("antibtagSF")
for i in range(0, 100):
  print withSFhist.GetBinContent(i)
