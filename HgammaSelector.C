#define HgammaSelector_cxx
#include "HgammaSelector.h"
#include "LinkDef.h"

using namespace std;

// Class for analyzing the flatTuples from the EXOVVNtuplizer
// The output gives a few trees -- all of which are focused on a V/H(fatjet)gamma resonance
// The trees differ in the AK8 jet mass cuts -- different windows are used for different bosons 
// John Hakala -- May 11, 2016

void HgammaSelector::Loop(string outputFileName, int btagVariation, int phSFvariation, float mcWeight) {
  cout << "output filename is: " << outputFileName << endl;
  // Flags for running this macro
  bool debugFlag                     =  false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool debugSF                       =  false ; 
  bool checkTrigger                  =  false ;
  bool dumpEventInfo                 =  false ;
  //bool ignoreAllCuts                 =  false ;
  bool noHLTinfo                     =  false  ;  // This is for the 2016 MC with no HLT info
  int  entriesToCheck                =  100000000 ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                   =  5000  ;

  // Photon id cut values
  float endcap_phoMVAcut             = 0.20 ;  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2016
  float barrel_phoMVAcut             = 0.20 ;
  float phoEtaMax                    =   2.4 ;
  float jetEtaMax                    =   2.4 ;
  //float jetT2T1Max                   =   0.5 ;
  float phoEtaRanges[5]              = {0, 0.75, 1.479, 2.4, 3.0};

  // for looking at cached trigger firing results
  //bool loadEventMap = true;
  //TFile* eventMapFile = TFile::Open("eventMap_HLT_Photon200.root", "READ");
  //cout << "eventMapFile " << eventMapFile << endl;
  //TTree* eventMapTree = (TTree*) eventMapFile->Get("eventMap");
  //cout << "eventMapTree " << eventMapTree << endl;
  //TBranch *b_eventMap = 0;
  //if (loadEventMap) {
  //  cout << "About to set branch address" << endl;
  //  eventMapTree->SetBranchAddress("eventMap", &eventMap, &b_eventMap);
  //  cout << "About to LoadTree" << endl;
  //  Long64_t tentry = eventMapTree->LoadTree(0);
  //  cout << "About to GetEntry" << endl;
  //  b_eventMap->GetEntry(tentry);
  //  cout << "Finished GetEntry" << endl;
  //}

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");
  outputFile->cd();

  //TTree* outputTreeSig    = new TTree("sig",               "sig");
  TTree* outputTreeHiggs  = new TTree("higgs",           "higgs");
  outputTreeHiggs -> SetAutoSave(-500000000);

  outputTreeHiggs->Branch("higgsJett2t1", &higgsJett2t1);
  outputTreeHiggs->Branch("higgsJet_DDBtag", &higgsJet_DDBtag);
  outputTreeHiggs->Branch("cosThetaStar", &cosThetaStar);
  outputTreeHiggs->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeHiggs->Branch("leadingPhEta", &leadingPhEta);
  outputTreeHiggs->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeHiggs->Branch("leadingPhPt", &leadingPhPt);
  outputTreeHiggs->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeHiggs->Branch("phJetInvMass_softdrop_higgs", &phJetInvMass_softdrop_higgs);
  outputTreeHiggs->Branch("phJetDeltaR_higgs", &phJetDeltaR_higgs);
  outputTreeHiggs->Branch("higgsJet_abseta", &higgsJet_abseta);
  outputTreeHiggs->Branch("higgsJet_eta", &higgsJet_eta);
  outputTreeHiggs->Branch("higgsJet_phi", &higgsJet_phi);
  outputTreeHiggs->Branch("higgsJet_pt", &higgsJet_pt);
  outputTreeHiggs->Branch("higgs_softdropJetCorrMass", &higgs_softdropJetCorrMass);
  outputTreeHiggs->Branch("triggerFired_165HE10", &triggerFired_165HE10);
  outputTreeHiggs->Branch("triggerFired_200", &triggerFired_200);
  outputTreeHiggs->Branch("antibtagSF", &antibtagSF);
  outputTreeHiggs->Branch("btagSF", &btagSF);
  outputTreeHiggs->Branch("weightFactor", &weightFactor);
  outputTreeHiggs->Branch("mcWeight", &mcWeight);


  // Branches from EXOVVNtuplizer tree
  fChain->SetBranchStatus( "*"                        ,  0 );  // disable all branches
  fChain->SetBranchStatus( "HLT_isFired"              ,  1 );  // activate select branches
  fChain->SetBranchStatus( "ph_pt"                    ,  1 );  
  fChain->SetBranchStatus( "ph_e"                     ,  1 );  
  fChain->SetBranchStatus( "ph_eta"                   ,  1 );  
  fChain->SetBranchStatus( "ph_phi"                   ,  1 );  
  fChain->SetBranchStatus( "ph_mvaVal"                ,  1 );
  fChain->SetBranchStatus( "ph_mvaCat"                ,  1 );
  fChain->SetBranchStatus( "ph_passEleVeto"           ,  1 );
  //fChain->SetBranchStatus( "jetAK4_pt"                ,  1 );  
  //fChain->SetBranchStatus( "jetAK4_IDLoose"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK8_softdrop_mass"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_softdrop_massCorr"   ,  1 );
  fChain->SetBranchStatus( "jetAK8_e"                 ,  1 );  
  fChain->SetBranchStatus( "jetAK8_eta"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_phi"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau1"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau2"              ,  1 );  
  //fChain->SetBranchStatus( "jetAK8_tau3"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTight"           ,  1 );  
  //fChain->SetBranchStatus( "jetAK8_IDTightLepVeto"    ,  1 );  
  fChain->SetBranchStatus( "jetAK8_DDB"            ,  1 );  
  //fChain->SetBranchStatus("EVENT_run"      ,  1 );
  //fChain->SetBranchStatus("EVENT_lumiBlock"      ,  1 );
  //fChain->SetBranchStatus("EVENT_event"      ,  1 );
  //fChain->SetBranchStatus("subjetAK8_softdrop_csv"      ,  1 );

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  //TFile* trigEffFile = new TFile("inputs/JetTrig.root");
  //TCanvas* trigEffCan = (TCanvas*) trigEffFile->Get("effi");
  //TPad* trigEffPad = (TPad*) trigEffCan->GetPrimitive("pad1");
  //TIter it(trigEffPad->GetListOfPrimitives());
  //TH1D* trigEffHist = new TH1D();
  //while (TObject* obj = it()) {
  //  if (strncmp(obj->IsA()->GetName(), "TH1D", 4)==0) {
  //    if (((TH1D*)obj)->GetLineColor() == 432) {
  //      trigEffHist = (TH1D*)obj;
  //    }
  //  }
  //}
  //trigEffFile->Close();

  TF1* turnOnCurve = new TF1("erf", "[0]*TMath::Erf((x-[1])/[2])+[3]", 0, 5000);
  turnOnCurve->SetParameters(0.493428, 197.58, 62.6643, 0.500232);
  
  cout << "\n\nStarting HgammaSelector::Loop().\n" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    // internal variables used for computation
    eventHasHiggs_softdropJet           = false ;
    leadingPhMVA                     = -999. ;
    leadingPhCat                     = -999. ;
    phoIsTight                       = false ;
    phoEtaPassesCut                  = false ;
    phoPtPassesCut                   = false ;
    eventHasTightPho                 = false ;
    leadingPhE                       = 0.    ;
    softdrop_higgsJetTau1              = -999. ;
    softdrop_higgsJetTau2              = -999. ;
    //softdrop_higgsJetTau3              = -999. ;

    // final output variables
    leadingPhPt                      = 0.    ;
    leadingPhEta                     = -999  ;
    leadingPhPhi                     = -999  ;
    leadingPhAbsEta                  = -999. ;
    higgsJet_abseta           = -999. ;
    higgsJet_eta              = -999. ;
    higgsJet_phi              = -999. ;
    higgsJet_pt               = -999. ;
    higgs_softdropJetCorrMass           = -999. ;
    higgsJet_DDBtag                  = -999. ;
    cosThetaStar                     =  -99. ; 
    phPtOverMgammaj                  =  -99. ; 
    triggerFired_200                 = false ; 
    triggerFired_165HE10             = false ; 
    btagSF                           =  -99. ;
    antibtagSF                       =  -99. ;
    weightFactor                     =  -99. ;

    leadingPhoton        .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector            .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedJet           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedPho           .SetPtEtaPhiE( 0., 0., 0., 0.) ;

    //higgs_csvValues.leading=-10.;
    //higgs_csvValues.subleading=-10.;

    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout.flush();
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events.        " << '\r';
    }
    if (debugFlag && dumpEventInfo) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger && debugFlag) cout << "     Trigger info is: " << endl;
    for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
      if (checkTrigger && debugFlag) { 
        cout << "       " << it->first << " = " << it->second << endl;
      }
      if (it->first.find("HLT_Photon200_") != std::string::npos )  {
        triggerFired_200 = (1==it->second);
        if (triggerFired_200) ++eventsPassingTrigger_200;
      }
      if (  it->first.find("HLT_Photon165_HE10_") != std::string::npos)  {
        triggerFired_165HE10 = (1==it->second);
        if (triggerFired_165HE10) ++eventsPassingTrigger_165HE10;
      }
    }
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut && ph_passEleVeto->at(iPh)==1) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut && ph_passEleVeto->at(iPh)==1);
      //phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoPtPassesCut = ( ph_pt->at(iPh)>180 );
      eventHasTightPho |= (phoIsTight && phoEtaPassesCut && phoPtPassesCut) ;      

      // Fill the leading photon variables, regardless of the ID

      // Fill the leading photon variables, requiring the photon to pass the ID requirements
      if ( ph_pt->at(iPh) > leadingPhPt && phoIsTight && phoEtaPassesCut && phoPtPassesCut) {
        leadingPhPt  = ph_pt     ->  at(iPh) ;
        leadingPhE   = ph_e      ->  at(iPh) ;
        leadingPhEta = ph_eta    ->  at(iPh) ;
        leadingPhPhi = ph_phi    ->  at(iPh) ;
        leadingPhMVA = ph_mvaVal ->  at(iPh) ;
        leadingPhCat = ph_mvaCat ->  at(iPh) ;
        leadingPhoton.SetPtEtaPhiE(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh), ph_e->at(iPh));
      }
   }


    if (debugFlag && eventHasTightPho && dumpEventInfo) cout << "    This event has a tight photon." << endl;

    // Loop over AK8 jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
 
      // TODO TODO fix lepton veto
      //if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_IDTightLepVeto->at(iJet) == 1 && jetAK8_pt->at(iJet)>250) { 
      if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_pt->at(iJet)>250) { 
      // Get leading jet variables, requiring tight jet ID
        tmpLeadingJet.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));

        if (!eventHasHiggs_softdropJet) { 
          eventHasHiggs_softdropJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    softdrop higgs AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    softdrop higgs AK8 jet mass is: " << jetAK8_softdrop_mass->at(iJet) << endl ;
            cout << "    softdrop higgs AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    softdrop higgs AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    softdrop higgs AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          higgsJet_softdrop.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (higgsJet_softdrop.DeltaR(leadingPhoton) < 0.8) {
            higgsJet_softdrop.SetPtEtaPhiE(0,0,0,0);
            eventHasHiggs_softdropJet = false;
          }
          else {
            if  ( iJet<jetAK8_softdrop_massCorr->size() && abs(jetAK8_softdrop_massCorr->at(iJet) - 125) <  abs(higgs_softdropJetCorrMass -  125 )) {
              higgs_softdropJetCorrMass = jetAK8_softdrop_massCorr->at(iJet);
              higgsJet_DDBtag = jetAK8_DDB->at(iJet);
              softdrop_higgsJetTau1 = jetAK8_tau1 ->  at(iJet) ;
              softdrop_higgsJetTau2 = jetAK8_tau2 ->  at(iJet) ;
              //softdrop_higgsJetTau3 = jetAK8_tau3 ->  at(iJet) ;
              //higgs_csvValues = getLeadingSubjets(subjetAK8_softdrop_csv->at(iJet));
              //cout << "    for higgs jet, get csv values " << higgs_csvValues.leading << ", " << higgs_csvValues.subleading << endl;
              //higgs_subjetCutDecisions = getSubjetCutDecisions(higgs_csvValues);
            }
          }
        }
        else if (debugFlag && dumpEventInfo) cout << " this event failed the jet requirement for the higgs branch!" << endl;
      } 
    }

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    // TODO: photon pT cut applied here. unhardcode
    if ( (eventHasTightPho  && leadingPhoton.Pt()>180 && abs(leadingPhoton.Eta()) < 2.6)) {
      if( (eventHasHiggs_softdropJet && higgsJet_softdrop.Pt() > 250 && abs(higgsJet_softdrop.Eta()) < 2.6 )) {
        sumVector = leadingPhoton + higgsJet_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << softdrop_higgsJetTau2/softdrop_higgsJetTau1 << endl;
        }
        higgsJett2t1 = softdrop_higgsJetTau2/softdrop_higgsJetTau1;
        antibtagSF = computeOverallSF("antibtag" , higgsJet_softdrop.Pt(), higgsJet_DDBtag, leadingPhoton.Pt(), leadingPhoton.Eta(), debugSF, btagVariation, phSFvariation);
        btagSF     = computeOverallSF("btag"     , higgsJet_softdrop.Pt(), higgsJet_DDBtag, leadingPhoton.Pt(), leadingPhoton.Eta(), debugSF, btagVariation, phSFvariation);
        //weightFactor = 1/trigEffHist->GetBinContent(trigEffHist->GetXaxis()->FindBin(leadingPhoton.Pt()));
        weightFactor = 1.0/(turnOnCurve->Eval(leadingPhoton.Pt()));
        boostedPho = leadingPhoton;
        boostedPho.Boost(-(sumVector.BoostVector()));
        boostedJet = higgsJet_softdrop;
        boostedJet.Boost(-(sumVector.BoostVector()));
        cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
        phPtOverMgammaj = leadingPhPt/sumVector.M();
        higgsJet_abseta=std::abs(higgsJet_softdrop.Eta());
        higgsJet_eta=higgsJet_softdrop.Eta();
        higgsJet_phi=higgsJet_softdrop.Phi();
        higgsJet_pt=higgsJet_softdrop.Pt();
        leadingPhAbsEta = std::abs(leadingPhEta);
        phJetInvMass_softdrop_higgs=sumVector.M();
        phJetDeltaR_higgs=leadingPhoton.DeltaR(higgsJet_softdrop);
        if ( phJetDeltaR_higgs<0.8 ) {
          if (debugFlag && dumpEventInfo) cout << "this event failed the DR cut!" << endl;
          continue;
        }
        //if (loadEventMap && FindEvent(EVENT_run, EVENT_lumiBlock, EVENT_event)!=0) cout << "found an event that passed selection but did not fire the trigger" << endl;
        outputTreeHiggs->Fill();
        //higgsJet_softdrop.SetT(90);
        //sumVector = leadingPhoton + higgsJet_softdrop;
      }
      else if (debugFlag && dumpEventInfo) {
        cout << " this event failed 'if( (eventHasHiggs_softdropJet && higgsJet_softdrop.Pt() > 250 && abs(higgsJet_softdrop.Eta()) < 2.6 ))'" << endl;
        cout << "eventHasHiggs_softdropJet="  << eventHasHiggs_softdropJet << ", higgsJet_softdrop.Pt()=" << higgsJet_softdrop.Pt() << ", abs(higgsJet_softdrop.Eta())=" << higgsJet_softdrop.Eta() << endl;
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }



  outputFile->Write();
  outputFile->Close();

  cout.flush();
  cout << "100% done: Scanned " << nentries << " events.       " << endl;
  cout << "HLT_Photon200 fired " << eventsPassingTrigger_200 << " times" << endl;
  cout << "The HLT_Photon200 efficiency was " << (float) eventsPassingTrigger_200/ (float)nentries << endl;
  cout << "HLT_Photon165_HE10 fired " << eventsPassingTrigger_165HE10 << " times" << endl;
  cout << "The HLT_Photon165_HE10 efficiency was " << (float) eventsPassingTrigger_165HE10/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}

float HgammaSelector::computeOverallSF(std::string category, float jetPt, float jetDDBtag, float photonPt, float photonEta, bool debug, int variation, int phSFvariation) {
  return computePhotonSF(photonPt, photonEta, debug, phSFvariation)*computeBtagSF(category, jetPt, jetDDBtag, debug, variation);
}

float HgammaSelector::computePhotonSF(float photonPt, float photonEta, bool debug, int phSFvariation) {
  float variedSF = 1.;
  if (phSFvariation != 0 && phSFvariation != 1 && phSFvariation != -1) {
    std::cout << "Error, photon SF variation must be 0 (unvaried), +1 (varied up), or -1 (varied down)" << std::endl;
    exit(EXIT_FAILURE);
  }
  if (photonEta > 0) {
    if (photonEta < 0.8) {
      variedSF = 0.99667 * 0.9938; //The two numbers are the photon SF for MVA, and the photon SF for the CSEV
    }
    else {
      variedSF = 1.01105 * 0.9938;
    }
  }
  else {
    if(photonEta > -0.8) {
      variedSF =  0.992282 * 0.9938;
    }
    else {
      variedSF = 0.995595 * 0.9938;
    }
  }
  if (phSFvariation == 1) {
    variedSF += std::sqrt(0.017*0.017 + 0.0119*0.0119); // the two numbers are the MVA SF uncertainty and the CSEV uncertainty
  }
  else if (phSFvariation == -1) {
    variedSF -= std::sqrt(0.017*0.017 + 0.0119*0.0119);

  }
  return variedSF;
}
float HgammaSelector::computeBtagSF(std::string category, float jetPt, float jetDDBtag, bool debug, int variation) {
  //  variation:
  //  0 = no variation
  //  1 = upward variation
  // -1 = downward variation
  float mistagSF = 0.;
  if (jetPt < 350) { 
    if (variation == 0) {
      mistagSF = 0.85; 
    }
    else if (variation == 1) {
      mistagSF = 0.85 + 0.03; 
    }
    else if (variation == -1) {
      mistagSF = 0.85 - 0.03; 
    }
  }
  else if (jetPt >= 350) {
    if (variation == 0) {
      mistagSF = 0.91; 
    }
    else if (variation == 1) {
      mistagSF = 0.91 + 0.03; 
    }
    else if (variation == -1) {
      mistagSF = 0.91 - 0.04; 
    }
  }
  if (mistagSF == 0.) {
    std::cout << "ERROR -- Something is awry!" << std::endl;
    exit(EXIT_FAILURE);
  }
  float response = -1337.;
  if (category=="antibtag") {
    if (jetDDBtag >= 0.9) {
      if (debug) std::cout << "passes btag! ";
      response =  1.-mistagSF;
    }
    else if (isnan(jetDDBtag) || jetDDBtag < 0.9) {
      if (debug) std::cout << "fails btag! ";
      response =  1.;
    }
  }
  else if (category=="btag") {
    if (jetDDBtag >= 0.9) {
      if (debug) std::cout << "passes btag! ";
      response = mistagSF;
    }
    else if (isnan(jetDDBtag) || jetDDBtag < 0.9) {
      if (debug) std::cout << "fails btag! ";
      response = 0.;
    }
  }
  if (response == -1337.) {
    std::cout << "jetDDBtag is: " << jetDDBtag << std::endl;
    std::cout << "ERROR -- Something went horribly wrong!" << std::endl;
    exit(EXIT_FAILURE);
  }
  if (debug) std::cout << "for " << category << " category SF, response: " << response << std::endl;
  return response;
}


//HgammaSelector::leadingSubjets HgammaSelector::getLeadingSubjets(vector<float> softdropJet) {
//  // Note: in miniaod, there are only two subjets stored since the declustering is done recursively and miniaod's declustering stops after splitting into two subjets
//  leadingSubjets topCSVs;
//  topCSVs.leading = -10.;
//  topCSVs.subleading = -10.;
//  for (uint iSubjet=0; iSubjet<softdropJet.size(); ++iSubjet) {
//    if (softdropJet.at(iSubjet)>topCSVs.leading) {
//      topCSVs.subleading = topCSVs.leading;
//      topCSVs.leading = softdropJet.at(iSubjet);
//    }
//    else if (topCSVs.leading > softdropJet.at(iSubjet) && topCSVs.subleading < softdropJet.at(iSubjet)) {
//      topCSVs.subleading = softdropJet.at(iSubjet);
//    }
//  }
//  return topCSVs;
//}


//HgammaSelector::passSubjetCuts HgammaSelector::getSubjetCutDecisions(leadingSubjets subjets) {
//  float looseWP  = 0.605;
//  float mediumWP = 0.89;
//  float tightWP  = 0.97;
//
//  bool leadingIsLoose     = (subjets.leading    > looseWP);
//  bool leadingIsMedium    = (subjets.leading    > mediumWP);
//  bool leadingIsTight     = (subjets.leading    > tightWP);
//  bool subleadingIsLoose  = (subjets.subleading > looseWP);
//  bool subleadingIsMedium = (subjets.subleading > mediumWP);
//  bool subleadingIsTight  = (subjets.subleading > tightWP);
//
//  passSubjetCuts decisions;
//
//  decisions.loose_loose    = leadingIsLoose   &&  subleadingIsLoose;
//  decisions.medium_loose   = leadingIsMedium  &&  subleadingIsLoose;
//  decisions.tight_loose    = leadingIsTight   &&  subleadingIsLoose;
//  decisions.medium_medium  = leadingIsMedium  &&  subleadingIsMedium;
//  decisions.tight_medium   = leadingIsTight   &&  subleadingIsMedium;
//  decisions.tight_tight    = leadingIsTight   &&  subleadingIsTight;
//
//  return decisions;
//}

//unsigned short HgammaSelector::FindEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event) {
//  std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >::iterator runIt = eventMap->find(run);
//  if (runIt != eventMap->end()) {
//    std::unordered_map<unsigned int, std::vector<unsigned long long> >::iterator lumiIt = eventMap->at(run).find(lumiBlock);
//    if (lumiIt != eventMap->at(run).end()) {
//
//      if (std::find(eventMap->at(run).at(lumiBlock).begin(), eventMap->at(run).at(lumiBlock).end(), event) != eventMap->at(run).at(lumiBlock).end()) {
//        return 0;    // found the event
//      }
//      else return 1; // found the run and lumiblock, but the event wasn't there
//    }
//    else return 2;   // found the run, but lumiblock wasn't there
//  }
//  else return 3;     // didn't find the run
//}
