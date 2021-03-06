#define HbbGammaSelector_cxx
#include "HbbGammaSelector.h"

using namespace std;

// Class for analyzing the flatTuples from the EXOVVNtuplizer
// The output gives a few trees -- all of which are focused on a V/H(fatjet)gamma resonance
// The trees differ in the AK8 jet mass cuts -- different windows are used for different bosons 
// John Hakala -- May 11, 2016

void HbbGammaSelector::Loop(string outputFileName) {
  cout << "output filename is: " << outputFileName << endl;
  // Flags for running this macro
  bool debugFlag                     =  false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                  =  false ;
  //bool ignoreAllCuts                 =  false ;
  bool dumpEventInfo                 =  false ;
  bool noHLTinfo                     =  true  ;  // This is for the 2016 MC with no HLT info
  int  entriesToCheck                =  100000000 ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                   =  5000  ;

  // Photon id cut values
  float endcap_phoMVAcut             = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  float barrel_phoMVAcut             = 0.374 ;
  float phoEtaMax                    =   2.4 ;
  float jetEtaMax                    =   2.4 ;
  float jetT2T1Max                   =   0.5 ;
  float phoEtaRanges[5]              = {0, 0.75, 1.479, 2.4, 3.0};

  float sidebandThreeCutLow          =   50. ;
  float sidebandThreeCutHigh         =   70. ;
  float sidebandFourCutLow           =  100. ;
  float sidebandFourCutHigh          =  110. ;
  float HmassCutLow                  =  110. ;  // H mass +- 15 GeV
  float HmassCutHigh                 =  140. ;

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");
  outputFile->cd();

  //TTree* outputTreeSig    = new TTree("sig",               "sig");
  TTree* outputTreeHiggs  = new TTree("higgs",           "higgs");
  outputTreeHiggs -> SetAutoSave(-500000000);
  TTree* outputTree5070   = new TTree("side5070",     "side5070");
  TTree* outputTree100110 = new TTree("side100110", "side100110");


  outputTreeHiggs->Branch("higgsJett2t1", &higgsJett2t1);
  outputTreeHiggs->Branch("higgsJet_HbbTag", &higgsJet_HbbTag);
  outputTreeHiggs->Branch("cosThetaStar", &cosThetaStar);
  outputTreeHiggs->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeHiggs->Branch("leadingPhEta", &leadingPhEta);
  outputTreeHiggs->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeHiggs->Branch("leadingPhPt", &leadingPhPt);
  outputTreeHiggs->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeHiggs->Branch("phJetInvMass_puppi_softdrop_higgs", &phJetInvMass_puppi_softdrop_higgs);
  outputTreeHiggs->Branch("phJetDeltaR_higgs", &phJetDeltaR_higgs);
  outputTreeHiggs->Branch("higgsJet_puppi_softdrop_abseta", &higgsJet_puppi_softdrop_abseta);
  outputTreeHiggs->Branch("higgsPuppi_softdropJetCorrMass", &higgsPuppi_softdropJetCorrMass);
  outputTreeHiggs->Branch("triggerFired", &triggerFired);

  outputTree5070->Branch("sideLowThreeJett2t1", &sideLowThreeJett2t1);
  outputTree5070->Branch("cosThetaStar", &cosThetaStar);
  outputTree5070->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTree5070->Branch("leadingPhEta", &leadingPhEta);
  outputTree5070->Branch("leadingPhPhi", &leadingPhPhi);
  outputTree5070->Branch("leadingPhPt", &leadingPhPt);
  outputTree5070->Branch("phJetInvMass_puppi_softdrop_sideLowThree", &phJetInvMass_puppi_softdrop_sideLowThree);
  outputTree5070->Branch("phJetDeltaR_sideLowThree", &phJetDeltaR_sideLowThree);
  outputTree5070->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTree5070->Branch("sideLowThreeJet_puppi_softdrop_abseta", &sideLowThreeJet_puppi_softdrop_abseta);
  outputTree5070->Branch("sideLowThreePuppi_softdropJetCorrMass", &sideLowThreePuppi_softdropJetCorrMass);
  outputTree5070->Branch("sideLowThreeJet_HbbTag", &sideLowThreeJet_HbbTag);

  outputTree100110->Branch("sideLowFourJett2t1", &sideLowFourJett2t1);
  outputTree100110->Branch("cosThetaStar", &cosThetaStar);
  outputTree100110->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTree100110->Branch("leadingPhEta", &leadingPhEta);
  outputTree100110->Branch("leadingPhPhi", &leadingPhPhi);
  outputTree100110->Branch("leadingPhPt", &leadingPhPt);
  outputTree100110->Branch("phJetInvMass_puppi_softdrop_sideLowFour", &phJetInvMass_puppi_softdrop_sideLowFour);
  outputTree100110->Branch("phJetDeltaR_sideLowFour", &phJetDeltaR_sideLowFour);
  outputTree100110->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTree100110->Branch("sideLowFourJet_puppi_softdrop_abseta", &sideLowFourJet_puppi_softdrop_abseta);
  outputTree100110->Branch("sideLowFourPuppi_softdropJetCorrMass", &sideLowFourPuppi_softdropJetCorrMass);
  outputTree100110->Branch("sideLowFourJet_HbbTag", &sideLowFourJet_HbbTag);
  //outputTree100110->Branch("sideLowFour_csvValues", &sideLowFour_csvValues);
  //outputTree100110->Branch("sideLowFour_subjetCutDecisions", &sideLowFour_subjetCutDecisions);

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
  fChain->SetBranchStatus( "jetAK4_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK4_IDLoose"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_mass"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_massCorr"   ,  1 );
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_massCorr" ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_e"                 ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_eta"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_phi"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_tau1"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_tau2"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_tau3"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTight"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTightLepVeto"    ,  1 );  
  fChain->SetBranchStatus( "jetAK8_Hbbtag"            ,  1 );  
  fChain->SetBranchStatus("EVENT_run"      ,  1 );
  fChain->SetBranchStatus("EVENT_lumiBlock"      ,  1 );
  fChain->SetBranchStatus("EVENT_event"      ,  1 );
  //fChain->SetBranchStatus("subjetAK8_puppi_softdrop_csv"      ,  1 );

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  cout << "\n\nStarting HbbGammaSelector::Loop().\n" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    leadingPhPt                      = 0.    ;
    leadingPhEta                     = -999  ;
    leadingPhPhi                     = -999  ;
    leadingPhE                       = 0.    ;
    eventHasHiggsPuppi_softdropJet           = false ;
    eventHasSideLowThreePuppi_softdropJet    = false ;
    eventHasSideLowFourPuppi_softdropJet     = false ;
    eventHasMatchedSoftdropJet       = false ;
    matchedPuppi_softdropJetCorrMass         = -999. ;
    higgsPuppi_softdropJetCorrMass           = -999. ;
    matchedJet_HbbTag                = -999. ;
    higgsJet_HbbTag                  = -999. ;
    puppi_softdrop_higgsJetTau1              = -999. ;
    puppi_softdrop_higgsJetTau2              = -999. ;
    puppi_softdrop_higgsJetTau3              = -999. ;
    phoIsTight                       = false ;
    phoEtaPassesCut                  = false ;
    phoPtPassesCut                   = false ;
    eventHasTightPho                 = false ;
    leadingPhMVA                     = -999. ;
    leadingPhCat                     = -999. ;
    triggerFired                     = false ; 
    //requireTrigger                   = false  ;
    leadingPhAbsEta                  = -999  ;
    cosThetaStar                     =   -99 ; 
    phPtOverMgammaj                  =   -99 ; 
    higgsJet_puppi_softdrop_abseta           = -999  ;
    sideLowThreeJet_puppi_softdrop_abseta    = -999  ;
    sideLowThreeJet_HbbTag           = -999. ;
    phJetInvMass_puppi_softdrop_sideLowThree =  -99  ;
    phJetDeltaR_sideLowThree         =  -99  ;
    sideLowFourJet_puppi_softdrop_abseta     = -999  ;
    sideLowFourJet_HbbTag            = -999. ;
    phJetInvMass_puppi_softdrop_higgs        =  -99  ;
    phJetInvMass_puppi_softdrop_sideLowFour  =  -99  ;
    phJetDeltaR_higgs                =  -99  ;
    phJetDeltaR_sideLowFour          =  -99  ;

    leadingPhoton       .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedJet           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedPho           .SetPtEtaPhiE( 0., 0., 0., 0.) ;

    //higgs_csvValues.leading=-10.;
    //higgs_csvValues.subleading=-10.;
    //sideLowFour_csvValues.leading=-10.;
    //sideLowFour_csvValues.subleading=-10.;

    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout.flush();
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << '\r';
    }
    if (debugFlag) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger && debugFlag) cout << "     Trigger info is: " << endl;
    for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
      if (checkTrigger && debugFlag) { 
        cout << "       " << it->first << " = " << it->second << endl;
      }
      if (it->first.find("HLT_Photon175_") != std::string::npos ||  it->first.find("HLT_Photon165_HE10_") != std::string::npos)  {
        triggerFired |= (1==it->second);
      }
    }
    if (triggerFired) ++eventsPassingTrigger;
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut && ph_passEleVeto->at(iPh)==1) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut && ph_passEleVeto->at(iPh)==1);
      //phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoPtPassesCut = ( ph_pt->at(iPh)>100 );
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
    //cout << " jetAK8_puppi_pt->size() is: " << jetAK8_puppi_pt->size()<< endl;
    for (uint iJet = 0; iJet<jetAK8_puppi_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_puppi_pt->at(iJet) << endl;
 
      if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_IDTightLepVeto->at(iJet) == 1 && jetAK8_puppi_pt->at(iJet)>250) { 
      // Get leading jet variables, requiring tight jet ID
        tmpLeadingJet.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));

        if (!eventHasHiggsPuppi_softdropJet) { 
          eventHasHiggsPuppi_softdropJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    puppi_softdrop higgs AK8 jet e is: "    << jetAK8_puppi_e->at(iJet)    << endl ;
            cout << "    puppi_softdrop higgs AK8 jet mass is: " << jetAK8_puppi_softdrop_mass->at(iJet) << endl ;
            cout << "    puppi_softdrop higgs AK8 jet eta is: "  << jetAK8_puppi_eta->at(iJet)  << endl ;
            cout << "    puppi_softdrop higgs AK8 jet phi is: "  << jetAK8_puppi_phi->at(iJet)  << endl ;
            cout << "    puppi_softdrop higgs AK8 jet pt is: "   << jetAK8_puppi_pt->at(iJet)   << endl ;
          }
          higgsJet_puppi_softdrop.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));
          if (higgsJet_puppi_softdrop.DeltaR(leadingPhoton) < 0.8) {
            higgsJet_puppi_softdrop.SetPtEtaPhiE(0,0,0,0);
            eventHasHiggsPuppi_softdropJet = false;
          }
          else {
            if  ( iJet<jetAK8_puppi_softdrop_massCorr->size() && abs(jetAK8_puppi_softdrop_massCorr->at(iJet) - 125) <  abs(higgsPuppi_softdropJetCorrMass -  125 )) {
              higgsPuppi_softdropJetCorrMass = jetAK8_puppi_softdrop_massCorr->at(iJet);
              higgsJet_HbbTag = jetAK8_Hbbtag->at(iJet);
              puppi_softdrop_higgsJetTau1 = jetAK8_puppi_tau1 ->  at(iJet) ;
              puppi_softdrop_higgsJetTau2 = jetAK8_puppi_tau2 ->  at(iJet) ;
              puppi_softdrop_higgsJetTau3 = jetAK8_puppi_tau3 ->  at(iJet) ;
              //higgs_csvValues = getLeadingSubjets(subjetAK8_puppi_softdrop_csv->at(iJet));
              //cout << "    for higgs jet, get csv values " << higgs_csvValues.leading << ", " << higgs_csvValues.subleading << endl;
              //higgs_subjetCutDecisions = getSubjetCutDecisions(higgs_csvValues);
            }
          }
        }
        else if (debugFlag && dumpEventInfo) cout << " this event failed the jet requirement for the higgs branch!" << endl;
        if (iJet<jetAK8_puppi_softdrop_massCorr->size() && jetAK8_puppi_softdrop_massCorr->at(iJet) >sidebandThreeCutLow  && jetAK8_puppi_softdrop_massCorr->at(iJet) < sidebandThreeCutHigh && !eventHasSideLowThreePuppi_softdropJet) {
          eventHasSideLowThreePuppi_softdropJet = true;
          sideLowThreeJet_puppi_softdrop.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));
          if (sideLowThreeJet_puppi_softdrop.DeltaR(leadingPhoton) < 0.8) {
            sideLowThreeJet_puppi_softdrop.SetPtEtaPhiE(0,0,0,0);
            eventHasSideLowThreePuppi_softdropJet = false;
          }
          else if (iJet<jetAK8_puppi_softdrop_massCorr->size() ) {
            sideLowThreePuppi_softdropJetCorrMass = jetAK8_puppi_softdrop_massCorr->at(iJet);
            sideLowThreeJet_HbbTag = jetAK8_Hbbtag->at(iJet);
            puppi_softdrop_sideLowThreeJetTau1 = jetAK8_puppi_tau1 ->  at(iJet) ;
            puppi_softdrop_sideLowThreeJetTau2 = jetAK8_puppi_tau2 ->  at(iJet) ;
            puppi_softdrop_sideLowThreeJetTau3 = jetAK8_puppi_tau3 ->  at(iJet) ;
          }
        }

        if(debugFlag && dumpEventInfo) {
          cout << "    puppi_softdrop sideLow AK8 jet e is: "    << jetAK8_puppi_e->at(iJet)    << endl ;
          cout << "    puppi_softdrop sideLow AK8 jet mass is: " << jetAK8_puppi_softdrop_mass->at(iJet) << endl ;
          cout << "    puppi_softdrop sideLow AK8 jet eta is: "  << jetAK8_puppi_eta->at(iJet)  << endl ;
          cout << "    puppi_softdrop sideLow AK8 jet phi is: "  << jetAK8_puppi_phi->at(iJet)  << endl ;
          cout << "    puppi_softdrop sideLow AK8 jet pt is: "   << jetAK8_puppi_pt->at(iJet)   << endl ;
        }
        if (iJet<jetAK8_puppi_softdrop_massCorr->size()  && jetAK8_puppi_softdrop_massCorr->at(iJet) >sidebandFourCutLow  && jetAK8_puppi_softdrop_massCorr->at(iJet) < sidebandFourCutHigh && !eventHasSideLowFourPuppi_softdropJet) {
          eventHasSideLowFourPuppi_softdropJet = true;
          sideLowFourJet_puppi_softdrop.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));
          if (sideLowFourJet_puppi_softdrop.DeltaR(leadingPhoton) < 0.8) {
            sideLowFourJet_puppi_softdrop.SetPtEtaPhiE(0,0,0,0);
            eventHasSideLowFourPuppi_softdropJet = false;
          }
          else if (iJet<jetAK8_puppi_softdrop_massCorr->size()){
            sideLowFourPuppi_softdropJetCorrMass = jetAK8_puppi_softdrop_massCorr->at(iJet);
            sideLowFourJet_HbbTag = jetAK8_Hbbtag->at(iJet);
            puppi_softdrop_sideLowFourJetTau1 = jetAK8_puppi_tau1 ->  at(iJet) ;
            puppi_softdrop_sideLowFourJetTau2 = jetAK8_puppi_tau2 ->  at(iJet) ;
            puppi_softdrop_sideLowFourJetTau3 = jetAK8_puppi_tau3 ->  at(iJet) ;
            //sideLowFour_csvValues = getLeadingSubjets(subjetAK8_puppi_softdrop_csv->at(iJet));
            //cout << "    for sideband jet, get csv values " << sideLowFour_csvValues.leading << ", " << sideLowFour_csvValues.subleading << endl;
            //sideLowFour_subjetCutDecisions = getSubjetCutDecisions(sideLowFour_csvValues);
            //cout << "    for sideband jet, get loose_loose = " << sideLowFour_subjetCutDecisions.loose_loose << endl;
          }
        }
      } 
    }

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    // TODO: photon pT cut applied here. unhardcode
    if ( (eventHasTightPho  && leadingPhoton.Pt()>180 && abs(leadingPhoton.Eta()) < 2.6)) {
      if( (eventHasHiggsPuppi_softdropJet && higgsJet_puppi_softdrop.Pt() > 250 && abs(higgsJet_puppi_softdrop.Eta()) < 2.6 )) {
        sumVector = leadingPhoton + higgsJet_puppi_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with puppi_softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << puppi_softdrop_higgsJetTau2/puppi_softdrop_higgsJetTau1 << endl;
        }
        if (noHLTinfo) triggerFired = true;        
        if (triggerFired ) {//|| !requireTrigger || ignoreAllCuts) 
          higgsJett2t1 = puppi_softdrop_higgsJetTau2/puppi_softdrop_higgsJetTau1;
          higgsJett2t1Hist->Fill(higgsJett2t1);
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = higgsJet_puppi_softdrop;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          higgsJet_puppi_softdrop_abseta=std::abs(higgsJet_puppi_softdrop.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_puppi_softdrop_higgs=sumVector.M();
          phJetDeltaR_higgs=leadingPhoton.DeltaR(higgsJet_puppi_softdrop);
          if ( phJetDeltaR_higgs>0.8 ) {
            phJetDeltaPhi_puppi_softdrop->Fill(leadingPhoton.DeltaPhi(higgsJet_puppi_softdrop));
            phJetDeltaEta_puppi_softdrop->Fill(abs( leadingPhoton.Eta() - higgsJet_puppi_softdrop.Eta() ));
            phJetDeltaR_puppi_softdrop->Fill(leadingPhoton.DeltaR(higgsJet_puppi_softdrop));
            leadingPhPtHist->Fill(leadingPhPt);
            leadingPhEtaHist->Fill(leadingPhEta);
            leadingPhPhiHist->Fill(leadingPhPhi);
            phJetInvMassHist_puppi_softdrop_higgs->Fill(phJetInvMass_puppi_softdrop_higgs);
            higgsJetPuppi_softdropMassHist ->Fill(higgsPuppi_softdropJetCorrMass);
            higgsJetPtHist->Fill( higgsJet_puppi_softdrop.Pt());
            higgsJetEtaHist->Fill(higgsJet_puppi_softdrop.Eta());
            higgsJetPhiHist->Fill(higgsJet_puppi_softdrop.Phi());
            phPtOverMgammajHist->Fill(phPtOverMgammaj);
            cosThetaStarHist->Fill(cosThetaStar);
            if (debugFlag && dumpEventInfo) cout << "this event passed!" << endl;

          }
          else if (debugFlag && dumpEventInfo) cout << "this event failed the DR cut!" << endl;
          outputTreeHiggs->Fill();
        }
        else if (debugFlag && dumpEventInfo) cout << "this event failed the trigger cut!" << endl;
        higgsJet_puppi_softdrop.SetT(90);
        sumVector = leadingPhoton + higgsJet_puppi_softdrop;
        if (triggerFired ) phCorrJetInvMassHist_puppi_softdrop_higgs->Fill(sumVector.M());
      }
      else if (debugFlag && dumpEventInfo) {
        cout << " this event failed 'if( (eventHasHiggsPuppi_softdropJet && higgsJet_puppi_softdrop.Pt() > 250 && abs(higgsJet_puppi_softdrop.Eta()) < 2.6 ))'" << endl;
        cout << "eventHasHiggsPuppi_softdropJet="  << eventHasHiggsPuppi_softdropJet << ", higgsJet_puppi_softdrop.Pt()=" << higgsJet_puppi_softdrop.Pt() << ", abs(higgsJet_puppi_softdrop.Eta())=" << higgsJet_puppi_softdrop.Eta() << endl;
      }
      if(eventHasSideLowThreePuppi_softdropJet && sideLowThreeJet_puppi_softdrop.Pt() > 250 && abs(sideLowThreeJet_puppi_softdrop.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + sideLowThreeJet_puppi_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with puppi_softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << puppi_softdrop_sideLowThreeJetTau2/puppi_softdrop_sideLowThreeJetTau1 << endl;
        }
                
        if (triggerFired ){//|| !requireTrigger) 
          sideLowThreeJett2t1 = puppi_softdrop_sideLowThreeJetTau2/puppi_softdrop_sideLowThreeJetTau1;
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = sideLowThreeJet_puppi_softdrop;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          sideLowThreeJet_puppi_softdrop_abseta=std::abs(sideLowThreeJet_puppi_softdrop.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_puppi_softdrop_sideLowThree=sumVector.M();
          phJetDeltaR_sideLowThree=leadingPhoton.DeltaR(sideLowThreeJet_puppi_softdrop);
          outputTree5070->Fill();
        }
          sideLowThreeJet_puppi_softdrop.SetT(90);
          sumVector = leadingPhoton + sideLowThreeJet_puppi_softdrop;
      }
      if( (eventHasSideLowFourPuppi_softdropJet && sideLowFourJet_puppi_softdrop.Pt() > 250 && abs(sideLowFourJet_puppi_softdrop.Eta()) < 2.6 )) {
        sumVector = leadingPhoton + sideLowFourJet_puppi_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with puppi_softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << puppi_softdrop_sideLowFourJetTau2/puppi_softdrop_sideLowFourJetTau1 << endl;
        }
                
        if (triggerFired ){//|| !requireTrigger || ignoreAllCuts) 
          sideLowFourJett2t1 = puppi_softdrop_sideLowFourJetTau2/puppi_softdrop_sideLowFourJetTau1;
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = sideLowFourJet_puppi_softdrop;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          sideLowFourJet_puppi_softdrop_abseta=std::abs(sideLowFourJet_puppi_softdrop.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_puppi_softdrop_sideLowFour=sumVector.M();
          phJetDeltaR_sideLowFour=leadingPhoton.DeltaR(sideLowFourJet_puppi_softdrop);
          outputTree100110->Fill();
        }
          sideLowFourJet_puppi_softdrop.SetT(90);
          sumVector = leadingPhoton + sideLowFourJet_puppi_softdrop;
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }



  outputFile->Write();
  outputFile->Close();

  cout.flush();
  cout << "100% done: Scanned " << nentries << " events." << endl;
  cout << "The trigger fired " << eventsPassingTrigger << " times" << endl;
  cout << "The trigger efficiency was " << (float) eventsPassingTrigger/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}

//HbbGammaSelector::leadingSubjets HbbGammaSelector::getLeadingSubjets(vector<float> puppi_softdropJet) {
//  // Note: in miniaod, there are only two subjets stored since the declustering is done recursively and miniaod's declustering stops after splitting into two subjets
//  leadingSubjets topCSVs;
//  topCSVs.leading = -10.;
//  topCSVs.subleading = -10.;
//  for (uint iSubjet=0; iSubjet<puppi_softdropJet.size(); ++iSubjet) {
//    if (puppi_softdropJet.at(iSubjet)>topCSVs.leading) {
//      topCSVs.subleading = topCSVs.leading;
//      topCSVs.leading = puppi_softdropJet.at(iSubjet);
//    }
//    else if (topCSVs.leading > puppi_softdropJet.at(iSubjet) && topCSVs.subleading < puppi_softdropJet.at(iSubjet)) {
//      topCSVs.subleading = puppi_softdropJet.at(iSubjet);
//    }
//  }
//  return topCSVs;
//}

//HbbGammaSelector::passSubjetCuts HbbGammaSelector::getSubjetCutDecisions(leadingSubjets subjets) {
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
