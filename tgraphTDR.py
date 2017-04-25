from ROOT import *
import CMS_lumi, tdrstyle
from sys import argv


tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

iPeriod = 4
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

tfile = TFile(argv[1], "r")
tfile.ls()
tgraph = tfile.Get("")
#canvas = tfile.Get("c1_n2")
canvas = TCanvas()
canvas.cd()
#tgraph.GetYaxis().SetRangeUser(105, 270)
tgraph.Draw()
tgraph.GetYaxis().SetTitleOffset(1.4)
#canvas.Draw()



#canvas.SetFillColor(0)
#canvas.SetBorderMode(0)
#canvas.SetFrameFillStyle(0)
#canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
gStyle.SetOptStat(0)
for primitive in canvas.GetListOfPrimitives():
    print primitive
    if primitive.GetName() in ["data"]:
        primitive.SetStats(kFALSE)
canvas.cd()
canvas.Update()
canvas.RedrawAxis()

canvas.Print("%s_plot.pdf"%argv[1])
