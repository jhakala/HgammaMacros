from ROOT import *
inFile = TFile("turnOnFits_fixedExp.root")
graph = inFile.Get("turnOn")
can = TCanvas()
can.cd()
graph.Draw()

fitFunction = TF1("fitFunction", "pol4")
graph.Fit(fitFunction, "M", "", 45, 165)

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
