from ROOT import *
from math import sqrt
btagInFile = TFile("newBtagErrs.root")
antiInFile = TFile("newAntiErrs.root")

antiFiles = [TFile("vgVarBinsNew/antibtag/histos_sig_m850.root"),
             TFile("vgVarBinsNew/antibtag/histos_sig_m1000.root"),
             TFile("vgVarBinsNew/antibtag/histos_sig_m1450.root"),
             TFile("vgVarBinsNew/antibtag/histos_sig_m2050.root"),
             ]
#antiFiles = [TFile("vgVarBins/antibtag/histos_sig_m850.root"),
#             TFile("vgVarBins/antibtag/histos_sig_m1000.root"),
#             TFile("vgVarBins/antibtag/histos_sig_m1450.root"),
#             TFile("vgVarBins/antibtag/histos_sig_m2050.root"),
#             ]
btagFiles = [TFile("vgVarBinsNew/btag/histos_sig_m850.root"),
             TFile("vgVarBinsNew/btag/histos_sig_m1000.root"),
             TFile("vgVarBinsNew/btag/histos_sig_m1450.root"),
             TFile("vgVarBinsNew/btag/histos_sig_m2050.root"),
             ]
#btagFiles = [TFile("vgVarBins/btag/histos_sig_m850.root"),
#             TFile("vgVarBins/btag/histos_sig_m1000.root"),
#             TFile("vgVarBins/btag/histos_sig_m1450.root"),
#             TFile("vgVarBins/btag/histos_sig_m2050.root"),
#             ]
colors = [kRed, kGreen, kCyan, kBlue] 
print antiInFile.ls()
print btagInFile.ls()
antiHists = [antiFile.Get("histVar") for antiFile in antiFiles]
btagHists = [btagFile.Get("histVar") for btagFile in btagFiles]
print antiHists

btagCan = btagInFile.Get("newBtagErrs")
btagCan.Draw()
antiCan = antiInFile.Get("newAntiErrs")
antiCan.Draw()
for prim in antiCan.GetListOfPrimitives():
  print prim.IsA().GetName(), prim.GetName()
antiPad = antiCan.GetPrimitive("anti_top")
btagPad = btagCan.GetPrimitive("btag_top")
antiPad.cd()
iColor = 0
for antiHist in antiHists:
  antiHist.SetLineColor(colors[iColor])
  antiHist.SetLineWidth(3)
  iColor+=1
  antiHist.Draw("HIST SAME")
btagPad.cd()
iColor = 0
for btagHist in btagHists:
  btagHist.SetLineColor(colors[iColor])
  btagHist.SetLineWidth(3)
  iColor+=1
  btagHist.Draw("HIST SAME")


errorCurves = {}
backgroundCurves = {}
for prim in btagPad.GetListOfPrimitives():
  if "RooCurve" in prim.IsA().GetName():
    if prim.GetFillColor() == 418:
      errorCurves["btag"]=prim.Clone()
    if prim.GetFillColor() == 0:
      backgroundCurves["btag"]=prim.Clone()
for prim in antiPad.GetListOfPrimitives():
  if "RooCurve" in prim.IsA().GetName():
    if prim.GetFillColor() == 418:
      errorCurves["anti"]=prim.Clone()
    if prim.GetFillColor() == 0:
      backgroundCurves["anti"]=prim.Clone()

xx = Double()
yy = Double()
for key in errorCurves.keys():
  for iPoint in range(0, errorCurves[key].GetN()):
    errorCurves[key].GetPoint(iPoint, xx, yy) 
    errorCurves[key].SetPoint(iPoint, xx, yy/backgroundCurves[key].Eval(xx))


btagCan.GetPrimitive("ratioPad_btag").SetLeftMargin(btagPad.GetLeftMargin())
btagCan.GetPrimitive("ratioPad_btag").SetRightMargin(btagPad.GetRightMargin())
antiCan.GetPrimitive("ratioPad_antibtag").SetLeftMargin(antiPad.GetLeftMargin())
antiCan.GetPrimitive("ratioPad_antibtag").SetRightMargin(antiPad.GetRightMargin())

antiRatioPad = antiCan.GetPrimitive("ratioPad_antibtag")
btagRatioPad = btagCan.GetPrimitive("ratioPad_btag")
print btagRatioPad

ratio = {}
data = {}
for pad in btagCan.GetListOfPrimitives():
  for prim in pad.GetListOfPrimitives():
    if "GetXaxis" in dir(prim):
      prim.GetYaxis().SetTitleOffset(prim.GetYaxis().GetTitleOffset()*1.1)
      if "data" in prim.GetYaxis().GetTitle():
        prim.GetYaxis().SetTitle("Data/Fit")
        ratio["btag"]=prim.Clone()
      elif "TH1" in prim.IsA().GetName() and "PE1" in prim.GetDrawOption():
        data["btag"]=prim
for pad in antiCan.GetListOfPrimitives():
  for prim in pad.GetListOfPrimitives():
    if "GetXaxis" in dir(prim):
      prim.GetYaxis().SetTitleOffset(prim.GetYaxis().GetTitleOffset()*1.1)
      if "data" in prim.GetYaxis().GetTitle():
        prim.GetYaxis().SetTitle("Data/Fit")
        ratio["anti"]=prim.Clone()
      elif "TH1" in prim.IsA().GetName()  and 20 == prim.GetMarkerStyle():
        data["anti"]=prim
#data['btag'].SetBinContent(20, 0.002)
#data['btag'].SetBinError(20, 1.5/60)
antiRatioPad.Clear()
print btagRatioPad
btagRatioPad.Clear()
antiRatioPad.cd()
errorCurves["anti"].Draw("af")
errorCurves["anti"].SetFillColorAlpha(kGray, 0.35)
print btagRatioPad
btagRatioPad.cd()
errorCurves["btag"].Draw("af")
errorCurves["btag"].SetFillColorAlpha(kGray, 0.35)
errorCurves['anti'].GetYaxis().SetRangeUser(0,2)
antiRatioPad.SetGridy()
errorCurves['anti'].GetYaxis().SetNdivisions(405)
errorCurves['anti'].GetYaxis().SetTitleSize(0.20000000298023224)
errorCurves['anti'].GetYaxis().SetTitleOffset(0.2750000059604645)
errorCurves['anti'].GetYaxis().SetLabelSize(0.10000000149011612)
errorCurves['anti'].GetYaxis().SetTitle('Data/Fit')
errorCurves['anti'].GetXaxis().SetLabelSize(0.10000000149011612)
errorCurves['anti'].GetXaxis().SetRangeUser(670, 3077)
errorCurves['btag'].GetYaxis().SetRangeUser(0,2)
print btagRatioPad
btagRatioPad.SetGridy()
errorCurves['btag'].GetYaxis().SetNdivisions(405)
errorCurves['btag'].GetYaxis().SetTitleSize(0.20000000298023224)
errorCurves['btag'].GetYaxis().SetTitleOffset(0.2750000059604645)
errorCurves['btag'].GetYaxis().SetLabelSize(0.10000000149011612)
errorCurves['btag'].GetYaxis().SetTitle('Data/Fit')
errorCurves['btag'].GetXaxis().SetLabelSize(0.10000000149011612)
errorCurves['btag'].GetXaxis().SetRangeUser(680, 2065)


import array
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 751, 783, 816, 851, 886, 923, 961, 1000, 1041, 1083, 1127, 1172, 1218, 1267, 1316, 1368, 1421, 1476, 1533, 1592, 1653, 1716, 1781, 1848, 1918, 1990, 2065, 2142, 2221, 2304, 2389, 2477, 2568, 2662, 2760, 2860, 2965, 3072, 3184, 3299, 3418, 3541, 3669, 3800, 3937, 4077, 4223, 4374, 4530, 4691, 4720]
binDoubles = array.array('d', sorted(bins))
newAntiRatio = TH1F("newAntiRatio", "", len(bins)-1, binDoubles)
antiRatioPad.cd()
newAntiRatio.Draw("SAME")
gStyle.SetOptStat(0)


for iBin in range(0, ratio['anti'].GetNbinsX()):
  newAntiRatio.SetBinContent(newAntiRatio.GetXaxis().FindBin(ratio['anti'].GetBinCenter(iBin)), ratio['anti'].GetBinContent(iBin))
  newAntiRatio.SetBinError(newAntiRatio.GetXaxis().FindBin(ratio['anti'].GetBinCenter(iBin)), ratio['anti'].GetBinError(iBin))
newAntiRatio.SetDrawOption("SAME PE1")
newAntiRatio.SetLineColor(kBlack)



newBtagRatio = TH1F("newBtagRatio", "", len(bins)-1, binDoubles)
print btagRatioPad
btagRatioPad.cd()
newBtagRatio.Draw("SAME")
btagCan.GetPrimitive("ratioPad_btag").SetLeftMargin(btagPad.GetLeftMargin())
btagCan.GetPrimitive("ratioPad_btag").SetRightMargin(btagPad.GetRightMargin())
gStyle.SetOptStat(0)

btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetRangeUser(670, 2065)

for iBin in range(0, ratio['btag'].GetNbinsX()):
  newBtagRatio.SetBinContent(newBtagRatio.GetXaxis().FindBin(ratio['btag'].GetBinCenter(iBin)), ratio['btag'].GetBinContent(iBin))
  newBtagRatio.SetBinError(newBtagRatio.GetXaxis().FindBin(ratio['btag'].GetBinCenter(iBin)), ratio['btag'].GetBinError(iBin))
newBtagRatio.SetDrawOption("SAME PE1")
newBtagRatio.SetLineColor(kBlack)


print btagRatioPad
btagRatioPad.Modified()
print btagRatioPad
btagRatioPad.Update()
print btagRatioPad
btagRatioPad.Modified()
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetRangeUser(670, 2065)
print btagRatioPad
btagRatioPad.Modified()
antiRatioPad.Modified()
antiRatioPad.Update()
antiRatioPad.Modified()
antiRatioPad.Update()


alpha = (1. - 0.6827)*0.5
errorBars = {}
for cat in data.keys():
  errorBars[cat] = TGraphAsymmErrors()
  for iBin in range(0, data[cat].GetNbinsX()):
    nev = data[cat].GetBinContent(iBin) * (data[cat].GetXaxis().GetBinWidth(iBin))
    #if nev == 0. :
    #  hist.SetPoint(ip,hist.GetX()[ip],0.)
    #  hist.SetPointEYlow(ip,0.)
    #  hist.SetPointEYhigh(ip,0.)
    el = (nev - ROOT.Math.gamma_quantile(alpha,nev,1.)) if nev > 0. else 0.
    eu = ROOT.Math.gamma_quantile_c(alpha,nev+1.,1.) - nev 
    if not (cat == "btag" and errorBars[cat].GetN() > 24) and not (cat == "anti" and errorBars[cat].GetN() > 37):
      errorBars[cat].SetPoint(errorBars[cat].GetN(), data[cat].GetXaxis().GetBinCenter(iBin), data[cat].GetBinContent(iBin))
      errorBars[cat].SetPointEYlow(iBin,el/data[cat].GetXaxis().GetBinWidth(iBin))
      errorBars[cat].SetPointEYhigh(iBin,eu/data[cat].GetXaxis().GetBinWidth(iBin))

     

antiDenoms = TH1F("antiDenoms", "", len(bins)-1, binDoubles)
btagDenoms = TH1F("btagDenoms", "", len(bins)-1, binDoubles)

denoms = {"anti": antiDenoms, "btag": btagDenoms}

for prim in btagPad.GetListOfPrimitives():
  if "RooCurve" in prim.IsA().GetName():
    if prim.GetFillColor() == 418:
      errorCurves["btagRaw"]=prim.Clone()
    if prim.GetFillColor() == 0:
      backgroundCurves["btagRaw"]=prim.Clone()
for prim in antiPad.GetListOfPrimitives():
  if "RooCurve" in prim.IsA().GetName():
    if prim.GetFillColor() == 418:
      errorCurves["antiRaw"]=prim.Clone()
    if prim.GetFillColor() == 0:
      backgroundCurves["antiRaw"]=prim.Clone()

antiYerrorArray = errorCurves['antiRaw'].GetY()
antiXerrorArray = errorCurves['antiRaw'].GetX()
btagYerrorArray = errorCurves['btagRaw'].GetY()
btagXerrorArray = errorCurves['btagRaw'].GetX()

def getFitError(x, xErrorArray, yErrorArray):
  (xLeftLow, yLeftLow) = (0,0)
  (xRightLow, yRightLow) = (9999,0)
  (xLeftHi, yLeftHi) = (0,9999)
  (xRightHi, yRightHi) = (9999,9999)
  errLow =  0
  errHi = 9999
  for i in range (0, len(xErrorArray)-1):
    if x == xErrorArray[i] and xErrorArray[i+1] > x:
      errLow = yErrorArray[i]
    if xErrorArray[i] < x < xErrorArray[i+1]:
      (xLeftLow, yLeftLow) = (xErrorArray[i], yErrorArray[i])
      (xRightLow, yRightLow) = (xErrorArray[i+1], yErrorArray[i+1])
      errLow = (x-xLeftLow)*((yRightLow-yLeftLow)/(xRightLow-xLeftLow))+yLeftLow
      break
  for i in range (0, len(xErrorArray)-1):
    if x == xErrorArray[i] and xErrorArray[i+1] < x:
      errHi = yErrorArray[i] 
    if xErrorArray[i] > x > xErrorArray[i+1] :
      (xLeftHi, yLeftHi) = (xErrorArray[i+1], yErrorArray[i+1])
      (xRightHi, yRightHi) = (xErrorArray[i], yErrorArray[i])
      errHi = (x-xLeftHi)*((yRightHi-yLeftHi)/(xRightHi-xLeftHi))+yLeftHi
      break
  return errHi-errLow

  print "leftLow =",  xLeftLow,  yLeftLow
  print "leftHi =",   xLeftHi,   yLeftHi
  print "rightLow =", xRightLow, yRightLow
  print "rightHi =",  xRightHi,  yRightHi
  print  errLow
  print  errHi

errorPoints = {}
errorVals = {}
for cat in errorBars.keys():
  buffX = errorBars[cat].GetX()
  buffY = errorBars[cat].GetY()
  errorPoints[cat]=[]
  for iPoint in range(0, len(buffX) ):
    errorPoints[cat].append(float(buffX[iPoint]))
  errorVals[cat]=[]
  for iPoint in range(0, len(buffY) ):
    errorVals[cat].append(float(buffY[iPoint]))

def getErrorPoint(xValue, cat):
  if xValue in errorPoints[cat]:
    return errorPoints[cat].index(xValue)
  else:
    print "error point for", xValue, "not found"

for iBin in range(0, len(bins)-1):
  binCenter = antiDenoms.GetXaxis().GetBinCenter(iBin)
  if 720. < binCenter and binCenter < 3018.5 :
    statErr = errorBars["anti"].GetErrorY(getErrorPoint(binCenter, "anti"))
    fitErr = getFitError(binCenter, antiXerrorArray, antiYerrorArray)
    totalErr = sqrt(fitErr*fitErr + statErr*statErr)
    print "bin", iBin, "bin center", binCenter, "stat err", statErr, "fit err", fitErr, "total err", totalErr
    antiDenoms.SetBinContent(iBin, sqrt(fitErr*fitErr + statErr*statErr))
  
  newAntiRatio.SetBinContent(newAntiRatio.GetXaxis().FindBin(ratio['anti'].GetBinCenter(iBin)), ratio['anti'].GetBinContent(iBin))


for iBin in range(0, len(bins)-1):
  binCenter = btagDenoms.GetXaxis().GetBinCenter(iBin)
  if 720. < binCenter and binCenter < 1820.:
    statErr = errorBars["btag"].GetErrorY(getErrorPoint(binCenter, "btag"))
    fitErr = getFitError(binCenter, btagXerrorArray, btagYerrorArray)
    totalErr = sqrt(fitErr*fitErr + statErr*statErr)
    print "bin", iBin, "bin center", binCenter, "stat err", statErr, "fit err", fitErr, "total err", totalErr
    btagDenoms.SetBinContent(iBin, sqrt(fitErr*fitErr + statErr*statErr))

for prim in btagPad.GetListOfPrimitives():
  if 'RooCurve' in prim.IsA().GetName():
    if prim.GetLineColor() == 1:
      if prim.GetLineWidth() == 3:
        backgroundCurves["btagRaw"] = prim
for prim in antiPad.GetListOfPrimitives():
  if 'RooCurve' in prim.IsA().GetName():
    if prim.GetLineColor() == 1:
      if prim.GetLineWidth() == 3:
        backgroundCurves["antiRaw"] = prim

antiBackgroundHist = TH1F("antiBackgroundHist", "", len(bins)-1, binDoubles)
btagBackgroundHist = TH1F("btagBackgroundHist", "", len(bins)-1, binDoubles)

for iBin in range(0, len(bins)-1):
  binLowEdge = antiBackgroundHist.GetXaxis().GetBinLowEdge(iBin)
  binUpEdge = antiBackgroundHist.GetXaxis().GetBinUpEdge(iBin)
  backgroundInt = backgroundCurves["antiRaw"].average(binLowEdge, binUpEdge)*(binUpEdge - binLowEdge)/(binUpEdge - binLowEdge)
  antiBackgroundHist.SetBinContent(iBin, backgroundInt)
  antiBackgroundHist.SetBinError(iBin, 0.)

for iBin in range(0, len(bins)-1):
  binLowEdge = btagBackgroundHist.GetXaxis().GetBinLowEdge(iBin)
  binUpEdge = btagBackgroundHist.GetXaxis().GetBinUpEdge(iBin)
  backgroundInt = backgroundCurves["btagRaw"].average(binLowEdge, binUpEdge)*(binUpEdge - binLowEdge)/(binUpEdge - binLowEdge)
  btagBackgroundHist.SetBinContent(iBin, backgroundInt)
  btagBackgroundHist.SetBinError(iBin, 0.)

antiDiff = TH1F("antiDiff", "", len(bins)-1, binDoubles)
btagDiff = TH1F("btagDiff", "", len(bins)-1, binDoubles)

bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 751, 783, 816, 851, 886, 923, 961, 1000, 1041, 1083, 1127, 1172, 1218, 1267, 1316, 1368, 1421, 1476, 1533, 1592, 1653, 1716, 1781, 1848, 1918, 1990, 2065, 2142, 2221, 2304, 2389, 2477, 2568, 2662, 2760, 2860, 2965, 3072, 3184, 3299, 3418, 3541, 3669, 3800, 3937, 4077, 4223, 4374, 4530, 4691, 4720]
antiDataRaw = TH1F("antiDataRaw", "", len(bins)-1, binDoubles)
btagDataRaw = TH1F("btagDataRaw", "", len(bins)-1, binDoubles)

for iBin in range(0, data["anti"].GetNbinsX()):
  correspondingBin = antiDataRaw.FindBin(data["anti"].GetBinCenter(iBin))
  antiDataRaw.SetBinContent(correspondingBin, data["anti"].GetBinContent(iBin))
  antiDataRaw.SetBinError(correspondingBin, data["anti"].GetBinError(iBin))
for iBin in range(0, data["btag"].GetNbinsX()):
  correspondingBin = btagDataRaw.FindBin(data["btag"].GetBinCenter(iBin))
  btagDataRaw.SetBinContent(correspondingBin, data["btag"].GetBinContent(iBin))
  btagDataRaw.SetBinError(correspondingBin, data["btag"].GetBinError(iBin))

antiDiff.Add(antiDataRaw, antiBackgroundHist, 1, -1)
btagDiff.Add(btagDataRaw, btagBackgroundHist, 1, -1)


btagDiff.Divide(btagDenoms)
antiDiff.Divide(antiDenoms)

diffs = {"anti":antiDiff, "btag":btagDiff}
for cat in diffs.keys():
  for iBin in range(0, diffs[cat].GetNbinsX()):
    diffs[cat].SetBinError(iBin, 0.00000001)
    if diffs[cat].GetBinCenter(iBin) < 720:
      diffs[cat].SetBinContent(iBin, -10)
    if cat == "btag" and diffs[cat].GetBinCenter(iBin)>1830:
      diffs[cat].SetBinContent(iBin, -10)
    if cat == "anti" and diffs[cat].GetBinCenter(iBin)>2940:
      diffs[cat].SetBinContent(iBin, -10)

pullErrs = {}
for cat in errorBars.keys():
  pullErrs[cat] = errorBars[cat].Clone()
  for iPoint in range(0, len(errorPoints[cat])):
    denom = denoms[cat].GetBinContent(denoms[cat].GetXaxis().FindBin(errorPoints[cat][iPoint]))
    if not denom == 0:
      pullErrs[cat].SetPoint(iPoint, errorPoints[cat][iPoint], diffs[cat].GetBinContent(diffs[cat].GetXaxis().FindBin(errorPoints[cat][iPoint])))
      pullErrs[cat].SetPointEYhigh(iPoint, errorBars[cat].GetErrorYhigh(iPoint)/denom)
      pullErrs[cat].SetPointEYlow(iPoint, errorBars[cat].GetErrorYlow(iPoint)/denom)
    else:
      pullErrs[cat].SetPoint(iPoint, errorPoints[cat][iPoint], 0)
      pullErrs[cat].SetPointEYhigh(iPoint, 0)
      pullErrs[cat].SetPointEYlow(iPoint, 0)

  

for iBin in range(0, btagDiff.GetNbinsX()):
  if btagDiff.GetBinContent(iBin) == -1:
    btagDiff.SetBinContent(iBin, -20)
  if antiDiff.GetBinContent(iBin) == -1:
    antiDiff.SetBinContent(iBin, -20)

antiRatioPad.Clear()
antiRatioPad.cd()
antiDiff.Draw("E1")
antiDiff.GetXaxis().SetRangeUser(700, 3200)
antiDiff.GetYaxis().SetRangeUser(-5, 5)
antiDiff.SetLineColor(kBlack)

btagRatioPad = btagCan.GetPrimitive("ratioPad_btag")
print btagRatioPad
btagRatioPad.Clear()
print btagRatioPad
btagRatioPad.cd()
btagDiff.Draw("E1")
btagDiff.GetXaxis().SetRangeUser(700, 2200)
btagDiff.GetYaxis().SetRangeUser(-5, 5)
btagDiff.SetLineColor(kBlack)

print btagRatioPad
btagRatioPad.SetGridy()
antiRatioPad.SetGridy()
btagDiff.SetMarkerColor(kBlack)
antiDiff.SetMarkerColor(kBlack)


antiDiff.GetYaxis().SetNdivisions(405)
antiDiff.GetYaxis().SetTitleSize(0.15)
antiDiff.GetYaxis().SetTitleOffset(0.3)
antiDiff.GetYaxis().SetLabelSize(0.1)
antiDiff.GetYaxis().SetTitle('(data-fit)/unc.')
antiDiff.GetYaxis().SetTitleOffset(0.35)
antiDiff.GetXaxis().SetLabelSize(0.1)
antiDiff.GetXaxis().SetRangeUser(670, 3184)
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetRangeUser(670, 3184)
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetRangeUser(1.2e-3, 900)
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitle("dN/dm_{J#gamma} (GeV^{-1})")
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetTitle("m_{J#gamma} (GeV)")
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitleOffset(0.9)
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitleSize(0.058)
btagDiff.GetYaxis().SetNdivisions(405)
btagDiff.GetYaxis().SetTitleSize(0.15)
btagDiff.GetYaxis().SetTitleOffset(0.3)
btagDiff.GetYaxis().SetLabelSize(0.1)
btagDiff.GetYaxis().SetTitle('(data-fit)/unc.')
btagDiff.GetYaxis().SetTitleOffset(0.35)
btagDiff.GetXaxis().SetLabelSize(0.1)
btagDiff.GetXaxis().SetRangeUser(670, 2142)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetRangeUser(670, 2142)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitle("dN/dm_{J#gamma} (GeV^{-1})")
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetTitle("m_{J#gamma} (GeV)")
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").RemovePoint(0)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitleOffset(0.9)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetTitleSize(0.058)

for cat in data.keys():
  errorBars[cat].RemovePoint(0)
  if cat == "btag":
    for iBin in range(0, data[cat].GetNbinsX()):
      data[cat].SetBinError(iBin, 0.00000001)
    btagPad.cd()
    errorBars[cat].Draw("SAME E1")
  if cat == "anti":
    for iBin in range(0, data[cat].GetNbinsX()):
      data[cat].SetBinError(iBin, 0.00000001)
    antiPad.cd()
    errorBars[cat].Draw("SAME E1")

for prim in btagPad.GetListOfPrimitives():
  print prim.IsA().GetName()
  print prim.GetName()
  if "RooCurve" in prim.IsA().GetName():
    if prim.GetFillColor()==418 or prim.GetFillColor() == 800:
      prim.RemovePoint(prim.GetN()-1)
      prim.RemovePoint(0)
      prim.RemovePoint(prim.GetN()-1)
      if prim.GetFillColor()==418:
        prim.RemovePoint(0)
      #prim.RemovePoint(prim.GetN()-1)
      print "removed point"

for err in errorBars.values():
  err.RemovePoint(0)
btagRatioPad.cd()
pullErrs["btag"].Draw("SAME PE1")
antiRatioPad.cd()
pullErrs["anti"].Draw("SAME PE1")

btagPad.Modified()
antiPad.Modified()
btagPad.Update()
antiPad.Update()


print btagRatioPad
btagRatioPad.Modified()
print btagRatioPad
btagRatioPad.Modified()
antiRatioPad.Modified()
print btagRatioPad
btagRatioPad.Update()
antiRatioPad.Update()

antiRatioPad.Modified()
print btagRatioPad
btagRatioPad.Update()
antiRatioPad.Update()

btagRatioPad.SetGridy(0)
antiRatioPad.SetGridy(0)
btagRatioPad.SetTicks(1)
antiRatioPad.SetTicks(1)

btagRatioPad.cd()
btagLine = TLine(700, 0 , 2142, 0)
btagLine.SetLineStyle(3)
btagLine.Draw()
antiRatioPad.cd()
antiLine = TLine(700, 0 , 3150, 0)
antiLine.SetLineStyle(3)
antiLine.Draw()

antiDiff.GetYaxis().SetRangeUser(-3, 3)
btagDiff.GetYaxis().SetRangeUser(-3, 3)

antiLabelSize = antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().GetLabelSize()
antiTitleSize = antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().GetTitleSize()
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetLabelSize(0)
antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetTitleSize(0)
btagLabelSize = btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().GetLabelSize()
btagTitleSize = btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().GetTitleSize()
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetLabelSize(0)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetXaxis().SetTitleSize(0)

antiPad.SetBottomMargin(0)
antiRatioPad.SetTopMargin(1)
antiPad.SetPad(0.05, 0.48, 1.025, 0.99)
antiRatioPad.SetTopMargin(2)
antiRatioPad.SetPad(0.05, 0.3, 1.025, 0.48)
btagPad.SetBottomMargin(0)
btagRatioPad.SetTopMargin(1)
btagPad.SetPad(0.05, 0.48, 1.025, 0.99)
btagRatioPad.SetTopMargin(2)
btagRatioPad.SetPad(0.05, 0.3, 1.025, 0.48)


antiPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetLabelSize(0.066)
btagPad.GetPrimitive("bkg_dijetsimple2_Norm[x]_errorband").GetYaxis().SetLabelSize(0.066)


btagPad.Modified()
antiPad.Modified()
btagPad.Update()
antiPad.Update()

