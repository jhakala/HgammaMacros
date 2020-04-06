from ROOT import *

vgFile = TFile("~/HgammaMacros/vgHists/btag/histos_sideband100110.root")
hist = vgFile.Get("distribs_X")
rebin=40
hist.Rebin(rebin)

formula = "[0]*TMath::Power(x,[1]+[2]*log(x))"
fit = TF1("nom", formula, 700, 4700)

fit.SetParameters(1, 30.772208177849887, -2.5224772757037215)
normNom = 79.35249078273773

fit.SetParameter(0, rebin*normNom/fit.Integral(700, 4700))


hist.Draw()
fit.Draw("SAME")
