from ROOT import *
from makeVgHists import getVgShortName

for category in ["btag", "antibtag"]:

  inFiles = {}
  inFiles["weighted"] = TFile("%s_btag-nom_phSF-nom/%s/histos_sideband110140.root" % (getVgShortName(), category))
  inFiles["unweighted"] = TFile("noTrigWeights_%s_btag-nom_phSF-nom/%s/histos_sideband110140.root" % (getVgShortName(), category))

  outFile = TFile("quantifyWeightFactors_%s.root" % category, "RECREATE")

  
  hists = {}
  rebin = 50
  for inFile in inFiles:
    hists[inFile] = inFiles[inFile].Get("distribs_X")
    hists[inFile].Rebin(rebin)
  
  diff = hists["weighted"].Clone()
  diff.Add(hists["unweighted"], -1)
  diff.Divide(hists["unweighted"])
  diff.SetNameTitle("frac_diff_%s" % category, "frac_diff_%s" % category)
  
  can = TCanvas("can_perecent_diff_%s" % category, "can_perecent_diff_%s" % category)
  can.cd()
  gStyle.SetOptStat(0)
  diff.SetTitle("Effects of weight factors, %s category" % category)
  diff.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
  diff.GetXaxis().SetRangeUser(600, 3000)
  diff.GetYaxis().SetTitle("Fractional difference / %i GeV" % rebin)
  diff.GetYaxis().SetLabelSize(0.028)
  diff.GetYaxis().SetTitleOffset(1.3)
  diff.Draw("hist")
  can.Print("weightFactor_effect_new-%s.pdf" % category)

  dataCan = TCanvas("can_unweighted_data_%s" % category, "can_unweighted_data_%s" % category)
  dataCan.cd()
  hists["unweighted"].SetNameTitle("unweighted_data_%s" % category, "unweighted_data_%s" % category)
  hists["unweighted"].Draw()
  weightedDataCan = TCanvas("can_weighted_data_%s" % category, "can_weighted_data_%s" % category)
  weightedDataCan.cd()
  hists["weighted"].SetNameTitle("weighted_data_%s" % category, "weighted_data_%s" % category)
  hists["weighted"].Draw()
  outFile.cd()
  can.Write()
  dataCan.Write()
  weightedDataCan.Write()
  outFile.Close()
  
