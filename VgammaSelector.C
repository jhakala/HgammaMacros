#define VgammaSelector_cxx
#include "VgammaSelector.h"
#include "LinkDef.h"

using namespace std;

// Class for analyzing the flatTuples from the EXOVVNtuplizer
// The output gives a few trees -- all of which are focused on a V/H(fatjet)gamma resonance
// The trees differ in the AK8 jet mass cuts -- different windows are used for different bosons 
// John Hakala -- May 11, 2016

void VgammaSelector::Loop(int analysis, string outputFileName, int btagVariation, int phSFvariation, float mcWeight) {
  if      (analysis == 25) std::cout << "    -> VgammaSelector - Working on Hg analysis" << std::endl;
  else if (analysis == 23) std::cout << "    -> VgammaSelector - working on Zg analysis" << std::endl;
  else                   {
                           std::cout << "Invalid analysis, either 25 for Hgamma or 23 for Zgamma" << std::endl;
                           exit(EXIT_FAILURE);
                         }
                            
  cout << "    -> output filename is: " << outputFileName << endl;
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
  float bosonMass;
  if (analysis == 25)      bosonMass = 125.0;
  else if (analysis == 23) bosonMass = 91.2;
  else                     {std::cout << "illegal bosonMass" << std::endl; exit(EXIT_FAILURE);}
  
  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");
  outputFile->cd();

  //TTree* outputTreeSig    = new TTree("sig",               "sig");
  TTree* outputTreeBoost  = new TTree("ddboost",           "ddboost");
  outputTreeBoost -> SetAutoSave(-500000000);

  outputTreeBoost->Branch("bJett2t1", &bJett2t1);
  outputTreeBoost->Branch("bJet_DDBtag", &bJet_DDBtag);
  outputTreeBoost->Branch("bJet_decDDBtag", &bJet_decDDBtag);
  outputTreeBoost->Branch("bJet_csvbb", &bJet_csvbb);

outputTreeBoost->Branch("bJet_akx_probHbb",  &bJet_akx_probHbb);
outputTreeBoost->Branch("bJet_akx_HbbvsQCD",  &bJet_akx_HbbvsQCD);
outputTreeBoost->Branch("bJet_akx_H4qvsQCD",  &bJet_akx_H4qvsQCD);
outputTreeBoost->Branch("bJet_akx_probZbb",  &bJet_akx_probZbb);
outputTreeBoost->Branch("bJet_akx_probZqq",  &bJet_akx_probZqq);
outputTreeBoost->Branch("bJet_akx_probZcc",  &bJet_akx_probZcc);
outputTreeBoost->Branch("bJet_akx_ZvsQCD",  &bJet_akx_ZvsQCD);
outputTreeBoost->Branch("bJet_akx_ZbbvsQCD",  &bJet_akx_ZbbvsQCD);
outputTreeBoost->Branch("bJet_akx_probWcq",  &bJet_akx_probWcq);
outputTreeBoost->Branch("bJet_akx_probWqq",  &bJet_akx_probWqq);
outputTreeBoost->Branch("bJet_akx_WvsQCD",  &bJet_akx_WvsQCD);

outputTreeBoost->Branch("bJet_akxDec_H4qvsQCD",   &bJet_akxDec_H4qvsQCD  );
outputTreeBoost->Branch("bJet_akxDec_HbbvsQCD",   &bJet_akxDec_HbbvsQCD  );
outputTreeBoost->Branch("bJet_akxDec_WvsQCD",     &bJet_akxDec_WvsQCD    );
outputTreeBoost->Branch("bJet_akxDec_ZHbbvsQCD",  &bJet_akxDec_ZHbbvsQCD );
outputTreeBoost->Branch("bJet_akxDec_ZHccvsQCD",  &bJet_akxDec_ZHccvsQCD );
outputTreeBoost->Branch("bJet_akxDec_ZbbvsQCD",   &bJet_akxDec_ZbbvsQCD  );
outputTreeBoost->Branch("bJet_akxDec_ZvsQCD",     &bJet_akxDec_ZvsQCD    );
outputTreeBoost->Branch("bJet_akxDec_bbvsLight",  &bJet_akxDec_bbvsLight );
outputTreeBoost->Branch("bJet_akxDec_probHbb",    &bJet_akxDec_probHbb   );
outputTreeBoost->Branch("bJet_akxDec_probHcc",    &bJet_akxDec_probHcc   );
outputTreeBoost->Branch("bJet_akxDec_probHqqqq",  &bJet_akxDec_probHqqqq );
outputTreeBoost->Branch("bJet_akxDec_probWcq",    &bJet_akxDec_probWcq   );
outputTreeBoost->Branch("bJet_akxDec_probWqq",    &bJet_akxDec_probWqq   );
outputTreeBoost->Branch("bJet_akxDec_probZbb",    &bJet_akxDec_probZbb   );
outputTreeBoost->Branch("bJet_akxDec_probZcc",    &bJet_akxDec_probZcc   );
outputTreeBoost->Branch("bJet_akxDec_probZqq",    &bJet_akxDec_probZqq   );




  outputTreeBoost->Branch("cosThetaStar", &cosThetaStar);
  outputTreeBoost->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeBoost->Branch("leadingPhEta", &leadingPhEta);
  outputTreeBoost->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeBoost->Branch("leadingPhPt", &leadingPhPt);
  outputTreeBoost->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeBoost->Branch("phJetInvMass_softdrop", &phJetInvMass_softdrop);
  outputTreeBoost->Branch("phJetDeltaR", &phJetDeltaR);
  outputTreeBoost->Branch("bJet_abseta", &bJet_abseta);
  outputTreeBoost->Branch("bJet_eta", &bJet_eta);
  outputTreeBoost->Branch("bJet_phi", &bJet_phi);
  outputTreeBoost->Branch("bJet_pt", &bJet_pt);
  outputTreeBoost->Branch("softdropJetCorrMass", &softdropJetCorrMass);
  outputTreeBoost->Branch("triggerFired_165HE10", &triggerFired_165HE10);
  outputTreeBoost->Branch("triggerFired_200", &triggerFired_200);
  outputTreeBoost->Branch("antibtagSF", &antibtagSF);
  outputTreeBoost->Branch("btagSF", &btagSF);
  outputTreeBoost->Branch("weightFactor", &weightFactor);
  outputTreeBoost->Branch("mcWeight", &mcWeight);


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
  fChain->SetBranchStatus( "jetAK8_decDDB"            ,  1 );  
  fChain->SetBranchStatus( "jetAK8_deep_csv_bb"            ,  1 );  

  fChain->SetBranchStatus( "jetAK8_akx_probHbb"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_HbbvsQCD"             ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_H4qvsQCD"             ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_probZbb"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_probZqq"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_probZcc"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_ZvsQCD"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_ZbbvsQCD"             ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_probWcq"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_probWqq"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_akx_WvsQCD"               ,  1 );  

  fChain->SetBranchStatus( "jetAK8_akxDec_H4qvsQCD",         1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_HbbvsQCD",         1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_WvsQCD",           1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_ZHbbvsQCD",        1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_ZHccvsQCD",        1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_ZbbvsQCD",         1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_ZvsQCD",           1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_bbvsLight",        1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probHbb",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probHcc",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probHqqqq",        1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probWcq",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probWqq",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probZbb",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probZcc",          1 );
  fChain->SetBranchStatus( "jetAK8_akxDec_probZqq",          1 );


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
  
  cout << "    -> starting VgammaSelector::Loop()" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    // internal variables used for computation
    eventHasBoost_softdropJet           = false ;
    leadingPhMVA                     = -999. ;
    leadingPhCat                     = -999. ;
    phoIsTight                       = false ;
    phoEtaPassesCut                  = false ;
    phoPtPassesCut                   = false ;
    eventHasTightPho                 = false ;
    leadingPhE                       = 0.    ;
    softdrop_bJetTau1              = -999. ;
    softdrop_bJetTau2              = -999. ;
    //softdrop_bJetTau3              = -999. ;

    // final output variables
    leadingPhPt                      = 0.    ;
    leadingPhEta                     = -999  ;
    leadingPhPhi                     = -999  ;
    leadingPhAbsEta                  = -999. ;
    bJet_abseta           = -999. ;
    bJet_eta              = -999. ;
    bJet_phi              = -999. ;
    bJet_pt               = -999. ;
    softdropJetCorrMass           = -999. ;
    bJet_DDBtag                  = -999. ;
    bJet_decDDBtag                  = -999. ;
    bJet_csvbb                  = -999. ;

    bJet_akx_probHbb                     = -999. ;
    bJet_akx_HbbvsQCD                    = -999. ;
    bJet_akx_H4qvsQCD                    = -999. ;
    bJet_akx_probZbb                     = -999. ;
    bJet_akx_probZqq                     = -999. ;
    bJet_akx_probZcc                     = -999. ;
    bJet_akx_ZvsQCD                      = -999. ;
    bJet_akx_ZbbvsQCD                    = -999. ;
    bJet_akx_probWcq                     = -999. ;
    bJet_akx_probWqq                     = -999. ;
    bJet_akx_WvsQCD                      = -999. ;

    bJet_akxDec_H4qvsQCD                 = -999. ;
    bJet_akxDec_HbbvsQCD                 = -999. ;
    bJet_akxDec_WvsQCD                   = -999. ;
    bJet_akxDec_ZHbbvsQCD                = -999. ;
    bJet_akxDec_ZHccvsQCD                = -999. ;
    bJet_akxDec_ZbbvsQCD                 = -999. ;
    bJet_akxDec_ZvsQCD                   = -999. ;
    bJet_akxDec_bbvsLight                = -999. ;
    bJet_akxDec_probHbb                  = -999. ;
    bJet_akxDec_probHcc                  = -999. ;
    bJet_akxDec_probHqqqq                = -999. ;
    bJet_akxDec_probWcq                  = -999. ;
    bJet_akxDec_probWqq                  = -999. ;
    bJet_akxDec_probZbb                  = -999. ;
    bJet_akxDec_probZcc                  = -999. ;
    bJet_akxDec_probZqq                  = -999. ;

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

    //csvValues.leading=-10.;
    //csvValues.subleading=-10.;

    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout.flush();
      cout << "    -> " << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events.        " << '\r';
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

        if (!eventHasBoost_softdropJet) { 
          eventHasBoost_softdropJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    softdrop AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    softdrop AK8 jet mass is: " << jetAK8_softdrop_mass->at(iJet) << endl ;
            cout << "    softdrop AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    softdrop AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    softdrop AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          bJet_softdrop.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (bJet_softdrop.DeltaR(leadingPhoton) < 0.8) {
            bJet_softdrop.SetPtEtaPhiE(0,0,0,0);
            eventHasBoost_softdropJet = false;
          }
          else {
            if  ( iJet<jetAK8_softdrop_massCorr->size() && abs(jetAK8_softdrop_massCorr->at(iJet) - bosonMass) <  abs(softdropJetCorrMass -  bosonMass )) {
              softdropJetCorrMass = jetAK8_softdrop_massCorr->at(iJet);
              bJet_DDBtag = jetAK8_DDB->at(iJet);
              bJet_decDDBtag = jetAK8_decDDB->at(iJet);
              bJet_csvbb = jetAK8_deep_csv_bb->at(iJet);

              bJet_akx_probHbb  = jetAK8_akx_probHbb  ->at(iJet);
              bJet_akx_HbbvsQCD = jetAK8_akx_HbbvsQCD ->at(iJet);
              bJet_akx_H4qvsQCD = jetAK8_akx_H4qvsQCD ->at(iJet);
              bJet_akx_probZbb  = jetAK8_akx_probZbb  ->at(iJet);
              bJet_akx_probZqq  = jetAK8_akx_probZqq  ->at(iJet);
              bJet_akx_probZcc  = jetAK8_akx_probZcc  ->at(iJet);
              bJet_akx_ZvsQCD   = jetAK8_akx_ZvsQCD   ->at(iJet);
              bJet_akx_ZbbvsQCD = jetAK8_akx_ZbbvsQCD ->at(iJet);
              bJet_akx_probWcq  = jetAK8_akx_probWcq  ->at(iJet);
              bJet_akx_probWqq  = jetAK8_akx_probWqq  ->at(iJet);
              bJet_akx_WvsQCD   = jetAK8_akx_WvsQCD   ->at(iJet);

              bJet_akxDec_H4qvsQCD   = jetAK8_akxDec_H4qvsQCD   ->at(iJet);  
              bJet_akxDec_HbbvsQCD   = jetAK8_akxDec_HbbvsQCD   ->at(iJet);  
              bJet_akxDec_WvsQCD     = jetAK8_akxDec_WvsQCD     ->at(iJet);  
              bJet_akxDec_ZHbbvsQCD  = jetAK8_akxDec_ZHbbvsQCD  ->at(iJet);  
              bJet_akxDec_ZHccvsQCD  = jetAK8_akxDec_ZHccvsQCD  ->at(iJet);  
              bJet_akxDec_ZbbvsQCD   = jetAK8_akxDec_ZbbvsQCD   ->at(iJet);  
              bJet_akxDec_ZvsQCD     = jetAK8_akxDec_ZvsQCD     ->at(iJet);  
              bJet_akxDec_bbvsLight  = jetAK8_akxDec_bbvsLight  ->at(iJet);  
              bJet_akxDec_probHbb    = jetAK8_akxDec_probHbb    ->at(iJet);  
              bJet_akxDec_probHcc    = jetAK8_akxDec_probHcc    ->at(iJet);  
              bJet_akxDec_probHqqqq  = jetAK8_akxDec_probHqqqq  ->at(iJet);  
              bJet_akxDec_probWcq    = jetAK8_akxDec_probWcq    ->at(iJet);  
              bJet_akxDec_probWqq    = jetAK8_akxDec_probWqq    ->at(iJet);  
              bJet_akxDec_probZbb    = jetAK8_akxDec_probZbb    ->at(iJet);  
              bJet_akxDec_probZcc    = jetAK8_akxDec_probZcc    ->at(iJet);  
              bJet_akxDec_probZqq    = jetAK8_akxDec_probZqq    ->at(iJet);  


              softdrop_bJetTau1 = jetAK8_tau1 ->  at(iJet) ;
              softdrop_bJetTau2 = jetAK8_tau2 ->  at(iJet) ;
              //softdrop_bJetTau3 = jetAK8_tau3 ->  at(iJet) ;
              //csvValues = getLeadingSubjets(subjetAK8_softdrop_csv->at(iJet));
              //cout << "    for jet, get csv values " << csvValues.leading << ", " << csvValues.subleading << endl;
              //subjetCutDecisions = getSubjetCutDecisions(csvValues);
            }
          }
        }
        else if (debugFlag && dumpEventInfo) cout << " this event failed the jet requirement!" << endl;
      } 
    }

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    // TODO: photon pT cut applied here. unhardcode
    if ( (eventHasTightPho  && leadingPhoton.Pt()>180 && abs(leadingPhoton.Eta()) < 2.6)) {
      if( (eventHasBoost_softdropJet && bJet_softdrop.Pt() > 250 && abs(bJet_softdrop.Eta()) < 2.6 )) {
        sumVector = leadingPhoton + bJet_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << softdrop_bJetTau2/softdrop_bJetTau1 << endl;
        }
        bJett2t1 = softdrop_bJetTau2/softdrop_bJetTau1;
        antibtagSF = computeOverallSF("antibtag" , bJet_softdrop.Pt(), bJet_DDBtag, leadingPhoton.Pt(), leadingPhoton.Eta(), debugSF, btagVariation, phSFvariation);
        btagSF     = computeOverallSF("btag"     , bJet_softdrop.Pt(), bJet_DDBtag, leadingPhoton.Pt(), leadingPhoton.Eta(), debugSF, btagVariation, phSFvariation);
        //weightFactor = 1/trigEffHist->GetBinContent(trigEffHist->GetXaxis()->FindBin(leadingPhoton.Pt()));
        weightFactor = 1.0/(turnOnCurve->Eval(leadingPhoton.Pt()));
        boostedPho = leadingPhoton;
        boostedPho.Boost(-(sumVector.BoostVector()));
        boostedJet = bJet_softdrop;
        boostedJet.Boost(-(sumVector.BoostVector()));
        cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
        phPtOverMgammaj = leadingPhPt/sumVector.M();
        bJet_abseta=std::abs(bJet_softdrop.Eta());
        bJet_eta=bJet_softdrop.Eta();
        bJet_phi=bJet_softdrop.Phi();
        bJet_pt=bJet_softdrop.Pt();
        leadingPhAbsEta = std::abs(leadingPhEta);
        phJetInvMass_softdrop=sumVector.M();
        phJetDeltaR=leadingPhoton.DeltaR(bJet_softdrop);
        if ( phJetDeltaR<0.8 ) {
          if (debugFlag && dumpEventInfo) cout << "this event failed the DR cut!" << endl;
          continue;
        }
        //if (loadEventMap && FindEvent(EVENT_run, EVENT_lumiBlock, EVENT_event)!=0) cout << "found an event that passed selection but did not fire the trigger" << endl;
        outputTreeBoost->Fill();
        //bJet_softdrop.SetT(90);
        //sumVector = leadingPhoton + bJet_softdrop;
      }
      else if (debugFlag && dumpEventInfo) {
        cout << " this event failed 'if( (eventHasBoost_softdropJet && bJet_softdrop.Pt() > 250 && abs(bJet_softdrop.Eta()) < 2.6 ))'" << endl;
        cout << "eventHasBoost_softdropJet="  << eventHasBoost_softdropJet << ", bJet_softdrop.Pt()=" << bJet_softdrop.Pt() << ", abs(bJet_softdrop.Eta())=" << bJet_softdrop.Eta() << endl;
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }



  outputFile->Write();
  outputFile->Close();

  cout.flush();
  cout << "    -> 100% done: Scanned " << nentries << " events.       " << endl;
  cout << "      ->HLT_Photon200 fired " << eventsPassingTrigger_200 << " times";
  cout << "(efficiency " << (float) eventsPassingTrigger_200/ (float)nentries << ")" << endl;
  cout << "    -> Completed output file is " << outputFileName.c_str() <<"." << endl;
}

float VgammaSelector::computeOverallSF(std::string category, float jetPt, float jettag, float photonPt, float photonEta, bool debug, int variation, int phSFvariation) {
  return computePhotonSF(photonPt, photonEta, debug, phSFvariation)*computeBtagSF(category, jetPt, jettag, debug, variation);
}

float VgammaSelector::computePhotonSF(float photonPt, float photonEta, bool debug, int phSFvariation) {
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
float VgammaSelector::computeBtagSF(std::string category, float jetPt, float jettag, bool debug, int variation) {
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
    if (jettag >= 0.9) {
      if (debug) std::cout << "passes btag! ";
      response =  1.-mistagSF;
    }
    else if (isnan(jettag) || jettag < 0.9) {
      if (debug) std::cout << "fails btag! ";
      response =  1.;
    }
  }
  else if (category=="btag") {
    if (jettag >= 0.9) {
      if (debug) std::cout << "passes btag! ";
      response = mistagSF;
    }
    else if (isnan(jettag) || jettag < 0.9) {
      if (debug) std::cout << "fails btag! ";
      response = 0.;
    }
  }
  if (response == -1337.) {
    std::cout << "jettag is: " << jettag << std::endl;
    std::cout << "ERROR -- Something went horribly wrong!" << std::endl;
    exit(EXIT_FAILURE);
  }
  if (debug) std::cout << "for " << category << " category SF, response: " << response << std::endl;
  return response;
}


//VgammaSelector::leadingSubjets VgammaSelector::getLeadingSubjets(vector<float> softdropJet) {
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


//VgammaSelector::passSubjetCuts VgammaSelector::getSubjetCutDecisions(leadingSubjets subjets) {
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

//unsigned short VgammaSelector::FindEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event) {
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
