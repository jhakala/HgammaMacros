from ROOT import *

fitFiles = {}
categories = ["antibtag", "btag"]
cans = {}
ratioPads = {}
fitPads = {}
for category in categories:
  fitFiles[category] = TFile("~/dec20/%s_fit_errs_new.root" % category)
  cans[category] = fitFiles[category].Get("masterCan_%s" % category)
  for prim in cans[category].GetListOfPrimitives():
    #print "----------"
    #print prim.GetName()
    #print prim.IsA().GetName()
    if "ratioPad_%s" % category in prim.GetName():
      ratioPads[category] = prim
    if "dataFit_%s" % category in prim.GetName():
      fitPads[category] = prim

legends = {}
mainHists = {}
ratioHists = {}
for category in categories:
  for prim in fitPads[category].GetListOfPrimitives():
    print "----------"
    print prim.GetName()
    print prim.IsA().GetName()
    if "TLegend" in prim.IsA().GetName():
      legends[category]=prim
    if "rebinned_fit" in prim.GetName():
      mainHists[category]=prim
  ratioHists[category] = ratioPads[category].GetPrimitive("pdfHist_0")

for mainHist in mainHists.values():
  mainHist.GetYaxis().SetTitleOffset(0.8)
  mainHist.GetYaxis().SetTitleSize(0.06)
  mainHist.GetYaxis().SetLabelSize(0.055)
  mainHist.GetXaxis().SetLabelSize(0.055)
  mainHist.GetXaxis().SetTitleOffset(0.85)
  mainHist.GetXaxis().SetLabelSize(0.055)
  mainHist.GetXaxis().SetTitleSize(0.06)


mainHists["antibtag"].GetYaxis().SetRangeUser(.11, 5e4)

for ratioHist in ratioHists.values():
  ratioHist.GetYaxis().SetTitleSize(0.18)
  ratioHist.GetYaxis().SetTitleOffset(0.27)
  ratioHist.GetYaxis().SetLabelSize(0.13)
  ratioHist.GetXaxis().SetLabelSize(0.13)
  #ratioHist.Draw()
print legends
for category in legends.keys():
  for prim in legends[category].GetListOfPrimitives():
    #print "-----------"
    #print prim.GetName()
    #print prim.IsA().GetName()
    if "Projection of bkg_dijetsimple2" in prim.GetLabel():
      prim.SetLabel("dijet2 fit")
    if "%s category: fits" % category in prim.GetLabel():
      prim.SetLabel("%s category" % category)
    #print prim.GetLabel()



testPads = {}
hists = {}
for category in categories:
  #cans[category].Print("fit_errs_%s.pdf"%category)
  for prim in cans[category].GetPrimitive("dataFit_%s" % category).GetListOfPrimitives():
    print "----------"
    print prim.GetName()
    print prim.IsA().GetName()
    print "----------"
  print cans[category].GetPrimitive("dataFit_%s" % category)
  testPads[category] = cans[category].GetPrimitive("dataFit_%s" % category)
  hists[category] = testPads[category].GetPrimitive("rebinned_fit").Clone()
  cans[category].Draw()
for category in categories:
  testPads[category].cd()
  hists[category].Draw("SAME E1")
  cans[category].Print("fit_errs_%s.pdf" % category)
