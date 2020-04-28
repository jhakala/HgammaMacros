import os
from ROOT import *
# function to compile a C/C++ macro for loading into a pyroot session
# John Hakala - May 11, 2016

debugFlag = False

def isOrIsNot(boolean, singularOrPlural):
  if singularOrPlural == "singular":
    return "is" if boolean else "isn't"
  else:
    return "are" if boolean else "aren't"

def deleteLibs(macroName):
        # remove the previously compiled libraries
   if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
      os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
   if os.path.exists(macroName+"_C.d"):
      os.remove(macroName+"_C.d")
   if os.path.exists(macroName+"_C.so"):
      os.remove(macroName+"_C.so")
        # compile the macro using g++

def instance(macroName, opt):
  # call the compiling function to compile the macro, then run its Loop() method
  #args: macro name, [input filename, output filename, load/compile]
  if (not (isinstance(macroName, basestring) and isinstance(opt, basestring))):
     print "please supply two arguments to pyrootTools.instance :  the class name (should be the same as the tree name) and either 'load' or 'compile'."   
     exit(1)
  elif not (opt=="load" or opt=="compile"):
     print "for the second argument, please pick 'load' or 'compile'."
     exit(1)
  else:
     if(debugFlag): print "\nAttempting to %s %s.\n" % (opt, macroName)
     pastTense = "loaded" if opt=="load" else "compiled"
  if opt=="compile":
     deleteLibs("%s"%macroName)
     exitCode = gSystem.CompileMacro("%s.C"%macroName, "gOck")
     success=(exitCode==1)
  elif opt=="load":
     exitCode = gSystem.Load('%s_C'%macroName)
     success=(exitCode>=-1)
  if not success:
     print "\nError... %s failed to %s. :-("%(macroName, opt)
     print "Make sure you're using an up-to-date version of ROOT by running cmsenv in a 7_4_X>=16 CMSSW area."
     exit(1)
  else:
     if(debugFlag): print "\n%s %s successfully."%(macroName, pastTense)
     if opt=="compile":
        gSystem.Load('%s_C'%macroName)

def drawInNewCanvas(hist, opt=""):
  newCan = TCanvas()
  newCan.cd()
  hist.Draw(opt)

def drawWithCutInNewCanvas(tree, var, comboCut, label):
  newCan = TCanvas()
  newCan.cd()
  tree.Draw(var, comboCut)
  newCan.Print("%s_%s.pdf"%(var, label))

def getSortedDictKeys(inDict):
  keyNumList = []
  allKeysAreInts    = True
  allKeysAreStrings = True
  allKeysAreFloats  = True
  for key in inDict.keys(): 
    if type(key) is not int:
      allKeysAreInts = False
    else:
      keyNumList.append(key)
    if type(key) is not str:
      allKeysAreStrings = False
    else:
      keyNumList.append(int(key))
    if type(key) is not float:
      allKeysAreFloats = False
    else:
      keyNumList.append(key)

  keyNumList.sort()
  #print "allKeysAreStrings: %r" % allKeysAreStrings
  #print "allKeysAreInts: %r" % allKeysAreInts
  #print "allKeysAreFloats: %r" % allKeysAreFloats
  if allKeysAreStrings:
    keyStrList = []
    for key in keyNumList:
      keyStrList.append(str(key))
    return keyStrList
  else:
    return keyNumList
