from ROOT import *

expCoeffFile = TFile("turnOnFits.root")
expCoeffFunc = TF1("expCoeffFunc", "TMath::Max([0]+[1]*TMath::ATan((x-[2])/[3]), -0.0064)", 40, 200)
expCoeffFunc.SetParameters(-0.00523795357368,  0.00120007401227,  109.24343923,  24.3269585017)
coeffCan = TCanvas()
coeffCan.cd() 
coeffGraph = expCoeffFile.Get("expCoeffs")
coeffGraph.SetTitle("Estimation of exponential's coefficient")
coeffGraph.GetXaxis().SetTitle("center of m_{j} window (GeV)")
coeffGraph.GetYaxis().SetTitle("coefficient in exp term")
coeffGraph.GetYaxis().SetTitleOffset(1.17)
coeffGraph.GetYaxis().SetLabelSize(0.022)

coeffGraph.Draw()
for i in range(0,30):
  coeffGraph.Fit(expCoeffFunc, "M", "", 65, 150)
  coeffGraph.Fit(expCoeffFunc, "", "", 65, 150)
print "parameters for fit function of exponential coefficients:"
for i in range(0, 4):
  print str(expCoeffFunc.GetParameter(i)) + ","
coeffCan.Print("coeffFit.pdf")


inFile = TFile("turnOnFits_fixedExp.root")
graph = inFile.Get("turnOn")
can = TCanvas()
can.cd()
graph.Draw()

fitFunction = TF1("fitFunction", "pol4")
graph.Fit(fitFunction, "M", "", 45, 165)
graph.SetTitle("99% turn on point estimation from fits")
graph.GetYaxis().SetTitle("solution for 99% turn on point (GeV)")
graph.GetYaxis().SetTitleOffset(1.1)
graph.GetXaxis().SetTitle("center of m_{j} window (GeV)")

solution = fitFunction.Eval(125.)

can.Draw()
lineVert = TLine(125., can.GetFrame().GetY1(), 125., can.GetFrame().GetY2() )
lineHoriz = TLine(can.GetFrame().GetX1(), solution, can.GetFrame().GetX2(), solution )
lineVert.SetLineColor(kGray)
lineHoriz.SetLineColor(kGray+1)
lineVert.Draw("SAME")
lineHoriz.Draw("SAME")
text = TPaveText(can.GetFrame().GetY2()/12., solution+can.GetFrame().GetX2()/16.,  can.GetFrame().GetY2()/12., solution+can.GetFrame().GetX2()/16.)
text.AddText("m_{j\gamma}=%01d GeV" % solution)
text.SetTextSize(0.03)
text.Draw("SAME")
can.Print("finalTurnOn_MC.pdf")
