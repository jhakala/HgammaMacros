from ROOT import *

inFiles = {}
inFiles["antibtag"]=TFile("sigEff_antibtag.root")
inFiles["btag"]=TFile("sigEff_btag.root")

canvases = {}
graphs = {}
for category in inFiles.keys():
  for key in inFiles[category].GetListOfKeys():
    if "TCanvas" in inFiles[category].Get(key.GetName()).IsA().GetName():
      canvases[category] = inFiles[category].Get(key.GetName())
      for prim in canvases[category].GetListOfPrimitives():
        print "--------"
        print prim.GetName()
        print prim.IsA().GetName()
        if "TGraph" in prim.IsA().GetName():
          graphs[category] = prim

print graphs


gStyle.SetOptFit(0)
gStyle.SetOptStat(0)
canvases["antibtag"].Draw()
gStyle.SetOptFit(0)
gStyle.SetOptStat(0)
graphs["antibtag"].GetYaxis().SetRangeUser(9e-3, 1.1)
graphs["antibtag"].GetYaxis().SetLabelSize(0.07)
graphs["antibtag"].GetYaxis().SetTitle("A#varepsilon")
graphs["antibtag"].GetYaxis().SetTitleSize(.07)
graphs["antibtag"].GetXaxis().SetTitleSize(.08)
graphs["antibtag"].GetXaxis().SetLabelSize(.07)
graphs["antibtag"].GetYaxis().SetTitleOffset(.45)

graphs["btag"].SetTitle("btag")
graphs["antibtag"].SetFillColor(kWhite)
graphs["btag"].SetFillColor(kWhite)
graphs["btag"].Draw("SAME P")
canvases["antibtag"].SetLogy()
graphs["btag"].GetFunction("fitFunctionBtag").SetLineColor(kBlue)
graphs["antibtag"].SetLineColor(kRed)
graphs["btag"].SetLineColor(kBlue)
graphs["antibtag"].SetTitle("antibtag")
canvases["antibtag"].BuildLegend(.65, .90, .90, .65)
graphs["antibtag"].SetTitle("Signal efficiencies")
from tcanvasTDR import TDRify
TDRify(canvases["antibtag"], False, "signalEffs")
for prim in canvases["antibtag"].GetListOfPrimitives():
  print prim.IsA().GetName()
  if "TPaveStats" in prim.IsA().GetName():
    print "found a stats box"
    prim.Delete()
canvases["antibtag"].Print("overlaidSigEffs.pdf")


