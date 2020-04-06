
def collectStacks(antibtagDir, btagDir):
  from glob import glob
  from os.path import join, exists, basename
  from pprint import pprint
  antibtagFiles = glob(join(antibtagDir,"*.root"))
  btagFiles     = glob(join(btagDir,"*.root"))
  print "antibtagFiles:", antibtagFiles
  print "btagFiles:", btagFiles
  matches = {}
  for btagFile in btagFiles:
    print "found btagFile", btagFile
    match = btagFile.replace("btag", "antibtag")
    print "looking for antibtagFile", match
    if exists(match):
      print "found matching file:", match  
      matches[basename(btagFile).replace("btag_", "")] = {"antibtag" : match, "btag" : btagFile}
    else:
      print "did not find matching file:", match
      exit(1)
  pprint(matches)

if __name__ == "__main__":
  from os.path import isdir
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument(  '--antibtagIn', dest="antibtagIn", default="stackplots_antibtag",
                        help = "the input antibtag dir [default=stackplots_antibtag]"
                     )
  parser.add_argument(  '--btagIn', dest="btagIn", default="stackplots_btag",
                        help = "the input btag dir [default=stackplots_btag]"
                     )
  args=parser.parse_args()
  if not args.antibtagIn:
    print "please supply an antibtag input dir using the antibtagIn option"
    exit(1)
  elif not isdir(args.antibtagIn):
    print "the antibtag input dir is not valid:", args.antibtagIn
    exit(1)
  print "antibtagIn is", args.antibtagIn
  if not args.btagIn:
    print "please supply an btag input dir using the btagIn option"
    exit(1)
  elif not isdir(args.btagIn):
    print "the btag input dir is not valid:", args.btagIn
    exit(1)
  print "btagIn is", args.btagIn

  collectStacks(args.antibtagIn, args.btagIn)
