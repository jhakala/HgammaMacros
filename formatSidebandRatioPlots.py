from ROOT import *

categories = ["antibtag", "btag"]
for category in categories:
  inFile = TFile("sbRatios/%s_sb_ratios_100-110_over_50-70.root" % category)
  inFile.ls()

  hists = {}
  ratioHist = inFile.Get("ratio_100-110_over_50-70_%s" % category)
  for sideband in ["5070", "100110"]:
    hists[sideband] = inFile.Get("%sHist%s" % (category, sideband))

  print ratioHist
  print hists

  gStyle.SetOptStat(0)
  gROOT.ForceStyle()
  canvas = TCanvas()
  canvas.cd()
  topPad =  TPad("stack", "stack", 0, 0.3, 1, 1.0)
  bottomPad = TPad("ratio", "ratio", 0, 0, 1, 0.3)
  bottomPad.SetBottomMargin(0.2)
  topPad.Draw()
  bottomPad.Draw()
  topPad.cd()
  topPad.SetLogy()
  gStyle.SetOptStat(0)
  hists["5070"].SetTitle("sideband 50 GeV < m_{j} < 70 GeV")
  hists["5070"].SetStats(False)
  hists["5070"].GetXaxis().SetTitle("m_{j#gamma} (GeV)")
  hists["5070"].GetXaxis().SetTitleSize(hists["5070"].GetXaxis().GetTitleSize()*1.3)
  #hists["5070"].GetXaxis().SetTitleOffset(hists["5070"].GetXaxis().GetTitleOffset())
  hists["5070"].GetXaxis().SetLabelSize(hists["5070"].GetXaxis().GetTitleSize())
  hists["5070"].GetYaxis().SetLabelSize(0.055)
  hists["5070"].GetYaxis().SetTitleOffset(0.55)
  hists["5070"].GetYaxis().SetTitle("Events / %i GeV" % hists["5070"].GetBinWidth(1))
  hists["5070"].GetYaxis().SetTitleSize(0.065)
  hists["5070"].SetMarkerStyle(20)
  hists["5070"].Draw("PE1")
  hists["5070"].SetMarkerColor(kGray)
  hists["5070"].SetLineColor(kGray)

  hists["100110"].SetTitle("sideband 100 GeV < m_{j} < 110 GeV [normalized]")
  hists["100110"].SetMarkerStyle(20)
  hists["100110"].Draw("PE1 SAME")
  hists["100110"].SetMarkerColor(kBlack)
  hists["100110"].SetLineColor(kBlack)
  
  topPad.BuildLegend(0.40, 0.55, 0.85, 0.85)
  hists["5070"].SetTitle("Sideband m_{j#gamma} comparison")
  topPad.Modified()
  topPad.Update()


  bottomPad.cd()
  ratioHist.SetTitle("")
  if "antibtag" in category:
    ratioHist.GetYaxis().SetRangeUser(0, (ratioHist.GetBinContent(1)+ratioHist.GetBinError(1))*2)
  else:
    ratioHist.GetYaxis().SetRangeUser(0, (ratioHist.GetBinContent(1)+ratioHist.GetBinError(1))*3)
  ratioHist.GetYaxis().SetLabelSize(ratioHist.GetYaxis().GetLabelSize()*2.5)
  ratioHist.GetXaxis().SetLabelSize(ratioHist.GetYaxis().GetLabelSize())
  ratioHist.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
  ratioHist.GetXaxis().SetTitleSize(ratioHist.GetYaxis().GetLabelSize()*1.1)
  ratioHist.GetXaxis().SetTitleOffset(ratioHist.GetXaxis().GetTitleOffset()*0.8)
  ratioHist.GetYaxis().SetTitle("#splitline{     ratio}{(no normalization)}")
  ratioHist.GetYaxis().SetTitleSize(0.09)
  ratioHist.GetYaxis().SetTitleOffset(0.4)
  ratioHist.GetYaxis().SetNdivisions(808)
  ratioHist.Draw()
  bottomPad.Modified()
  bottomPad.Update()
  
  outPdfName = "sbRatios/twopane_" + category + ".pdf"
  outFileName = "sbRatios/twopane_" + category + ".root"
  canvas.Print(outPdfName)
  outFile = TFile(outFileName, "RECREATE")
  outFile.cd()
  canvas.Write()
  outFile.Close()


