from ROOT import TFile, TH1F, TCanvas, TPad       

#cans=[]
pads=[]
datahists=[]

outFile = TFile.Open("debug.root", "RECREATE")
can=TCanvas()
pads.append(TPad("topPad", "top pad", 0, 0.3, 1, 1.0))
can.cd()
pads[-1].Draw()
pads[-1].SetLogy()

test = TH1F("test", "test hist", 100, 0., 1.)
for iBin in range(0,100):
  test.SetBinContent(iBin, iBin/2.)
datahists.append(test)
pads[-1].cd()
datahists[-1].Draw("PE")
datahists[-1].SetMarkerStyle(20)
datahists[-1].SetMarkerSize(datahists[-1].GetMarkerSize()*.7)

pads[-1].SetBottomMargin(0)
pads[-1].BuildLegend()
can.cd()
pads[-1].Draw()
for prim in pads[-1].GetListOfPrimitives():
  if "TLegend" in prim.IsA().GetName():
    ### removing this line prevents the pure virtual function error.... ? ###
    prim.GetListOfPrimitives()

outFile.cd()
can.Write()
outFile.Close()
