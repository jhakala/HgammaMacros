from ROOT import *
phSFvariation = "nom"
tfile = TFile("btag-nom_phSF-%s_efficienciesGraphs_masswindow_110-140.root" % phSFvariation)
graphBtag = tfile.Get("SigEff_btag")
can1 = TCanvas()
can1.cd()
graphBtag.Draw("AP")

fitFunctionBtag = TF1("fitFunctionBtag", "[0]+[1]*TMath::ATan((x-[2])^2/[3])*TMath::Exp(-x/[4])", 600, 4000)
fitFunctionBtag.SetParameters(0, .06, 500, 100000, 2500)
#fitFunctionBtag = TF1("fitFunctionBtag", "[0]+[1]*TMath::ATan([2]*(x-[3]))*TMath::Exp([4]*TMath::Power(x-[5], [6]))", 600, 3250)
#fitFunctionBtag.SetParameters(0, 0.1 , 0.002 , 650 , -0.00000015, 650, 2)
#fitFunctionBtag = TF1("fitFunctionBtag", "pol5", 600, 4000)

#fitFunctionBtag = TF1("fitFunctionBtag", "[0]*TMath::Landau([1]*x*x+[2]*x+[3], [4], [5])+[6]", 650, 4000)
#fitFunctionBtag.SetParameters(0.562537353038 , -0.000172410406751 , 1.13748300272 , 529.72432969 , 1966.27567031 , 510.478940203 , -0.0322061235835)
#fitFunctionBtag = TF1("fitFunctionBtag", "pol6", 60, 4000)
#fitFunctionBtag.SetParameters(0, 0, 0, 0, 0, 0)
print "Fitting the BTAG category:"
graphBtag.Fit(fitFunctionBtag)


graphAntiBtag = tfile.Get("SigEff_antibtag")
can2 = TCanvas()
can2.cd()
graphAntiBtag.Draw("AP")
#fitFunctionBtag.Draw("SAME")
#fitFunctionBtag.Draw()

#print type(fitFunctionBtag.GetParameters())
#print fitFunctionBtag.GetParameters()
for iParameter in range(0, fitFunctionBtag.GetNumberFreeParameters()):
  #  print parameter, ","
  print fitFunctionBtag.GetParameters()[iParameter], ",",
print
#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::TanH(TMath::Power(x-[1],[2])/[3])*TMath::Power((x/[4]),[5])", 649.992, 1000)
#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::TanH((x-[1])*[2])*TMath::Power(x,[3])+[4]", 650, 1000)
fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::ATan((x-[1])*[2])*TMath::Power(x,[3])+[4]", 650, 1000)
fitFunctionAntiBtag.SetParameters(0.16 , 650 , .002 , 0 , 0)
#fitFunctionAntiBtag = TF1("fitFunctionAntiBtag", "[0]*TMath::ATan((x-[1])/[2])+[3]", 650, 4000)
#fitFunctionAntiBtag.SetParameters(0.1, 700, 200,  .01)
print "Fitting the ANTIBTAG category"
graphAntiBtag.Fit(fitFunctionAntiBtag)

can1.Print("phSF_%s_sigEff_btag.root" % phSFvariation)
can2.Print("phSF_%s_sigEff_antibtag.root" % phSFvariation)

for iParameter in range(0, fitFunctionAntiBtag.GetNumberFreeParameters()):
  #  print parameter, ","
  print fitFunctionAntiBtag.GetParameters()[iParameter], ",",
print

