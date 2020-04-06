from ROOT import *
from math import sqrt
from tcanvasTDR import TDRify

inputsDir = "/Users/johakala/feb22/"

tfile=[]
tfile.append(TFile(inputsDir + "rebinnedPdfs_varBins_antibtag.root"))
tfile.append(TFile(inputsDir + "rebinnedPdfs_varBins_btag.root"))

anti = tfile[0].Get("masterCan_antibtag")
antiFit = anti.GetPrimitive("dataFit_antibtag")
for prim in antiFit.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "-------------------------"
antiHist = antiFit.GetPrimitive("histVar")
antiHist.SetTitle("Data") 
antiCurve = antiFit.GetPrimitive("bkg_dijetsimple2_Norm[x]")
antiCurve.SetTitle("Fit function")

btag = tfile[1].Get("masterCan_btag")
btagFit = btag.GetPrimitive("dataFit_btag")
btagHist = btagFit.GetPrimitive("histVar")
btagHist.SetTitle("Data") 
btagCurve = btagFit.GetPrimitive("bkg_dijetsimple2_Norm[x]")
btagCurve.SetTitle("Fit function")

antiErrFile = TFile(inputsDir + "fitRes_antibtag.root")
btagErrFile = TFile(inputsDir + "fitRes_btag.root")

btagErrCan = btagErrFile.Get("c1")
btagErrorCurves = []
for prim in btagErrCan.GetListOfPrimitives():
  print prim.GetName()
  if "errorband" in prim.GetName():
    btagErrorCurves.append(prim)

for btagErrorCurve in btagErrorCurves:
  for i in range(0, btagErrorCurve.GetN()):
    #btagErrorCurve.GetY()[i] *= 50 # the rebin factor
    pass

antiErrCan = antiErrFile.Get("c1")
antiErrorCurves = []
for prim in antiErrCan.GetListOfPrimitives():
  if "errorband" in prim.GetName():
    antiErrorCurves.append(prim)

for antiErrorCurve in antiErrorCurves:
  for i in range(0, antiErrorCurve.GetN()):
    #antiErrorCurve.GetY()[i] *= 50 # the rebin factor
    pass


btagRatio = btag.GetPrimitive("ratioPad_btag")
print "======= btag ratio plot ======="
for prim in btagRatio.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "------------------------"
  if "TH1" in prim.IsA().GetName():
    #prim.GridY()
    prim.GetXaxis().SetRangeUser(720, 2020)
btagRatio.Modified()
btagRatio.Update()
btagRatio.Modified()
btagRatio.Update()

antiRatio = anti.GetPrimitive("ratioPad_antibtag")
print "======= anti ratio plot ======="
for prim in antiRatio.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "------------------------"
  if "TH1" in prim.IsA().GetName():
    prim.GetXaxis().SetRangeUser(720, 3020)
antiRatio.Modified()
antiRatio.Update()
antiRatio.Modified()
antiRatio.Update()

for prim in antiFit.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "-------"
  if "TLegend" in prim.IsA().GetName():
    antiLegend = prim
for prim in btagFit.GetListOfPrimitives():
  print prim.GetName()
  print prim.IsA().GetName()
  print "-------"
  if "TLegend" in prim.IsA().GetName():
    btagLegend = prim

newAntiCan = TCanvas("newAntiErrs", "newAntiErrs", 600, 800)
newAntiCan.cd()
newAntiTopPad = TPad("anti_top", "anti_top", 0, 0.3, 1, 1.0)
newAntiTopPad.Draw()
newAntiTopPad.cd()
newAntiTopPad.SetLogy()
antiErrorCurves[0].SetMarkerColor(kOrange)
antiErrorCurves[0].SetLineColor(kOrange)
antiErrorCurves[0].SetFillColor(kOrange)
antiErrorCurves[0].Draw("Af")
antiErrorCurves[0].GetXaxis().SetRangeUser(675, 3080)
antiErrorCurves[0].GetXaxis().SetLabelSize(antiErrorCurves[0].GetXaxis().GetLabelSize()*1.1)
antiErrorCurves[0].GetXaxis().SetTitle("m_{j#gamma} (GeV)")
antiErrorCurves[0].GetXaxis().SetTitleSize(antiErrorCurves[0].GetXaxis().GetTitleSize()*1.2)
antiErrorCurves[0].GetYaxis().SetRangeUser(0.07/50., 4e4/50.)
antiErrorCurves[0].GetYaxis().SetTitle("Events / GeV")
antiErrorCurves[0].GetYaxis().SetTitleSize(antiErrorCurves[0].GetYaxis().GetTitleSize()*1.5)
antiErrorCurves[0].GetYaxis().SetTitleOffset(1)
antiErrorCurves[0].GetYaxis().SetLabelSize(antiErrorCurves[0].GetYaxis().GetLabelSize()*1.2)
antiErrorCurves[1].SetMarkerColor(kGreen+2)
antiErrorCurves[1].SetLineColor(kGreen+2)
antiErrorCurves[1].SetFillColor(kGreen+2)
antiErrorCurves[1].Draw("f")
antiCurve.Draw("SAME")
antiHist.Draw("SAME PE1")
TDRify(newAntiTopPad, False, "newAntiTopPad")
antiLegend.Draw()
for prim in antiLegend.GetListOfPrimitives():
  if "Projection of bkg_dijetsimple2" in prim.GetLabel():
    prim.SetLabel("dijet2 fit")
  if "antibtag category: fits" in prim.GetLabel():
    prim.SetLabel("antibtag category")
newAntiCan.cd()
antiRatio.Draw()
TDRify(antiRatio, True, "newAntiBottomPad")


newBtagCan = TCanvas("newBtagErrs", "newBtagErrs", 600, 800)
newBtagCan.cd()
newBtagTopPad = TPad("btag_top", "btag_top", 0, 0.3, 1, 1.0)
newBtagTopPad.Draw()
newBtagTopPad.cd()
newBtagTopPad.SetLogy()
btagErrorCurves[0].SetMarkerColor(kOrange)
btagErrorCurves[0].SetLineColor(kOrange)
btagErrorCurves[0].SetFillColor(kOrange)
btagErrorCurves[0].Draw("Af")
btagErrorCurves[0].GetXaxis().SetRangeUser(675, 2080)
btagErrorCurves[0].GetXaxis().SetLabelSize(antiErrorCurves[0].GetXaxis().GetLabelSize())
btagErrorCurves[0].GetXaxis().SetTitle("m_{j#gamma} (GeV)")
btagErrorCurves[0].GetXaxis().SetTitleSize(antiErrorCurves[0].GetXaxis().GetTitleSize())
btagErrorCurves[0].GetXaxis().SetTitleOffset(antiErrorCurves[0].GetXaxis().GetTitleOffset())
btagErrorCurves[0].GetYaxis().SetTitleOffset(antiErrorCurves[0].GetYaxis().GetTitleOffset())
btagErrorCurves[0].GetYaxis().SetRangeUser(0.07/50., 1.2e3/50.)
btagErrorCurves[0].GetYaxis().SetTitle("Events / GeV")
btagErrorCurves[0].GetYaxis().SetTitleSize(antiErrorCurves[0].GetYaxis().GetTitleSize())
btagErrorCurves[0].GetYaxis().SetTitleOffset(antiErrorCurves[0].GetYaxis().GetTitleOffset())
btagErrorCurves[0].GetYaxis().SetLabelSize(antiErrorCurves[0].GetYaxis().GetLabelSize())
btagErrorCurves[1].SetMarkerColor(kGreen+2)
btagErrorCurves[1].SetLineColor(kGreen+2)
btagErrorCurves[1].SetFillColor(kGreen+2)
btagErrorCurves[1].Draw("f")
btagCurve.Draw("SAME")
btagHist.Draw("SAME PE1")
TDRify(newBtagTopPad, False, "newBtagTopPad")
btagLegend.Draw()
for prim in btagLegend.GetListOfPrimitives():
  if "Projection of bkg_dijetsimple2" in prim.GetLabel():
    prim.SetLabel("dijet2 fit")
  if "btag category: fits" in prim.GetLabel():
    prim.SetLabel("btag category")
newBtagCan.cd()
btagRatio.Draw()
TDRify(btagRatio, True, "newBtagBottomPad")

titleSize = 0
titleOffset = 0
for prim in antiRatio.GetListOfPrimitives():
  print prim.GetName(), prim.IsA().GetName()
  if "copy" in prim.GetName():
    newAntiCan.RecursiveRemove(prim)
    newAntiCan.Modified()
    newAntiCan.Update()
  elif "TH" in prim.IsA().GetName():
    prim.GetYaxis().SetTitleOffset(prim.GetYaxis().GetTitleOffset()*1.2) 
    prim.GetXaxis().SetRangeUser(675, 3000) 
    prim.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
    newAntiCan.Modified()
    newAntiCan.Update()
    titleSize = prim.GetXaxis().GetTitleSize()
    titleOffset = prim.GetXaxis().GetTitleOffset()

for prim in btagRatio.GetListOfPrimitives():
  print prim.GetName(), prim.IsA().GetName()
  if "copy" in prim.GetName():
    newBtagCan.RecursiveRemove(prim)
    newBtagCan.Modified()
    newBtagCan.Update()
  elif "TH" in prim.IsA().GetName():
    prim.GetYaxis().SetTitleOffset(prim.GetYaxis().GetTitleOffset()*1.2) 
    prim.GetXaxis().SetRangeUser(675, 2000) 
    prim.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
    prim.GetXaxis().SetTitleSize(titleSize)
    prim.GetXaxis().SetTitleSize(titleOffset)
    newBtagCan.Modified()
    newBtagCan.Update()

btagUpErr = TGraph()
btagUpErr.SetNameTitle("err_btag_up", "err_btag_up")
btagDownErr = TGraph()
btagDownErr.SetNameTitle("err_btag_down", "err_btag_down")
antiUpErr = TGraph()
antiUpErr.SetNameTitle("err_anti_up", "err_anti_up")
antiDownErr = TGraph()
antiDownErr.SetNameTitle("err_anti_down", "err_anti_down")

x = Double()
y = Double()
for i in range (0, btagErrorCurves[1].GetN()/2):
  btagErrorCurves[1].GetPoint(i, x, y)
  btagDownErr.SetPoint(i, x, y)
  btagErrorCurves[1].GetPoint(i+antiErrorCurves[1].GetN()/2, x, y)
  btagUpErr.SetPoint(i, x, y)
for i in range (0, antiErrorCurves[1].GetN()/2):
  antiErrorCurves[1].GetPoint(i, x, y)
  antiDownErr.SetPoint(i, x, y)
  antiErrorCurves[1].GetPoint(i+antiErrorCurves[1].GetN()/2, x, y)
  antiUpErr.SetPoint(i, x, y)

testCan = TCanvas()
newAntiRatio = antiHist.Clone()
newAntiFitHist = antiHist.Clone()
testCan.cd()
newAntiRatio.Draw()
antiCurve.Draw("SAME")
antiCurve.Integral(1000, 1200)
for iBin in range(0, newAntiRatio.GetNbinsX()):
  average = antiCurve.average(newAntiRatio.GetXaxis().GetBinLowEdge(iBin), newAntiRatio.GetXaxis().GetBinUpEdge(iBin))
  print "average:", average
  newAntiFitHist.SetBinContent(iBin, average)
  newAntiFitHist.SetBinError(iBin, 0.5*(antiUpErr.Eval(newAntiRatio.GetXaxis().GetBinCenter(iBin))-antiDownErr.Eval(newAntiRatio.GetXaxis().GetBinCenter(iBin))))
newAntiFitHist.SetMarkerColor(kRed)
newAntiFitHist.Draw("SAME")
newAntiRatio.Divide(newAntiFitHist)
antiRatio.cd()
antiRatio.Clear()
antiRatio.SetGridy()
newAntiRatio.Draw()
newAntiRatio.GetYaxis().SetRangeUser(0,2)
newAntiRatio.GetYaxis().SetRangeUser(0,2)
newAntiRatio.GetYaxis().SetTitle("data/fit")
newAntiRatio.GetYaxis().SetLabelSize(0.15)
newAntiRatio.GetYaxis().SetTitleOffset(0.25)
newAntiRatio.GetYaxis().SetTitleSize(.2)
newAntiRatio.SetStats(kFALSE)
newAntiRatio.GetXaxis().SetLabelSize(0.10)
newAntiRatio.GetXaxis().SetTitleSize(0.13)
newAntiRatio.GetXaxis().SetTitleOffset(2)
newAntiRatio.GetYaxis().SetLabelSize(0.1)
newAntiRatio.GetYaxis().SetNdivisions(405)
newAntiRatio.SetMarkerSize(.2)
newAntiRatio.Draw("PE1")


testCan = TCanvas()
newBtagRatio = btagHist.Clone()
newBtagFitHist = btagHist.Clone()
testCan.cd()
newBtagRatio.Draw()
btagCurve.Draw("SAME")
btagCurve.Integral(1000, 1200)
for iBin in range(0, newBtagRatio.GetNbinsX()):
  average = btagCurve.average(newBtagRatio.GetXaxis().GetBinLowEdge(iBin), newBtagRatio.GetXaxis().GetBinUpEdge(iBin))
  print "average:", average
  newBtagFitHist.SetBinContent(iBin, average)
  newBtagFitHist.SetBinError(iBin, 0.5*(btagUpErr.Eval(newBtagRatio.GetXaxis().GetBinCenter(iBin))-btagDownErr.Eval(newBtagRatio.GetXaxis().GetBinCenter(iBin))))
newBtagFitHist.SetMarkerColor(kRed)
newBtagFitHist.Draw("SAME")
newBtagRatio.Divide(newBtagFitHist)
btagRatio.cd()
btagRatio.Clear()
btagRatio.SetGridy()
newBtagRatio.Draw()
newBtagRatio.GetYaxis().SetRangeUser(0,2)
newBtagRatio.GetYaxis().SetRangeUser(0,2)
newBtagRatio.GetYaxis().SetTitle("data/fit")
newBtagRatio.GetYaxis().SetLabelSize(0.15)
newBtagRatio.GetYaxis().SetTitleOffset(0.25)
newBtagRatio.GetYaxis().SetTitleSize(.2)
newBtagRatio.SetStats(kFALSE)
newBtagRatio.GetXaxis().SetLabelSize(0.10)
newBtagRatio.GetXaxis().SetTitleSize(0.13)
newBtagRatio.GetXaxis().SetTitleOffset(2)
newBtagRatio.GetYaxis().SetLabelSize(0.1)
newBtagRatio.GetYaxis().SetNdivisions(405)
newBtagRatio.SetMarkerSize(.2)
newBtagRatio.Draw("PE1")


outFile = TFile("finalFits.root", "RECREATE")
outFile.cd()
newBtagCan.Print("btag_fit_errs.pdf")
newBtagCan.Write()
newAntiCan.Print("antibtag_fit_errs.pdf")
newAntiCan.Write()
outFile.Close()
