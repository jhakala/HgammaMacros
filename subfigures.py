#!/usr/bin/env python
def getVariableTex():
  varDict = {}
  varDict["higgsJet_puppi_softdrop_abseta"]    = "$\left|\eta_{J}\\right|$"
  varDict["leadingPhEta"]              = "$\eta_{\gamma}$"
  varDict["higgsJet_HbbTag"]           = "H$b\\bar{b}$ tagger discriminant"
  varDict["phJetDeltaR_higgs"]         = "$\Delta$R($\gamma$, jet)"
  varDict["leadingPhPt"]               = "$p_{T}^{\gamma}$ (GeV)"
  varDict["higgsJett2t1"]              = "$\\tau_{21}$"
  varDict["leadingPhAbsEta"]           = "$\left|\eta_{\gamma}}\\right$"
  varDict["phPtOverMgammaj"]           = "$p_{T}^{\gamma}/m_{j\gamma}$"
  varDict["leadingPhPhi"]              = "$\phi_{\gamma}$"
  varDict["cosThetaStar"]              = "$\left|cos(\\theta*)$"
  varDict["phJetInvMass_puppi_softdrop_higgs"] = "$m_{j\gamma}$ (GeV)"
  varDict["higgsPuppi_softdropJetCorrMass"]    = "$m_{j}^{PUPPI+SD}$ (GeV)"
  return varDict
from sys import argv

fileName = argv[1]
shortName = argv[2]
varNames = getVariableTex()
found = False
for key in varNames:
  if key in argv[1]:
    print "variable name =", varNames[key]
    if "Abs" in varNames[key] and "Abs" not in argv[1]:
      continue
    varName = varNames[key]
    found = True
if not found:
  print "variable not found"
  exit(1)

category = "btag"
caveat1 = "before applying double-b tagging scale factors"
caveat2 = "with application of double-b tagging scale factors"
namePrefix1 = "%s_noSF" % category
namePrefix2 = "%s_withSF" % category
directory1  = "scalefactors/pdf_stackplots_%s" % category
directory2  = "scalefactors/pdf_stackplots_%s_SF" % category

print '''

\subfigure[%s, %s]{\label{subfig:%s_%s}
\includegraphics[width=0.35\\textwidth]{figs/%s/%s}
}
\subfigure[%s, %s]{\label{subfig:%s_%s}
\includegraphics[width=0.35\\textwidth]{figs/%s/%s}
}\\\\

''' % (varName, caveat1, namePrefix1, shortName, directory1, fileName, 
       varName, caveat2, namePrefix2, shortName, directory2, fileName)
