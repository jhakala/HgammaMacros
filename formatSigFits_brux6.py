from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", dest="category",
                  help = "the category: either btag or antibtag")
parser.add_option("-r", dest="rebin", type=int, default=10,
                  help = "the rebin factor")
parser.add_option("-b", action="store_true", dest="batch",
                  help = "turn on batch mode")
(options, args) = parser.parse_args()
if not options.category in ["btag", "antibtag"]:
  print "you must pick either 'btag' or 'antibtag' as the -c option"
  exit(1)
from ROOT import *
if options.batch:
  gROOT.SetBatch()

gStyle.SetOptStat(0)
outFile = TFile("prettyFits_%s.root" % options.category, "RECREATE")
def getIntegral(curve, xLow, xHi):
  integral = Double(0)
  yLow  = Double(curve.Eval(xLow))
  yHi   = Double(curve.Eval(xHi) )
  print "curve at x=%f has value y=%f" % (xLow, yLow)
  print "curve at x=%f has value y=%f" % (xHi, yHi)
  xLast = Double(xLow            )
  yLast = Double(yLow            )
  xx = Double(xLow               )
  yy = Double(yLow               )
  for iPoint in range(0, curve.GetN()):
    #curve.GetPoint(iPoint-1, xLast, yLast)
    curve.GetPoint(iPoint, xx, yy)
    if xx>=xLow and xx<=xHi :
      print "python evaluates %f <= %f to %r" % (xx, xHi, xx<=xHi)
      print "found a point between %f and %f: it has (x,y) value (%f, %f)"%(xLow, xHi, xx,yy)
      print "will add (%f=%f) * (%f+%f)/2" % (xx, xLast, yy, yLast)
      integral +=  (xx-xLast) *(yy+yLast)/2
      print "   == %f" % ((xx-xLast) *(yy+yLast)/2)
      print " total   == %f" % integral
      xLast = Double(float(xx))
      yLast = Double(float(yy))
  print "  adding the last piece"
  print "(%f-%f) * (%f+%f)/2" % (xHi, xLast, yHi, yLast) 
  integral +=  (xHi-xLast) *(yHi+yLast)/2 
  print "   == %f" % ((xHi-xLast) *(yHi+yLast)/2)
  print "total = %f" % integral
  return integral

from ROOT import *
fullsimMCs      = [750, 850, 1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2450, 2850, 3250]
#fullsimMCs      = [3250]
for fullsimMC in fullsimMCs:
  outCan = TCanvas("c_%i"% fullsimMC, "c_%i"% fullsimMC, 600, 800)
  fullsimHist     = None
  fullsimCurve     = None
  topPad       = TPad("rebinned_sigfit_%i" % fullsimMC, "Signal fit, m_{X}=%i GeV" % fullsimMC, 0, 0.3, 1, 1.0)
  bottomPad       = TPad("rebinned_sigpull_%i" % fullsimMC, "Fit Pull, m_{X}=%i GeV"  % fullsimMC, 0, 0.05, 1, 0.29)
  topPad.SetName("rebinned_%i" % fullsimMC)
  fullsimFileName = "../Vg/signalFits_%s_fullsim/c_mX_SR_%i.root" % (options.category, fullsimMC)
  fullsimFile = TFile(fullsimFileName)
  fullsimCanvas = fullsimFile.Get("c_mX_SR_%i" % fullsimMC)
  fullsimPad = fullsimCanvas.GetPrimitive("p_1")
  for primitive in fullsimPad.GetListOfPrimitives():
    print primitive
    if "RooHist" in primitive.IsA().GetName():
      fullsimHist = primitive
      fullsimHist.SetName("hist_%i" % fullsimMC)
    elif "RooCurve" in primitive.IsA().GetName():
      fullsimCurve = primitive
      fullsimCurve.SetName("curve_%i" % fullsimMC)
  hist = TH1F("rebinned_hist", "Signal fit, m_{X}=%i GeV" % fullsimMC, 4000, 700, 4700)
  hist.Sumw2()
  x = Double()
  xLast = Double()
  y = Double()
  for iPoint in range(0, fullsimHist.GetN()+5):
    fullsimHist.GetPoint(iPoint, x, y)
    e= fullsimHist.GetErrorYhigh(iPoint)
    #if (y > 0):
      #print "checking point %i: (%f, %f)" % (iPoint, x, y)
    histBin = hist.GetXaxis().FindBin(x)
    hist.SetBinContent(histBin, y)
    hist.SetBinError(histBin, e)
  for iPoint in range(0, fullsimCurve.GetN()+5):
    fullsimCurve.GetPoint(iPoint, x, y)
    fullsimCurve.SetPoint(iPoint, x, options.rebin*y)
    print "fullSimCurve has (x,y) values: (%f,%f)" % (x,y)

  hist.SetMarkerStyle(20)
  hist.Rebin(options.rebin)
  topPad.cd()
  hist.Draw("PE1")
  hist.GetYaxis().SetTitle("Events (A.U.)")
  hist.GetXaxis().SetTitle("M_{X} (GeV)")
  hist.GetYaxis().SetTitleOffset(1.2)
  hist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  fullsimCurve.SetLineColor(kRed)
  fullsimCurve.Draw("SAME")
  outCan.cd()
  topPad.Draw()
  outCan.Draw()
  ksHist = hist.Clone()
  pullHist = hist.Clone() 
  pullHist.SetName("ratio_%i" % fullsimMC)
  for iBin in range(1,hist.GetXaxis().GetNbins()):
    integral = getIntegral(fullsimCurve, hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin))
    ksHist.SetBinContent(iBin, integral)
    print "bin content from %f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), hist.GetBinContent(iBin))
    print "adjusted from x=%f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), integral/hist.GetXaxis().GetBinWidth(iBin))
    if not hist.GetBinError(iBin) == 0 and not hist.GetBinContent(iBin) <=0.1 :
      pullHist.SetBinContent(iBin, (hist.GetBinContent(iBin) - integral/hist.GetXaxis().GetBinWidth(iBin) )/hist.GetBinError(iBin))
      pullHist.SetBinError(iBin, 0)
    else:
      pullHist.SetBinContent(iBin, -999)
  #cloneHist = hist.Clone()
  #cloneHist.Divide(pullHist)
  bottomPad.cd()
  #cloneHist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  #cloneHist.Draw()
  #cloneHist.GetXaxis().SetLabelSize(.1)
  #cloneHist.GetYaxis().SetLabelSize(.1)
  #cloneHist.GetYaxis().SetRangeUser(0, 2)
  pullHist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  pullHist.Draw("P")
  pullHist.SetMarkerStyle(2)
  pullHist.SetTitle("")
  pullHist.GetXaxis().SetLabelSize(0)
  pullHist.GetXaxis().SetTitle("")
  pullHist.GetYaxis().SetTitle("Pull")
  pullHist.GetYaxis().SetTitleSize(0.1)
  pullHist.GetYaxis().SetTitleOffset(0.3)
  pullHist.GetYaxis().SetLabelSize(.13)
  pullHist.GetYaxis().SetRangeUser(-5, 5)
  pullHist.GetYaxis().SetNdivisions(405)
  outCan.cd()
  bottomPad.Draw()
  outFile.cd()
  outCan.Write()
  outCan.SaveAs("%s_%i.pdf" % (options.category, fullsimMC))
  print "KS test result for %i:" % fullsimMC , hist.KolmogorovTest(ksHist)
outFile.Close()
  
