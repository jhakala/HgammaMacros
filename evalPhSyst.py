from ROOT import *
files = {"antibtag" : {}, "btag" : {}}
phSFvars = ["up", "down", "nom"]
for phSFvariation in phSFvars:
  for category in files.keys():
    files[category][phSFvariation] = TFile("phSF_%s_sigEff_%s.root" % (phSFvariation, category))

canNames = {"antibtag" : "c1_n2", "btag" : "c1"}
graphs = {"antibtag" : {}, "btag" : {}}
for phSFvariation in phSFvars:
  for category in files.keys():

    #for key in files[category][phSFvariation].GetListOfKeys():
    #  print "\n----------"
    #  print files[category][phSFvariation].GetName()
    #  print key.GetName()
    #  print files[category][phSFvariation].Get(key.GetName()).GetName()
    #  print files[category][phSFvariation].Get(key.GetName()).IsA().GetName()
    #  print "----------\n"
    #for prim in files[category][phSFvariation].Get(canNames[category]).GetListOfPrimitives():
    #  print prim.GetName()
    #  print prim.IsA().GetName()

    graphs[category][phSFvariation] = files[category][phSFvariation].Get(canNames[category]).GetPrimitive("SigEff_%s" % category)
    graphs[category][phSFvariation].SetName("SigEff_%s_%s" % (category, phSFvariation))
  
from pprint import pprint
pprint(files)
pprint(graphs)

cans = {}
for category in files.keys():
  cans[category] = TCanvas()
  cans[category].SetName("phSystCan_%s" % category)
  graphs[category]["up"].Draw("AP")
  graphs[category]["down"].Draw("P SAME")

diffGraphs = {}
diffCans = {}
for category in files.keys():
  diffGraphs[category] = TGraph()
  diffGraphs[category].SetName("effDiffs_%s" % category)
  diffCans[category] = TCanvas()
  diffCans[category].SetName("effDiffCan_%s" % category)
  xxUp   = Double()
  xxDown = Double()
  xxNom  = Double()
  yyUp   = Double()
  yyDown = Double()
  yyNom  = Double()
  for point in range(0, graphs[category]["nom"].GetN()):
    graphs[category]["up"].GetPoint(point, xxUp, yyUp)
    graphs[category]["down"].GetPoint(point, xxDown, yyDown)
    graphs[category]["nom"].GetPoint(point, xxNom, yyNom)
    if xxUp != xxDown:
      print "got a point out of order"
      exit(1)
    diffGraphs[category].SetPoint(point, xxUp, (yyUp-yyDown)/yyNom)
  diffCans[category].cd()   
  diffGraphs[category].SetMarkerStyle(20)
  diffGraphs[category].Draw("AP")
