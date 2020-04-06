from os import path, makedirs
from pprint import pprint
from sympy.solvers import solve
from sympy import Symbol, erf
from ROOT import *
from HgCuts import *

fixExpCoeff = False
quick = True
solutionLine = False

can = TCanvas()
can.cd()

graph = TGraph()
graph.SetNameTitle("turnOn", "turnOn")

if fixExpCoeff:
  nParams = 3
else: 
  nParams = 4
useWeightFactors=True
outDir = "jan26_mc_turnOns_functions_"
if useWeightFactors:
  outDir += "_withWeightFactors"
else:
  outDir += "_noWeightFactors"
if fixExpCoeff:
  outDir += "_fixedExp"
else:
  outDir += "_floatExp"
if not path.exists(outDir):
  makedirs(outDir)
  

#inFile = TFile("organize_DDs_btag-nom/data/ddTree_data2016SinglePhoton.root")
#inFile = TFile("organize_DDs_btag-nom/backgrounds/ddTree_gJets400To600.root")
inFile = TFile("organize_mcDDs_btag-nom/allMCbgs_withWeights.root")
tree = inFile.Get("higgs")
hist = TH1F("hist", "m_{j#gamma}", 500, 0, 5000)
hist.GetXaxis().SetRangeUser(400, 1400)
hist.GetXaxis().SetTitle("m_{j#gamma} (GeV)")
hist.GetYaxis().SetTitle("Events / 10 GeV")
hist.GetYaxis().SetTitleOffset(1.35)
jetMassWindows = []
turnOns=[]
expCoeffs = []
windowWidth = 30.

x = Symbol("x")
if fixExpCoeff:
  expCoeffFunc = TF1("expCoeffFunc", "TMath::Max([0]+[1]*TMath::ATan((x-[2])/[3]), -0.0064)", 40, 200) 
  #expCoeffFunc.SetParameters(-0.00523795357368,  0.00120007401227,  109.24343923,  24.3269585017)
  expCoeffFunc.SetParameters(-0.00529366792733, 0.00116711330691, 107.446268733, 23.0800140458)

if quick:
  for i in range(0,13):
    jetMassWindows.append([30.0+10.*i, 30.0+windowWidth+10.*i])
else:
  for i in range(0,121):
    jetMassWindows.append([30.0+1.*i, 30.0+windowWidth+1.*i])
#jetMassWindows.append([110.0,140.0])
first = True
cachedParameters = []
noFitCan = TCanvas()
if quick:
  noFitWindows = {kRed+1 : jetMassWindows[2], kOrange+1 : jetMassWindows[4], kYellow : jetMassWindows[6], kGreen+1 : jetMassWindows[8], kAzure : jetMassWindows[10]}
else:
  noFitWindows = {kRed+1 : jetMassWindows[20], kOrange+1 : jetMassWindows[40], kYellow : jetMassWindows[60], kGreen+1 : jetMassWindows[80], kAzure : jetMassWindows[100]}
noFitHists = []
firstNoFit = True;
for jetMassWindow in jetMassWindows:
  if fixExpCoeff:
    expCoeff = expCoeffFunc.Eval((jetMassWindow[0]+jetMassWindow[1])/2.)
    fit = TF1("fit", "[0]*TMath::Exp(%f*x)*(0.5+0.5*TMath::Erf((x-[1])/[2]))" % expCoeff, 0, 13000)
    if first:
      fit.SetParameters(11000, 600, 100)
      first = False
    else:
      fit.SetParameters(cachedParameters[0], cachedParameters[1], cachedParameters[2])
  else:
    fit = TF1("fit", "[0]*TMath::Exp([1]*x)*(0.5+0.5*TMath::Erf((x-[2])/[3]))", 0, 13000)
    if first:
      fit.SetParameters(107180, -0.00626, 500.3, 52.8)
      first = False
    else:
      fit.SetParameters(cachedParameters[0], cachedParameters[1], cachedParameters[2], cachedParameters[3])

  hist.SetTitle("m_{j#gamma}, %i GeV < m_{j} < %i GeV" % (int(jetMassWindow[0]), int(jetMassWindow[1])))
  if useWeightFactors:
    cut ="mcWeight*weightFactor*(%s)" % getNoBtagComboCut("higgs", True, True, jetMassWindow)
  else:
    cut = "mcWeight*(%s)" % getNoBtagComboCut("higgs", True, True, jetMassWindow)
  #print cut
  tree.Draw("phJetInvMass_puppi_softdrop_higgs >>hist", cut)
  for color, window in noFitWindows.iteritems():
    if window == jetMassWindow:
      noFitCan.cd()
      noFitHists.append(hist.Clone())
      cloneHistName = "%i GeV < m_{j} < %i GeV" % (int(jetMassWindow[0]), int(jetMassWindow[1]))
      noFitHists[-1].SetNameTitle(cloneHistName, cloneHistName)
      noFitHists[-1].SetMarkerColor(color)
      noFitHists[-1].SetLineColor(color)
      if firstNoFit:
        noFitHists[-1].Draw()
        firstNoFit = False
      else:
        noFitHists[-1].Draw("SAME")
      can.cd()
      #noFitCan.Print("noFit_massWindow%i-%i.pdf" % (int(jetMassWindow[0]), int(jetMassWindow[1])))

  can.cd()
  print "pre-fit parameter values:"
  for i in range(0, nParams):
    print str(fit.GetParameter(i)) + ",",
  print "\n",
  
  for i in range(0, 10):
    result = hist.Fit(fit, "SMLQ", "", 500, 2500)
  print "result of fit:", result.IsValid()
  i=2
  while not result.IsValid():
    if fixExpCoeff:
      fit.SetParameters(fit.GetParameter(0)+1000*i*(-1)**i, fit.GetParameter(1)+10*i*(-1)**i, fit.GetParameter(2)+5*i*(-1)**i)
    else:
      fit.SetParameters(fit.GetParameter(0)+1000*i*(-1)**(i+1), fit.GetParameter(1)+1e-4*i*(-1)**i, fit.GetParameter(2)+10*i*(-1)**i, fit.GetParameter(3)+5*i*(-1)**(i+1))
    result = hist.Fit(fit, "SLQ", "", 500, 2500)
    print "result of fit, try %i:" % i, result.IsValid()
    i += 1
  if result.IsValid():
    print "fit parameters:"
    for i in range(0, nParams):
      print str(fit.GetParameter(i)) + ",",
    print "\n",
   
  if fixExpCoeff:
    cachedParameters = [fit.GetParameter(0), fit.GetParameter(1), fit.GetParameter(2)]
    print cachedParameters
  else:
    cachedParameters = [fit.GetParameter(0), fit.GetParameter(1), fit.GetParameter(2), fit.GetParameter(3)]
    print cachedParameters
  erfComponent = TF1("erf", "[0]*(0.5+0.5*TMath::Erf((x-[1])/[2]))", 0, 13000)
  if fixExpCoeff:
    erfComponent.SetParameters(fit.GetMaximum(), fit.GetParameter(1), fit.GetParameter(2))
  else:
    erfComponent.SetParameters(fit.GetMaximum(), fit.GetParameter(2), fit.GetParameter(3))
  erfComponent.SetLineColor(kGray)
  erfComponent.SetLineStyle(7)
  expComponent = TF1("exp", "[0]*TMath::Exp([1]*x)", 0, 13000)
  if fixExpCoeff:
    expComponent.SetParameters(fit.GetParameter(0), expCoeff)
  else:
    expComponent.SetParameters(fit.GetParameter(0), fit.GetParameter(1))
    expCoeffs.append(([jetMassWindow[0], jetMassWindow[1]], fit.GetParameter(1)))
  expComponent.SetLineColor(kGray+2)
  expComponent.SetLineStyle(7)
  erfComponent.Draw("SAME")
  expComponent.Draw("SAME")
  gStyle.SetOptFit(0)
  gStyle.SetOptStat(0)
  #for prim in can.GetListOfPrimitives():
  #  if hasattr(prim, 'GetName'):
  #    print prim.GetName()
  print "solution for mass window", jetMassWindow, ":"
  if fixExpCoeff:
    solution = solve(-0.99 + 0.5 + 0.5*(erf((x-fit.GetParameter(1))/fit.GetParameter(2))), x)
  else:
    solution = solve(-0.99 + 0.5 + 0.5*(erf((x-fit.GetParameter(2))/fit.GetParameter(3))), x)
  print solution
  if len(solution) == 1:
    if jetMassWindow[1]-jetMassWindow[0] == windowWidth:
      graph.SetPoint(graph.GetN(), (jetMassWindow[0]+jetMassWindow[1])/float(2), solution[0])
  else:
    print "... did not get exactly one solution for this mass window"
  turnOns.append(([jetMassWindow[0],jetMassWindow[1]], solution[0]))
  if solutionLine:
    line = TLine(solution[0], 0, solution[0], can.GetFrame().GetY2())
    line.SetLineColor(kBlack)
    line.Draw("SAME")
    text = TPaveText(solution[0]+can.GetFrame().GetX2()/16., can.GetFrame().GetY2()/12., solution[0]+can.GetFrame().GetX2()/16. , can.GetFrame().GetY2()/12.)
    text.AddText("m_{j\gamma}=%01d GeV" % solution[0])
    text.SetTextSize(0.03)
    text.Draw("SAME")
  can.Print(path.join(outDir, "turnOn_%i-%i.pdf" % (int(jetMassWindow[0]), int(jetMassWindow[1]))))
  

can2=TCanvas()
can2.cd()
graph.Draw()
can2.Print(path.join(outDir, "turnOnGraph.pdf"))

pprint(turnOns)

if fixExpCoeff:
  outFile = TFile("turnOnFits_fixedExp.root", "RECREATE")
else:
  outFile = TFile("turnOnFits.root", "RECREATE")
outFile.cd()
graph.Write()
print expCoeffs
expCoeffGraph = TGraph()
expCoeffGraph.SetNameTitle("expCoeffs", "expCoeffs")
expCoeffHist = TH1F("exp", "exp", 200, -1, 1)
for expCoeff in expCoeffs:
  expCoeffGraph.SetPoint(expCoeffGraph.GetN(), (expCoeff[0][0]+expCoeff[0][1])/2., expCoeff[1])
  expCoeffHist.Fill(expCoeff[1])
expCoeffGraph.Write()
expCoeffHist.Write()
outFile.Close()
noFitCan.BuildLegend()
noFitHists[0].SetTitle("comparison of m_{j#gamma} spectra in different m_{j} sidebands")
outFileNoFit = TFile("noFitCan.root", "RECREATE")
noFitCan.Write()
outFileNoFit.Close()
noFitCan.Print("noFit_overlay.pdf") 
