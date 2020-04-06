inputNames = ["vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sig_m850.root", 
"vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sideband110140.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sig_m1000.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sig_m1450.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sig_m2050.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/antibtag/histos_sig_m3250.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sideband110140.root", 
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sig_m850.root", 
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sig_m1000.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sig_m1450.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sig_m2050.root",
"vgHists_lowerBound720_btag-nom_phSF-nom/btag/histos_sig_m3250.root"]



from ROOT import *
inputFiles = [TFile(name) for name in inputNames]

from os import path
import array
for inputFile in inputFiles:
  outName = path.dirname(inputFile.GetName()).split("/")[-1] + "/" + path.basename(inputFile.GetName())
  outputFile = TFile("vgVarBinsNew/"+outName, "RECREATE")
  outputFile.cd()
  print outName
  inputFile.ls()
  hist = inputFile.Get("distribs_X")
  print hist
  bins = [720, 751, 783, 816, 851, 886, 923, 961, 1000, 1041, 1083, 1127, 1172, 1218, 1267, 1316, 1368, 1421, 1476, 1533, 1592, 1653, 1716, 1781, 1848, 1918, 1990, 2065, 2142, 2221, 2304, 2389, 2477, 2568, 2662, 2760, 2860, 2965, 3072, 3184, 3299, 3418, 3541, 3669, 3800, 3937, 4077, 4223, 4374, 4530, 4691, 4720]
  binDoubles = array.array('d', sorted(bins))
  histVar = hist.Rebin(len(bins)-1, "histVar", binDoubles)
  histVar.SetBinErrorOption(TH1.kPoisson)
  for iPoint in range(0, histVar.GetXaxis().GetNbins()):
    #if (y > 0):
      #print "checking point %i: (%f, %f)" % (iPoint, x, y)
    print "histVar had binContent", histVar.GetBinContent(iPoint)
    print "histVar had binWidth", histVar.GetBinWidth(iPoint)
    newContent = 100*histVar.GetBinContent(iPoint)/histVar.GetBinWidth(iPoint)
    newError = histVar.GetBinError(iPoint)/histVar.GetBinWidth(iPoint)
    print "setting bin content to:", newContent
    histVar.SetBinContent(iPoint, newContent)
    histVar.SetBinError(iPoint, newError)
    print "check", histVar.GetBinContent(iPoint)
  histVar.Write()
  outputFile.Write()
