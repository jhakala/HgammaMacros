from ROOT import *
can = TCanvas()
can.cd()
erf = TF1("erf", "[0]*([3]+0.5*TMath::Erf((x-[1])/[2]))", 200, 3000)
erf.SetParameters(2.1, 1000, 500, 0.55)
erf.GetYaxis().SetRangeUser(0, 6)
erf.Draw()
can.Modified()
can.Update()
