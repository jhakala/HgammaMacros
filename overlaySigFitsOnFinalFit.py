from ROOT import *
btagInFile = TFile("~/btagErrs.root")
antiInFile = TFile("~/antibtagErrs.root")

fitDiagnosticFiles = [  
                 TFile("/Users/johakala/feb28/fitDiagnosticsHgamma_antibtag_900.root"),
                 TFile("/Users/johakala/feb28/fitDiagnosticsHgamma_antibtag_1070.root"),
                 TFile("/Users/johakala/feb28/fitDiagnosticsHgamma_antibtag_1220.root"),
                 TFile("/Users/johakala/feb28/fitDiagnosticsHgamma_antibtag_1500.root")
              ]





#fitDiagnosticFiles = [  
#             TFile("/Users/johakala/feb27/fitDiagnosticsHgamma860.root"  ),
#             TFile("/Users/johakala/feb27/fitDiagnosticsHgamma980.root"  ),
#             TFile("/Users/johakala/feb27/fitDiagnosticsHgamma1320.root" ),
#             TFile("/Users/johakala/feb27/fitDiagnosticsHgamma1470.root" )
#          ]
colors = [kRed, kGreen, kCyan, kBlue] 

antiTotalHists = [inFile.Get("shapes_fit_s/Vg/total") for inFile in fitDiagnosticFiles]
#antiTotalHists = [inFile.Get("shapes_fit_s/ch1/total") for inFile in fitDiagnosticFiles]
#btagTotalHists = [inFile.Get("shapes_fit_s/ch2/total") for inFile in fitDiagnosticFiles]
print antiTotalHists

#btagCan = btagInFile.Get("newBtagErrs")
#btagCan.Draw()
antiCan = antiInFile.Get("newAntiErrs")
antiCan.Draw()
for prim in antiCan.GetListOfPrimitives():
  print prim.IsA().GetName(), prim.GetName()
antiPad = antiCan.GetPrimitive("anti_top")
#btagPad = btagCan.GetPrimitive("btag_top")
antiPad.cd()
iColor = 0
for antiHist in antiTotalHists:
  antiHist.SetLineColor(colors[iColor])
  antiHist.SetLineWidth(3)
  iColor+=1
  antiHist.Draw("HIST SAME")
#btagPad.cd()
#iColor = 0
#for btagHist in btagTotalHists:
#  btagHist.SetLineColor(colors[iColor])
#  btagHist.SetLineWidth(3)
#  iColor+=1
#  btagHist.Draw("HIST SAME")

data = {}
for prim in btagPad.GetListOfPrimitives():
  if "SAME PE1" in prim.GetDrawOption():
    data["btag"] = prim

for prim in antiPad.GetListOfPrimitives():
  if "SAME PE1" in prim.GetDrawOption():
    data["anti"] = prim

print data

antiCan.Print("antiOverlay.pdf")
#btagCan.Print("btagOverlay.pdf")

#outFile = TFile("signalPlusBackgroundFits.root", "RECREATE")
outFile = TFile("signalPlusBackgroundFit_antibtag.root", "RECREATE")
antiCan.Write()
#btagCan.Write()
outFile.Close()


