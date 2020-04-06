from ROOT import *
for category in ["antibtag", "btag"]:
  print "\n\n ====================================================================== \n"
  print "                   %s category " % category
  print "                  -------------------"
  inFile = TFile("quantifyWeightFactors_%s.root" % category)
  dataCan = inFile.Get("can_unweighted_data_%s" % category)
  weigCan = inFile.Get("can_weighted_data_%s" % category)
  diffCan = inFile.Get("can_perecent_diff_%s" % category)
  

  data = dataCan.GetPrimitive("unweighted_data_%s" % category)
  weig = weigCan.GetPrimitive("weighted_data_%s" % category)
  diff = diffCan.GetPrimitive("frac_diff_%s" % category)


  print "%56s" % "number of unweighted events in first bin:", data.GetBinContent(1)
  print "%56s" % "number of weighted events in first bin:", "%.4f" % weig.GetBinContent(1)
  print "%56s" % "percent difference due to weights in first bin:", "%.4f" % (100*diff.GetBinContent(1)), "%"
  #print " ... check: ", abs(data.GetBinContent(1) - weig.GetBinContent(1))/data.GetBinContent(1)
  
  #print "%56s" % "root's error on first bin of unweighted data:", "%.4f" % data.GetBinError(1)
  print "%56s" % "error on first bin of unweighted data:", "%.4f" % TMath.Sqrt(data.GetBinContent(1))
  dataFirstBinPercentErr = 100*TMath.Sqrt(data.GetBinContent(1))/data.GetBinContent(1)
  print "%56s" % "percent error on first bin of unweighted data:", "%.4f" % dataFirstBinPercentErr, "%"
  print "%56s" % "error on first bin of weighted data:", "%.4f" % TMath.Sqrt(weig.GetBinContent(1))
  #print "%56s" % "check error on first bin of weighted data:", "%.4f" % TMath.Sqrt(weig.GetBinContent(1))
  weigFirstBinPercentErr = 100*TMath.Sqrt(weig.GetBinContent(1))/weig.GetBinContent(1)
  print "%56s" % "percent error on first bin of weighted data:", "%.4f" % weigFirstBinPercentErr, "%"
  print "%56s" % "percent error changed by:", "%.4f" % (weigFirstBinPercentErr - dataFirstBinPercentErr), "%"
  print "%56s" % "change in error divided by original error:", "%.4f" % ((weigFirstBinPercentErr - dataFirstBinPercentErr)/dataFirstBinPercentErr)
  print "%56s" % "percent effect on error", "%.4f" % (100*(weigFirstBinPercentErr - dataFirstBinPercentErr)/dataFirstBinPercentErr), "%"
  

