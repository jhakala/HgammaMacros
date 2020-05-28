from ROOT import TFile, kRed, kBlue, TH1F, TCanvas, TPad, THStack
from optTools import *
fnS = "debug.root"
sidebandFile = TFile.Open(fnS)
i=2
debug=True
can_sideband    = getCanvas(sidebandFile    , i, True  , debug)
#legend = None
#for prim in can_sideband.GetPrimitive("2_stack_nMinus1_bJet_akxDec_bbvsLight_sideband").GetListOfPrimitives():
#  print prim.GetName(), prim.IsA().GetName()
#  if "TLegend" in prim.IsA().GetName():
#    legend = prim
can_sideband.Draw()


#can = TCanvas()
#can.cd()
#top    = TPad("top-test_underscore.root",       "top", 0, 0.3,  1, 1.0)
#top.Draw()
#bottom = TPad("bottom-test_underscore.root", "bottom", 0, 0.05, 1, 0.3)
#bottom.Draw()
#
#thist = TH1F("thist-test_underscore.root", "thist", 100, 0, 100)
#ahist = TH1F("ahist-test_underscore.root", "ahist", 100, 0, 100)
#bhist = TH1F("bhist-test_underscore.root", "bhist", 100, 0, 100)
#chist = TH1F("chist-test_underscore.root", "chist", 100, 0, 100)
#
#for i in range(0, 100):
#  thist.SetBinContent(i, i)
#  bhist.SetBinContent(i, (100-i)/2.)
#  ahist.SetBinContent(i, i/2.)
#thist.SetFillColor(kRed)
#bhist.SetFillColor(kBlue)
#stack = THStack("stack-test_underscore.root", "stack")
#stack.Add(thist)
#stack.Add(bhist)
#stack.Add(chist)
#
#
#
#from tcanvasTDR import TDRify
#
#bottom.cd()
#bhist.Draw("HIST")
#bottom.BuildLegend()
#TDRify(bottom,   True, "bp")
#top.cd()
##thist.Draw("HIST")
#stack.Draw("HIST")
#ahist.SetMarkerStyle(20)
#ahist.Draw("PE SAME")
#
#top.BuildLegend()
#TDRify(top,   False, "tp")
#
#for prim in top.GetListOfPrimitives():
#  if "TLegend" in prim.IsA().GetName():
#    prim.SetX1NDC(0.753)
#    prim.SetY1NDC(0.703)
#    prim.SetX2NDC(0.946)
#    prim.SetY2NDC(0.911)
#    print "moved"
#    for subprim in prim.GetListOfPrimitives():
#      print "subprim:", subprim.GetName(), subprim.IsA().GetName()
#      subprim.SetLabel("#alpha#beta")
#      subprim.SetOption("lf")
#
#for prim in bottom.GetListOfPrimitives():
#  if "TLegend" in prim.IsA().GetName():
#    prim.SetX1NDC(0.753)
#    prim.SetY1NDC(0.703)
#    prim.SetX2NDC(0.946)
#    prim.SetY2NDC(0.911)
#    print "moved"
#    for subprim in prim.GetListOfPrimitives():
#      if "ahist" in subprim.GetName():
#        subprim.SetLabel("#xi#gamma")
#        subprim.SetOption("pe")
#      else:
#        print "subprim:", subprim.GetName(), subprim.IsA().GetName()
#        subprim.SetLabel("#alpha#gamma")
#        subprim.SetOption("lf")
#
#top.Modified()
#top.Update()
#bottom.Modified()
#bottom.Update()
#
#can.Modified()
#can.Update()
#
#
