from ROOT import *
from HgParameters import getSamplesDirs
from HgCuts import getBtagComboCut, getAntiBtagComboCut

def makeRatioPlots(sidebandsReversed, rebin=1):
  sidebands = [sidebandsReversed[1], sidebandsReversed[0]]
  inFile = TFile(getSamplesDirs()["dataDDFile"])
  inTree = inFile.Get("higgs")
  
  def getSidebandName(sideband):
    return str(int(sideband[0]))+str(int(sideband[1]))
  
  def getHistName(category, sideband):
    return category + "Hist" + getSidebandName(sideband)

  cuts={}
  cuts["antibtag"] = {
                        getSidebandName(sidebands[0]): "weightFactor*(%s)" % getAntiBtagComboCut("higgs", True, True, False, [sidebands[0][0],sidebands[0][1]]),
                        getSidebandName(sidebands[1]): "weightFactor*(%s)" % getAntiBtagComboCut("higgs", True, True, False, [sidebands[1][0],sidebands[1][1]])
                     }
  cuts["btag"]     = {
                        getSidebandName(sidebands[0]): "weightFactor*(%s)" % getBtagComboCut("higgs", True, True, False, [sidebands[0][0],sidebands[0][1]]),
                        getSidebandName(sidebands[1]): "weightFactor*(%s)" % getBtagComboCut("higgs", True, True, False, [sidebands[1][0],sidebands[1][1]])
                     }
  
  
  cans = {}
  hists = {}
  categories = ["antibtag", "btag"]
  #sidebands = [[100., 110.], [110., 140.]]
  norms={}
  ratios = {}
  
  for category in categories:
    hists[category]={}
    norms[category]={}
    canName = "can_%s-%s_and_%s-%s_" % (int(sidebands[0][0]), int(sidebands[0][1]), int(sidebands[1][0]), int(sidebands[1][1]))+category
    cans[category] = TCanvas(canName, canName)
    ratioName = "ratio_%s-%s_over_%s-%s_" % (int(sidebands[0][0]), int(sidebands[0][1]), int(sidebands[1][0]), int(sidebands[1][1]))+category
    ratios[category]=TH1F(ratioName, ratioName, 3000, 720, 3720)
    ratios[category].Rebin(rebin)
    first = True
    inTree.Draw("phJetInvMass_puppi_softdrop_higgs >> %s" % ratios[category].GetName(), cuts[category][getSidebandName(sidebands[0])])
    for sideband in sidebands:
      hists[category][getSidebandName(sideband)] = TH1F(getHistName(category, sideband), getHistName(category, sideband), 3000, 720, 3720)
      cut = cuts[category][getSidebandName(sideband)]
      inTree.Draw("phJetInvMass_puppi_softdrop_higgs >> %s" % hists[category][getSidebandName(sideband)].GetName(), cut)
      norms[category][getSidebandName(sideband)] = hists[category][getSidebandName(sideband)].GetSumOfWeights()
      hists[category][getSidebandName(sideband)].Rebin(rebin)
  
  
  ratioCans = {}
  for category in categories:
    outFileName = "sbRatios/%s_sb_ratios_%i-%i_over_%i-%i.root" % (category, int(sidebands[0][0]), int(sidebands[0][1]), int(sidebands[1][0]), int(sidebands[1][1]))
    print "making file", outFileName
    outFile = TFile(outFileName, "RECREATE")
    ratioCanName = "ratioCan_%s-%s_over_%s-%s_" % (int(sidebands[0][0]), int(sidebands[0][1]), int(sidebands[1][0]), int(sidebands[1][1]))+category
    cans[category].cd()
    hists[category][getSidebandName(sidebands[0])].Draw()
    hists[category][getSidebandName(sidebands[0])].SetMarkerColor(kGreen)
    hists[category][getSidebandName(sidebands[0])].SetLineColor(kGreen)
  
    cans[category].cd()
    ratios[category].Divide(hists[category][getSidebandName(sidebands[1])])
    hists[category][getSidebandName(sidebands[1])].Scale(norms[category][getSidebandName(sidebands[0])]/norms[category][getSidebandName(sidebands[1])])
    hists[category][getSidebandName(sidebands[1])].Draw("SAME")
    hists[category][getSidebandName(sidebands[1])].SetMarkerColor(kRed)
    hists[category][getSidebandName(sidebands[1])].SetLineColor(kRed)
    cans[category].Modified()
    cans[category].Update()
    ratioCans[category] = TCanvas(ratioCanName)
    ratioCans[category].cd()
    ratios[category].Draw()
    ratioCans[category].Print("sbRatios/%s_sb_ratios_%i-%i_over_%i-%i.pdf" % (category, int(sidebands[0][0]), int(sidebands[0][1]), int(sidebands[1][0]), int(sidebands[1][1])))
    ratios[category].Write()
    hists[category][getSidebandName(sidebands[0])].Write()
    hists[category][getSidebandName(sidebands[1])].Write()
  outFile.Close()
  print "wrote file", outFile.GetName()


if __name__ == "__main__":
  sidebands = [[100., 110.], [110., 140.]]
  makeRatioPlots(sidebands)
