from ROOT import *

#>>> fitResult.correlationMatrix()[0][0]
#1.0
#>>> fitResult.correlationMatrix()[0][1]
#-0.9980042322325037
#>>> fitResult.correlationMatrix()[1][0]
#-0.9980042322325037
#>>> fitResult.correlationMatrix()[1][1]
#1.0

corrMatrix = [[1., -0.9980042322325037],[-0.9980042322325037, 1]]

p1 = 32.95592290945736
p1errHi = 2.247091595109989
p2errLo = -2.2164570595773725

p2 = -2.7199969278203806
p2errHi = 0.15986898816924228
p2errLo= -0.16213815281842958

formula = "[0]*TMath::Power(x,([1]+[2]*TMath::Log(x)))"
func = TF1("fitFunc", formula, 700, 4700)
func.SetParameters(1, p1, p2)
func.SetParameter(0, 1./func.Integral(700, 4700))
can = TCanvas()
func.SetLineColor(kBlack)
func.Draw()



efunc1 = TF1("fitErrFunc1", formula, 700, 4700)
efunc1.SetParameters(1, p1+p1errHi, p2)
efunc1.SetParameter(0, 1./efunc1.Integral(700, 4700))
efunc1.SetLineColor(kRed)
#efunc1.Draw()
efunc1.Draw("SAME")

efunc0 = TF1("fitErrFunc0", formula, 700, 4700)
efunc0.SetParameters(1, p1+p1errHi, p2+(p2errHi*corrMatrix[1][0]))
efunc0.SetParameter(0, 1./efunc0.Integral(700, 4700))
efunc0.SetLineColor(kBlue)
#efunc0.Draw()
efunc0.Draw("SAME")
