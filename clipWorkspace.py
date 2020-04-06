from ROOT import *

def clipWorkspace(inFile, newRange):
  
  mass = int(inFile.GetName().split("_")[2].replace(".root", ""))
  inWs = inFile.Get("Vg")
  
  pdfList = inWs.allPdfs()
  nPdfs = pdfList.getSize()
  
  pdfIt = pdfList.iterator()
  pdfNames = []
  for i in range(0, nPdfs):
    pdfNames.append(pdfIt.Next().GetName())
  
  if len(pdfNames) != 1:
    print "something is wrong with the input workspace, not exactly 1 pdfs found in workspace."
    exit(1)
  
  inPdf = inWs.pdf(pdfNames[0])
  if not "RooCBShape" in inPdf.IsA().GetName():
    print "something is wrong with the pdf in the workspace, it does not have type RooCBShape, instead it has type:", inPdf.IsA().GetName()
    exit(1)
  
  category = "antibtag" if "antibtag" in pdfNames[0] else "btag"
  
  varList =  inWs.allVars()
  nVars = varList.getSize()
  varIt = varList.iterator()
  
  newVars = []
  for i in range(0, nVars):
    #print varIt.Next().getValV()
    newVar = varIt.Next().Clone()
    if not "x" == newVar.GetName():
      newVars.append(newVar)
    
  print newVars
  for newVar in newVars:
    print newVar.GetName()
  
  newX = RooRealVar("x", "m_{X} (GeV)", newRange[0], newRange[1])
  newVars.append(newX)
  newCB = RooCBShape(pdfNames[0], "signal", newX, newVars[0], newVars[1], newVars[2], newVars[3])
  
  outWS = RooWorkspace("Vg")
  for var in newVars:
    getattr(outWS, "import")(var)
  getattr(outWS, "import")(newCB)
  from os import path, makedirs
  outDirName = "clipped_signalFits_%s" % category
  if not path.exists(outDirName):
    makedirs(outDirName)
  outWS.SaveAs(path.join(outDirName, "w_signal_%i.root" % mass))
  
  
if __name__ == "__main__":
  newRange = [720., 4720.]
  inFile = TFile("../dec18/w_signal_1000.root")
  clipWorkspace(inFile, newRange)
