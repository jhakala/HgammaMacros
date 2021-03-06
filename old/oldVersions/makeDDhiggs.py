from os import path, makedirs
import subprocess
from math import sqrt
from ROOT import *
from tcanvasTDR import TDRify

def makeDDhiggs(argv1, argv2, argv3, argv4, argv5, argv6, argv7, argv8):
    argv=[ "leethax", argv1, argv2, argv3, argv4, argv5, argv6, argv7, argv8]
    print argv

    cosThetaCut   = True;
    compareOldCut = False;
    showSignal    = True;

    dataFile = TFile("../HgammaSamples/ddTrees/ddNew_silver.root")
    sig750File   = TFile("../HgammaSamples/ddTrees/ddNew_Hgamma_m750.root")
    sig1000File  = TFile("../HgammaSamples/ddTrees/ddNew_Hgamma_m1000.root")
    sig2000File  = TFile("../HgammaSamples/ddTrees/ddNew_Hgamma_m2000.root")
    sig3000File  = TFile("../HgammaSamples/ddTrees/ddNew_Hgamma_m3000.root")

    trees = []
    data          = dataFile.Get(   "higgs"  )
    trees.append(data)
    sig750        = sig750File.Get( "higgs"  )
    trees.append(sig750)
    sig1000       = sig1000File.Get("higgs"  )
    trees.append(sig1000)
    sig2000       = sig2000File.Get("higgs"  )
    trees.append(sig2000)
    sig3000       = sig3000File.Get("higgs"  )
    trees.append(sig3000)
    for tree in trees:
        print tree

    print "using sideband %s"%argv[3]
    if (argv[3]=="100to110"):
        sidebandName = "side100110"
        sidebandIndex = "Four"
    elif (argv[3]=="50to70"):
        sidebandName = "side5070"
        sidebandIndex = "Three"
    else:
        exit("please pick the sideband range: either 100to110 or 50to70.")
    sideLow = dataFile.Get(sidebandName)

    phoEtaMaxEB   = 1.4442
    phoEtaMaxEE   = 2.5
    phoEtaMinEE   = 1.566
    jetEtaMax   = 2.2
    deltaRmin   = 1.1
    #cosThetaMax = 0.6

    massWindowLo = int(argv[4])
    massWindowHi = int(argv[5])

    dataCutsArray     = []
    sidebandCutsArray = []
    if argv[8]=="EB":
        phoEtaCut           = TCut("leadingPhAbsEta<%s"               % str(phoEtaMaxEB  ) )
    if argv[8]=="EE":
        phoEtaCut           = TCut("%s<leadingPhAbsEta&&leadingPhAbsEta<%s"               % ( str(phoEtaMinEE),str(phoEtaMaxEE) ) )
    if argv[8]=="EBEE":
        phoEtaCut           = TCut("leadingPhAbsEta<%s"               %  str(phoEtaMaxEE)  )
    deltaRdataCut       = TCut("phJetDeltaR_higgs>%s"             % str(deltaRmin  ) )
    deltaRsidebandCut   = TCut("phJetDeltaR_sideLow%s>%s"         % ( sidebandIndex, str(deltaRmin)) )
    jetEtaDataCut       = TCut("higgsJet_pruned_abseta<%s"        % str(jetEtaMax  ) )
    jetEtaSidebandCut   = TCut("sideLow%sJet_pruned_abseta<%s"% (sidebandIndex, str(jetEtaMax)) )
    cosThetadataCut     = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_higgs-750)/250"                                          )
    cosThetasidebandCut = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_sideLow%s-750)/250"  % sidebandIndex                   )

    dataMassCuts         = TCut("(phJetInvMass_pruned_higgs>%s)&&(phJetInvMass_pruned_higgs<%s)"               % ( str(massWindowLo), str(massWindowHi) )    )
    sidebandMassCuts     = TCut("(phJetInvMass_pruned_sideLow%s>%s)&&(phJetInvMass_pruned_sideLow%s<%s)" % ( sidebandIndex, str(massWindowLo), sidebandIndex, str(massWindowHi) )    )

    if not argv[1]=="leadingPhAbsEta":
        dataCutsArray.append(      phoEtaCut   )
        sidebandCutsArray.append(  phoEtaCut   )

    if not argv[1]=="phJetDeltaR_higgs":
        dataCutsArray.append(      deltaRdataCut   )
        sidebandCutsArray.append(  deltaRsidebandCut   )

    if not argv[1]=="higgsJet_pruned_abseta":
        dataCutsArray.append(      jetEtaDataCut   )
        sidebandCutsArray.append(  jetEtaSidebandCut   )

    if not argv[1]=="cosThetaStar":
        dataCutsArray.append(      cosThetadataCut   )
        sidebandCutsArray.append(  cosThetasidebandCut   )

    dataCutsArray.append(      dataMassCuts   )
    sidebandCutsArray.append(  sidebandMassCuts   )
    dataCuts = TCut()
    sidebandCuts = TCut()

    for cut in sidebandCutsArray:
        sidebandCuts += cut
    #masscutSideband += sidebandMassCuts + deltaRsidebandCut + phoEtaCut + cosThetasidebandCut
    for cut in dataCutsArray:
        dataCuts += cut

    print "the cut string for the signal region is %s" % dataCuts
    print "the cut string for the sideband region is %s" % sidebandCuts


    c = TCanvas()
    c.SetLogy()
    data.Draw(argv[1], dataCuts)

    primitives = []

    data.Draw(argv[1], dataCuts)
    for primitive in c.GetListOfPrimitives():
        primitive.SetName("data")
        primitive.SetBinErrorOption(TH1.kPoisson)
        primitive.SetLineColor(kBlack)
        primitives.append(primitive.GetName())
    print "\n \n first list of primitives:"
    for primitive in c.GetListOfPrimitives():
        print primitive

    dataEntries = c.GetPrimitive("data").GetEntries()
    print "data has %i entries" % dataEntries

    sideLow.Draw(argv[2], sidebandCuts, "SAME")
    for primitive in c.GetListOfPrimitives():
        if not primitive.GetName()=="data":
            primitive.SetName("sideband")
            primitive.SetBinErrorOption(TH1.kPoisson)
            primitives.append(primitive.GetName())
    sidebandEntries = c.GetPrimitive("sideband").GetEntries()
    print "sideband has %i entries" % sidebandEntries
    sidebandNormalization = dataEntries/sidebandEntries
    print "sideband normalization factor is %f" % sidebandNormalization
    for sidebandBin in range(0, c.GetPrimitive("sideband").GetNbinsX()):
        c.GetPrimitive("sideband").SetBinContent(sidebandBin, c.GetPrimitive("sideband").GetBinContent(sidebandBin)*sidebandNormalization)
    c.GetPrimitive("sideband").SetLineColor(kGreen)

    if compareOldCut:
        dataOld.Draw(argv[1], dataOldCuts, "SAME")
        for primitive in c.GetListOfPrimitives():
            if not primitive.GetName() in primitives:
                primitive.SetName("dataOld")
                primitive.SetLineColor(kBlack)
                primitives.append(primitive.GetName())
        dataOldEntries = c.GetPrimitive("dataOld").GetEntries()
        print "dataOld has %i entries" % dataOldEntries

        sideLowOld.Draw(argv[2], sidebandOldCuts, "SAME")
        for primitive in c.GetListOfPrimitives():
            print "initial:"
            print primitive
            if not primitive.GetName() in primitives:
                primitive.SetName("sidebandOld")
                primitive.SetBinErrorOption(TH1.kPoisson)
                primitives.append(primitive.GetName())
        sidebandOldEntries = c.GetPrimitive("sidebandOld").GetEntries()
        print "sidebandOld has %i entries" % sidebandOldEntries
        sidebandOldNormalization = dataOldEntries/sidebandOldEntries
        print "sidebandOld normalization factor is %f" % sidebandOldNormalization
        for sidebandOldBin in range (0, c.GetPrimitive("sidebandOld").GetNbinsX()):
            c.GetPrimitive("sidebandOld").SetBinContent(sidebandOldBin, c.GetPrimitive("sidebandOld").GetBinContent(sidebandOldBin)*sidebandOldNormalization)
        c.GetPrimitive("sidebandOld").SetLineColor(kRed)

    print "\n\n List of primitives on c:"
    for primitive in c.GetListOfPrimitives():
        print primitive

    if showSignal:
        if argv[6] == "only750" or argv[6] == "all":
            sig750.Draw(argv[1], dataCuts, "SAME")
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives:
                    print "found new primitive with name %s" % primitive.GetName()
                    primitive.SetName("signal750")
                    for sigBin in range (0, primitive.GetNbinsX()):
                        primitive.SetBinContent(sigBin, primitive.GetBinContent(sigBin)*3)
                    print "found updated primitive with name %s" % primitive.GetName()
                    primitives.append(primitive.GetName())


        if argv[6] == "only1000" or argv[6] == "all" :
            sig1000.Draw(argv[1], dataCuts, "SAME")
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives:
                    print "found new primitive with name %s" % primitive.GetName()
                    primitive.SetName("signal1000")
                    print "found updated primitive with name %s" % primitive.GetName()
                    primitives.append(primitive.GetName())
        if argv[6] == "only2000" or argv[6] == "all" :
            sig2000.Draw(argv[1], dataCuts, "SAME")
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives:
                    print "found new primitive with name %s" % primitive.GetName()
                    primitive.SetName("signal2000")
                    print "found updated primitive with name %s" % primitive.GetName()
                    primitives.append(primitive.GetName())


        if argv[6] == "only3000" or argv[6] == "all" :
            sig3000.Draw(argv[1], dataCuts, "SAME")
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives:
                    print "found new primitive with name %s" % primitive.GetName()
                    primitive.SetName("signal3000")
                    print "found updated primitive with name %s" % primitive.GetName()
                    primitives.append(primitive.GetName())
    c.Update()
    c.Draw()
    #sig.Draw("higgsJet_pruned_abseta", dataCuts, "SAME")
    #for primitive in c.GetListOfPrimitives():
    #    print primitive
    #    if not primitive.GetName() in primitives:
    #        print "found new primitive with name %s" % primitive.GetName()
    #        primitive.SetName("signal")
    #        print "found updated primitive with name %s" % primitive.GetName()

    ymax=0
    for primitive in c.GetListOfPrimitives():
        if primitive.GetName() in ["sideband", "sidebandOld", "signal750",  "signal1000", "signal2000", "signal3000", "data", "dataOld"]:
            primitive.Rebin(5)
            if "signal" in primitive.GetName():
                for sigBin in range(0, c.GetPrimitive(primitive.GetName()).GetNbinsX()):
                    c.GetPrimitive(primitive.GetName()).SetBinContent(sigBin, c.GetPrimitive(primitive.GetName()).GetBinContent(sigBin)*0.1)
            if primitive.GetMaximum()>ymax:
                ymax = primitive.GetMaximum()

    for primitive in c.GetListOfPrimitives():
        print "final: "
        print primitive
        if primitive.GetName() in primitives:
            primitive.GetYaxis().SetRangeUser(1, ymax*5)

    c.Draw()
    c.Update()
    c2 = TCanvas()
    c2.cd()
    c2.SetLogy()
    if compareOldCut:
        c.GetPrimitive("sideband").SetLineColor(kBlue)
        c.GetPrimitive("sideband").SetMarkerStyle(20)
        c.GetPrimitive("sideband").SetMarkerColor(kBlue)
        c.GetPrimitive("sideband").Draw("pE0")
        c.GetPrimitive("sidebandOld").SetLineColor(kGray)
        c.GetPrimitive("sidebandOld").SetFillColor(kOrange)
        c.GetPrimitive("sidebandOld").SetFillStyle(3004)
        c.GetPrimitive("sidebandOld").Draw("SAME")
    else:
        c.GetPrimitive("sideband").SetLineColor(kOrange+2)
        c.GetPrimitive("sideband").SetFillColor(kOrange)
        c.GetPrimitive("sideband").Draw()
        bgErrs = c.GetPrimitive("sideband").Clone()
        for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
            bgErrs.SetBinError(sidebandBin, c.GetPrimitive("sideband").GetBinError(sidebandBin)*sidebandNormalization)
        bgErrs.SetFillColor(kOrange-6)
        bgErrs.SetFillStyle(3018)
        bgErrs.Draw("E2 SAME")
        c.GetPrimitive("data").SetMarkerStyle(20)
        c.GetPrimitive("data").SetMarkerColor(kBlack)
        if argv[7]=="showData":
            c.GetPrimitive("data").Draw("apE0 SAME")
    c2.Draw()
    if showSignal:
        if argv[6] == "only750" or argv[6] == "all" :
            c.GetPrimitive("signal750").SetLineWidth(3)
            c.GetPrimitive("signal750").SetLineStyle(6)
            c.GetPrimitive("signal750").SetLineColor(kBlue)
            c.GetPrimitive("signal750").Draw("SAME")
        if argv[6] == "only1000" or argv[6] == "all" :
            c.GetPrimitive("signal1000").SetLineWidth(3)
            c.GetPrimitive("signal1000").SetLineStyle(6)
            c.GetPrimitive("signal1000").SetLineColor(kGreen)
            c.GetPrimitive("signal1000").Draw("SAME")
        if argv[6] == "only2000" or argv[6] == "all" :
            c.GetPrimitive("signal2000").SetLineWidth(3)
            c.GetPrimitive("signal2000").SetLineStyle(6)
            c.GetPrimitive("signal2000").SetLineColor(kRed)
            c.GetPrimitive("signal2000").Draw("SAME")
        if argv[6] == "only3000" or argv[6] == "all" :
            c.GetPrimitive("signal3000").SetLineWidth(3)
            c.GetPrimitive("signal3000").SetLineStyle(6)
            c.GetPrimitive("signal3000").SetLineColor(kCyan)
            c.GetPrimitive("signal3000").Draw("SAME")
    c2.Draw()
    outputDirName="output_Higgs_sideband%s_masswindow%i-%i"%(sidebandName, massWindowLo, massWindowHi)
    if not path.exists(outputDirName):
          makedirs(outputDirName)
    outfile = TFile("%s/%s_canvas.root"%(outputDirName, argv[1]),"RECREATE")
    outfile.cd()

    c.GetPrimitive("sideband").Clone().Write()
    if compareOldCut:
        c.GetPrimitive("sidebandOld").Clone().Write()
    c2.Write()
    outfile.Close()

    print "\nOutput tcanvas is:\n%s"%outfile.GetName()
    c2.Update()
    c2.Draw()

    print "about to do c2 = TDRify(" + "'c2', " + "'%s_%s_%s_M%s-%s"%(argv[1], argv[3], argv[8], argv[4], argv[5]) + "', '" + outputDirName +"')"
    outputFilename = TDRify(c2, "%s_%s_%s_M%s-%s"%(argv[1], argv[3], argv[8], argv[4], argv[5]), outputDirName)
    return outputFilename
