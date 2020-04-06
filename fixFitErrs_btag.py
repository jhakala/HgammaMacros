from ROOT import *
from math import sqrt
tfile = []
tfile.append(TFile("~/oct31/rebinnedPdfs_btag.root"))

btag = tfile[0].Get("masterCan_btag")
btagFit = btag.GetPrimitive("dataFit_btag")
btagHist = btagFit.GetPrimitive("rebinned_fit")
print "# entries in btag category:"
print btagHist.GetSumOfWeights()
print " --> sqrt:"
print "     ", sqrt(btagHist.GetSumOfWeights())
print "      % error: -->", sqrt(btagHist.GetSumOfWeights())/btagHist.GetSumOfWeights()

btagHist.SetTitle("btag category")
btagCurve = btagFit.GetPrimitive("bkg_dijetsimple2_Norm[x]")
btagCurve.SetTitle("dijet2 fit")

#anti.Draw()
btag.Draw()

formula = "[0]*TMath::Power(x,[1]+[2]*log(x))"
formulaVar  = "TMath::Max(TMath::Max([8]*TMath::Power(x,[0]+[1]*log(x)), [9]*TMath::Power(x,[2]+[3]*log(x))), TMath::Max([10]*TMath::Power(x,[4]+[5]*log(x)), [11]*TMath::Power(x,[6]+[7]*log(x))))"
formulaNom = "[12]*TMath::Power(x,[13]+[14]*log(x))"
formulaMax ="TMath::Max(%s,  %s)" % (formulaVar, formulaNom)
formulaVar2  = "TMath::Min(TMath::Min([8]*TMath::Power(x,[0]+[1]*log(x)), [9]*TMath::Power(x,[2]+[3]*log(x))), TMath::Min([10]*TMath::Power(x,[4]+[5]*log(x)), [11]*TMath::Power(x,[6]+[7]*log(x))))"
formulaMin = "TMath::Min(%s, %s)" % (formulaVar2, formulaNom)
par1nom = 30.772208177849887
par1err = 0.02*par1nom
par2nom = -2.5224772757037215
par2err = 0.018*par2nom
normNom = 79.35249078273773
normErr = 8.90800153006
normHiNom = normNom+normErr
normLoNom = normNom-normErr
rebin=50

fitNom = TF1("nom", formula, 700, 4700)
fitTmp = TF1("nom", formula, 700, 4700)
fitNom.SetParameters(1, par1nom, par2nom)
fitInt = fitNom.Integral(700, 4700)
fitNom.SetParameter(0, (rebin*normNom)/fitInt)

fitMax = TF1("max", formulaMax, 700, 4700)
fitMax.SetParameter(0, par1nom+par1err)
fitMax.SetParameter(1, par2nom)
fitMax.SetParameter(2, par1nom-par1err)
fitMax.SetParameter(3, par2nom)
fitMax.SetParameter(4, par1nom)
fitMax.SetParameter(5, par2nom+par2err)
fitMax.SetParameter(6, par1nom)
fitMax.SetParameter(7, par2nom-par2err)

fitTmp.SetParameters(1, par1nom+par1err, par2nom)
piece1norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMax.SetParameter(8, piece1norm)

fitTmp.SetParameters(1, par1nom-par1err, par2nom)
piece2norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMax.SetParameter(9, piece2norm )


fitTmp.SetParameters(1, par1nom, par2nom+par2err)
piece3norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMax.SetParameter(10, piece3norm)

fitTmp.SetParameters(1, par1nom, par2nom-par2err)
piece4norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMax.SetParameter(11, piece4norm )

fitMax.SetParameter(12, (rebin*normHiNom)/fitInt)
fitMax.SetParameter(13, par1nom)
fitMax.SetParameter(14, par2nom)

fitMax.SetLineColor(kBlue)

fitMin = TF1("min", formulaMin, 700, 4700)
fitMin.SetParameter(0, par1nom+par1err)
fitMin.SetParameter(1, par2nom)
fitMin.SetParameter(2, par1nom-par1err)
fitMin.SetParameter(3, par2nom)
fitMin.SetParameter(4, par1nom)
fitMin.SetParameter(5, par2nom+par2err)
fitMin.SetParameter(6, par1nom)
fitMin.SetParameter(7, par2nom-par2err)

fitTmp.SetParameters(1, par1nom+par1err, par2nom)
piece1norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMin.SetParameter(8, piece1norm)

fitTmp.SetParameters(1, par1nom-par1err, par2nom)
piece2norm = (rebin*normHiNom)/fitTmp.Integral(700, 4700)
fitMin.SetParameter(9, piece2norm )


fitTmp.SetParameters(1, par1nom, par2nom+par2err)
piece3norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
fitMin.SetParameter(10, piece3norm)

fitTmp.SetParameters(1, par1nom, par2nom-par2err)
piece4norm = (rebin*normLoNom)/fitTmp.Integral(700, 4700)
fitMin.SetParameter(11, piece4norm )

fitMin.SetParameter(12, (rebin*normLoNom)/fitInt)
fitMin.SetParameter(13, par1nom)
fitMin.SetParameter(14, par2nom)

fitMin.SetLineColor(kRed)

fitNom.SetLineColor(kBlack)

btagFit.cd()
#newCan = TCanvas()
#newCan.cd()
#fitNom.Draw()
fitNom.Draw("SAME")
fitMax.Draw("SAME")
fitMin.Draw("SAME")
