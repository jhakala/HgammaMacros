from ROOT import *
from fitResultHelpers import generateToyFunctions, getVarsAndCorrMatrix

par1, par2, correlationMatrix, covarianceMatrix = getVarsAndCorrMatrix("fitRes_btag.root")

normNom = 79.35249078273773
p1nom = 30.772208177849887
p2nom = -2.5224772757037215
print par1
print par2
functions = generateToyFunctions(normNom, 8.90800153006, p1nom, p1nom*.12, p2nom, p2nom*.12, correlationMatrix, covarianceMatrix, 40)

tcanvas = TCanvas()
tcanvas.cd()

first=True
for function in functions:
  if first:
    function.Draw()
    first=False
  else:
    function.Draw("SAME")

nomFormula = "[0]*TMath::Power(x, [1]+[2]*TMath::Log(x))"
nomFunction = TF1("nominal", nomFormula, 700, 4700)
nomFunction.SetParameters(1, p1nom, p2nom)
nomFunction.SetParameter(0, normNom / nomFunction.Integral(700, 4700))
nomFunction.SetLineColor(kBlue)
nomFunction.Draw("SAME")
