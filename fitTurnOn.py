from ROOT import *
from glob import glob
from HgCuts import *

inFiles = glob("organize_DDs_btag-nom/signals/*")
chain = TChain("higgs")
for inFile in inFiles:
  chain.Add(inFile)

histNoTrig = TH1F("noTrig", "noTrig", 5000, 0, 5000)
histYesTrig = TH1F("yesTrig", "yesTrig", 5000, 0, 5000)
histNoTrigRebin = TH1F("noTrigRebin", "noTrigRebin", 5000, 0, 5000)
histYesTrigRebin = TH1F("yesTrigRebin", "yesTrigRebin", 5000, 0, 5000)

chain.Draw("leadingPhPt >>noTrig", getNoBtagComboCut("higgs", False))
chain.Draw("leadingPhPt >>yesTrig", getNoBtagComboCut("higgs", True))
chain.Draw("leadingPhPt >>noTrigRebin", getNoBtagComboCut("higgs", False))
chain.Draw("leadingPhPt >>yesTrigRebin", getNoBtagComboCut("higgs", True))

histNoTrigRebin.Rebin(10)
histYesTrigRebin.Rebin(10)

#histYesTrig.Divide(histNoTrig)
eff = TEfficiency(histYesTrig, histNoTrig)
histYesTrigRebin.Divide(histNoTrigRebin)
errorFcn = TF1("erf", "[0]*TMath::Erf((x-[1])/[2])+[3]", 200, 700)
errorFcn.SetParameters(0.5, 250, 15, 0.5)

can = TCanvas()
can.cd()
eff.Draw()
#for i in range(0, 100):
#  eff.Fit(errorFcn, "IR")
fitResult = eff.Fit(errorFcn, "SIR")

histYesTrigRebin.SetLineColor(kRed)
eff.SetLineColorAlpha(kBlack, 0.3)
histYesTrigRebin.Draw("SAME")

print fitResult
fitResult.Print()
