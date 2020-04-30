//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Jan 12 12:03:22 2016 by ROOT version 6.02/05
// from TTree tree/tree
// found on file: flatTuple.root
//////////////////////////////////////////////////////////

#ifndef HgammaSelector_h
#define HgammaSelector_h

#include <math.h>

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>
#include <iomanip>
#include <TH2.h>
#include <TF1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TProfile.h>
#include <TLorentzVector.h>

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "map"
#include "unordered_map"

class HgammaSelector {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

  // Variables calculated using events
  bool  triggerFired_200                 = false ; 
  bool  triggerFired_165HE10             = false ; 
  bool  ignoreAllCuts                    = true  ; 
  bool  requireTrigger                   = false  ; 
  bool  phoIsTight                       = false ; 
  bool  phoEtaPassesCut                  = false ; 
  bool  phoPtPassesCut                   = false ; 
  bool  eventHasTightPho                 = false ; 
  bool  eventHas_softdropJet           = false ; 
  int   eventsPassingTrigger_200         =    0  ;
  int   eventsPassingTrigger_165HE10     =    0  ;
  //int   eventsWithTightPho               =    0  ;
  //int   eventsWithLooseJet               =    0  ;
  //int   eventsWtightPhoAndLooseJet       =    0  ;
  //int   eventsPassingFinalSelection      =    0  ;
  float leadingJetPt                     =    0. ;
  float leadingJetE                      =    0. ;
  float leadingJetEta                    = -999. ;
  float leadingJetPhi                    = -999. ;
  float leadingJetM                      =    0. ;
  float leadingJet_softdropM           =    0. ; 
  float leadingJetSoftdropM              =    0. ;
  //float HT                             =    0. ;
  //float HT_ak4                         =    0. ;
  float leadingJetTau1                   = -999. ;
  float softdropJetCorrMass           = -999. ;
  float bJet_DDBtag                  = -999. ;
  //float test_looseloose                = -1.   ;
  //bool looseloose                = false ;
  float softdrop_bJetTau1         = -999. ;
  float leadingJetTau2              = -999. ;
  float softdrop_bJetTau2       = -999. ;
  float leadingJetTau3              = -999. ;
  //float pruned_bJetTau3         = -999. ;
  float leadingPhPt                 =    0. ;
  float leadingPhEta                =    0. ;
  float leadingPhPhi                =    0. ;
  float leadingPhE                  =    0. ;
  float leadingPhMVA                =    0. ;
  float leadingPhCat                =    0. ;
  float matchedJett2t1              = -999. ;
  float bJett2t1                = -999. ;
  float bJet_abseta      = -999. ;
  float bJet_eta         = -999. ;
  float bJet_phi         = -999. ;
  float bJet_pt          = -999. ;
  float leadingPhAbsEta             = -999. ;
  float cosThetaStar                =  -99. ;
  float phPtOverMgammaj             =  -99. ;
  float phJetInvMass_softdrop   =  -99. ;
  float phJetDeltaR           =  -99. ;
  float antibtagSF                  =  -99. ;
  float btagSF                      =  -99. ;
  float weightFactor                =  -99. ;

  TLorentzVector leadingPhoton              ;
  TLorentzVector tmpLeadingJet              ;
  TLorentzVector bJet_softdrop            ;
  TLorentzVector sumVector                  ;
  TLorentzVector boostedJet                 ;
  TLorentzVector boostedPho                 ;
  
  //structs for b-tagging
   struct leadingSubjets {
     float leading;
     float subleading;
   };
   struct passSubjetCuts {
     bool loose_loose;
     bool medium_loose;
     bool medium_medium;
     bool tight_loose;
     bool tight_medium;
     bool tight_tight;
   }; 
   leadingSubjets csvValues;
   leadingSubjets sideLowFour_csvValues;
   passSubjetCuts subjetCutDecisions;
   passSubjetCuts sideLowFour_subjetCutDecisions;

// Fixed size dimensions of array or collections stored in the TTree if any.
   const Int_t kMaxpassFilter_HBHE = 1;
   const Int_t kMaxpassFilter_HBHEIso = 1;
   const Int_t kMaxpassFilter_CSCTightHalo2015 = 1;
   const Int_t kMaxpassFilter_GoodVtx = 1;
   const Int_t kMaxpassFilter_EEBadSc = 1;
   const Int_t kMaxpassFilter_muonBadTrack = 1;
   //const Int_t kMaxpassFilter_GoodVtx = 1;
   //const Int_t kMaxpassFilter_TrkFailure = 1;
   //const Int_t kMaxpassFilter_EEBadSc = 1;
   //const Int_t kMaxpassFilter_ECALlaser = 1;
   //const Int_t kMaxpassFilter_TrkPOG = 1;
   //const Int_t kMaxpassFilter_TrkPOG_manystrip = 1;
   //const Int_t kMaxpassFilter_TrkPOG_toomanystrip = 1;
   //const Int_t kMaxpassFilter_TrkPOG_logError = 1;
   //const Int_t kMaxpassFilter_METFilters = 1;

   // Declaration of leaf types
   //Int_t           genParticle_N;
   //vector<float>   *genParticle_pt;
   //vector<float>   *genParticle_px;
   //vector<float>   *genParticle_py;
   //vector<float>   *genParticle_pz;
   //vector<float>   *genParticle_e;
   //vector<float>   *genParticle_eta;
   //vector<float>   *genParticle_phi;
   //vector<float>   *genParticle_mass;
   //vector<int>     *genParticle_pdgId;
   //vector<int>     *genParticle_status;
   //vector<vector<int> > *genParticle_mother;
   //vector<int>     *genParticle_nMoth;
   //vector<int>     *genParticle_nDau;
   //vector<vector<int> > *genParticle_dau;
   //Float_t         lheV_pt;
   //Float_t         lheHT;
   //Float_t         lheNj;
   //Float_t         genWeight;
   //Float_t         qScale;
   //vector<float>   *PDF_x;
   //vector<float>   *PDF_xPDF;
   //vector<int>     *PDF_id;
   Int_t           ph_N;
   vector<int>     *ph_pdgId;
   vector<float>   *ph_charge;
   vector<float>   *ph_e;
   vector<float>   *ph_eta;
   vector<float>   *ph_phi;
   vector<float>   *ph_mass;
   vector<float>   *ph_pt;
   vector<float>   *ph_et;
   vector<float>   *ph_rho;
   vector<float>   *ph_superCluster_eta;
   vector<float>   *ph_superCluster_phi;
   vector<float>   *ph_sigmaIetaIeta;
   vector<float>   *ph_hOverE;
   vector<float>   *ph_isoGamma;
   vector<float>   *ph_isoCh;
   vector<int>     *ph_passLooseId;
   vector<int>     *ph_passMediumId;
   vector<int>     *ph_passTightId;
   vector<float>   *ph_mvaVal;
   vector<float>   *ph_mvaCat;
   vector<bool>    *ph_passEleVeto;
   //Int_t           el_N;
   //vector<int>     *el_pdgId;
   //vector<float>   *el_charge;
   //vector<float>   *el_e;
   //vector<float>   *el_eta;
   //vector<float>   *el_phi;
   //vector<float>   *el_mass;
   //vector<float>   *el_pt;
   //vector<float>   *el_et;
   //vector<float>   *el_superCluster_eta;
   //vector<int>     *el_isVetoElectron;
   //vector<int>     *el_isMediumElectron;
   //vector<int>     *el_isTightElectron;
   //vector<int>     *el_isHeepElectron;
   //vector<int>     *el_isHeep51Electron;
   //vector<int>     *el_isLooseElectron;
   //vector<int>     *el_isVetoElectronBoosted;
   //vector<int>     *el_isMediumElectronBoosted;
   //vector<int>     *el_isTightElectronBoosted;
   //vector<int>     *el_isHeepElectronBoosted;
   //vector<int>     *el_isHeep51ElectronBoosted;
   //vector<int>     *el_isLooseElectronBoosted;
   //Int_t           mu_N;
   //vector<int>     *mu_pdgId;
   //vector<float>   *mu_charge;
   //vector<float>   *mu_e;
   //vector<float>   *mu_eta;
   //vector<float>   *mu_phi;
   //vector<float>   *mu_mass;
   //vector<float>   *mu_pt;
   //vector<int>     *mu_isHighPtMuon;
   //vector<int>     *mu_isTightMuon;
   //vector<int>     *mu_isLooseMuon;
   //vector<int>     *mu_isPFMuon;
   //vector<int>     *mu_isSoftMuon;
   Float_t         rho;
   //Int_t           jetAK4_N;
   //vector<float>   *jetAK4_pt;
   //vector<float>   *jetAK4_eta;
   //vector<float>   *jetAK4_mass;
   //vector<float>   *jetAK4_phi;
   //vector<float>   *jetAK4_e;
   //vector<float>   *jetAK4_jec;
   //vector<bool>    *jetAK4_IDLoose;
   //vector<bool>    *jetAK4_IDTight;
   //vector<bool>    *jetAK4_IDTightLepVeto;
   //vector<int>     *jetAK4_charge;
   ////vector<float>   *jetAK4_cisv;
   //vector<float>   *jetAK4_vtxMass;
   //vector<float>   *jetAK4_vtxNtracks;
   //vector<float>   *jetAK4_vtx3DVal;
   //vector<float>   *jetAK4_vtx3DSig;
   ////vector<int>     *jetAK4_partonFlavour;
   ////vector<int>     *jetAK4_hadronFlavour;
   ////vector<int>     *jetAK4_genParton_pdgID;
   ////vector<int>     *jetAK4_nbHadrons;
   ////vector<int>     *jetAK4_ncHadrons;
   Int_t           jetAK8_N;
   vector<float>   *jetAK8_pt;
   vector<float>   *jetAK8_eta;
   vector<float>   *jetAK8_mass;
   vector<float>   *jetAK8_phi;
   vector<float>   *jetAK8_e;
   vector<float>   *jetAK8_jec;
   vector<float>   *jetAK8_jecUp;
   vector<float>   *jetAK8_jecDown;
   vector<bool>    *jetAK8_IDLoose;
   vector<bool>    *jetAK8_IDTight;
   //vector<bool>    *jetAK8_IDTightLepVeto;
   vector<int>     *jetAK8_charge;
   vector<float>   *jetAK8_DDB;
   //vector<int>     *jetAK8_partonFlavour;
   //vector<int>     *jetAK8_hadronFlavour;
   //vector<int>     *jetAK8_genParton_pdgID;
   //vector<int>     *jetAK8_nbHadrons;
   //vector<int>     *jetAK8_ncHadrons;
   vector<float>   *jetAK8_csv;
   vector<float>   *jetAK8_tau1;
   vector<float>   *jetAK8_tau2;
   vector<float>   *jetAK8_tau3;
   vector<float>   *jetAK8_softdrop_mass;
   vector<float>   *jetAK8_softdrop_massCorr;
   vector<float>   *jetAK8_softdrop_jec;
   //vector<int>     *subjetAK8_softdrop_N;
   //vector<vector<float> > *subjetAK8_softdrop_pt;
   //vector<vector<float> > *subjetAK8_softdrop_eta;
   //vector<vector<float> > *subjetAK8_softdrop_mass;
   //vector<vector<float> > *subjetAK8_softdrop_phi;
   //vector<vector<float> > *subjetAK8_softdrop_e;
   //vector<vector<int> > *subjetAK8_softdrop_charge;
   //vector<vector<int> > *subjetAK8_softdrop_partonFlavour;
   //vector<vector<int> > *subjetAK8_softdrop_hadronFlavour;
   //vector<vector<float> > *subjetAK8_pt;
   //vector<vector<float> > *subjetAK8_eta;
   //vector<vector<float> > *subjetAK8_softdrop_mass;
   //vector<vector<float> > *subjetAK8_phi;
   //vector<vector<float> > *subjetAK8_e;
   //vector<vector<int> > *subjetAK8_charge;
   //vector<vector<int> > *subjetAK8_partonFlavour;
   //vector<vector<int> > *subjetAK8_hadronFlavour;
   //vector<vector<float> > *subjetAK8_csv;
   //Int_t           genJetAK4_N;
   //vector<float>   *genJetAK4_pt;
   //vector<float>   *genJetAK4_eta;
   //vector<float>   *genJetAK4_mass;
   //vector<float>   *genJetAK4_phi;
   //vector<float>   *genJetAK4_e;
   //vector<float>   *genJetNoNuAK4_pt;
   //vector<float>   *genJetNoNuAK4_mass;
   //vector<float>   *genJetNoNuAK4_e;
   //Int_t           genJetAK8_N;
   //vector<float>   *genJetAK8_pt;
   //vector<float>   *genJetAK8_eta;
   //vector<float>   *genJetAK8_mass;
   //vector<float>   *genJetAK8_phi;
   //vector<float>   *genJetAK8_e;
   //vector<float>   *genJetAK8_prunedmass;
   //vector<float>   *genJetAK8_softdropmass;
   map<string,bool> *HLT_isFired;
   Bool_t          passFilter_HBHE;
   Bool_t          passFilter_HBHEIso;
   Bool_t          passFilter_CSCTightHalo2015;
   Bool_t          passFilter_GoodVtx;
   Bool_t          passFilter_EEBadSc;
   Bool_t          passFilter_muonBadTrack;
   Int_t           EVENT_event;
   Int_t           EVENT_run;
   Int_t           EVENT_lumiBlock;
   //Bool_t          passFilter_ECALlaser;
   //Bool_t          passFilter_TrkPOG;
   //Bool_t          passFilter_TrkPOG_manystrip;
   //Bool_t          passFilter_TrkPOG_toomanystrip;
   //Bool_t          passFilter_TrkPOG_logError;
   //Bool_t          passFilter_METFilters;
   //vector<float>   *METraw_et;
   //vector<float>   *METraw_phi;
   //vector<float>   *METraw_sumEt;
   //vector<float>   *MET_corrPx;
   //vector<float>   *MET_corrPy;
   //vector<float>   *MET_et;
   //vector<float>   *MET_phi;
   //vector<float>   *MET_sumEt;
   //Int_t           EVENT_event;
   //Int_t           EVENT_run;
   //Int_t           EVENT_lumiBlock;
   //vector<int>     *nPuVtxTrue;
   //vector<int>     *nPuVtx;
   //vector<int>     *bX;
   //Int_t           PV_N;
   //Bool_t          PV_filter;
   //vector<float>   *PV_chi2;
   //vector<float>   *PV_ndof;
   //vector<float>   *PV_rho;
   //vector<float>   *PV_z;

   // List of branches
   //TBranch        *b_genParticle_N;   //!
   //TBranch        *b_genParticle_pt;   //!
   //TBranch        *b_genParticle_px;   //!
   //TBranch        *b_genParticle_py;   //!
   //TBranch        *b_genParticle_pz;   //!
   //TBranch        *b_genParticle_e;   //!
   //TBranch        *b_genParticle_eta;   //!
   //TBranch        *b_genParticle_phi;   //!
   //TBranch        *b_genParticle_mass;   //!
   //TBranch        *b_genParticle_pdgId;   //!
   //TBranch        *b_genParticle_status;   //!
   //TBranch        *b_genParticle_mother;   //!
   //TBranch        *b_genParticle_nMoth;   //!
   //TBranch        *b_genParticle_nDau;   //!
   //TBranch        *b_genParticle_dau;   //!
   //TBranch        *b_lheV_pt;   //!
   //TBranch        *b_lheHT;   //!
   //TBranch        *b_lheNj;   //!
   //TBranch        *b_genWeight;   //!
   //TBranch        *b_qScale;   //!
   //TBranch        *b_PDF_x;   //!
   //TBranch        *b_PDF_xPDF;   //!
   //TBranch        *b_PDF_id;   //!
   TBranch        *b_ph_N;   //!
   TBranch        *b_ph_pdgId;   //!
   TBranch        *b_ph_charge;   //!
   TBranch        *b_ph_e;   //!
   TBranch        *b_ph_eta;   //!
   TBranch        *b_ph_phi;   //!
   TBranch        *b_ph_mass;   //!
   TBranch        *b_ph_pt;   //!
   TBranch        *b_ph_et;   //!
   TBranch        *b_ph_rho;   //!
   TBranch        *b_ph_superCluster_eta;   //!
   TBranch        *b_ph_superCluster_phi;   //!
   TBranch        *b_ph_sigmaIetaIeta;   //!
   TBranch        *b_ph_hOverE;   //!
   TBranch        *b_ph_isoGamma;   //!
   TBranch        *b_ph_isoCh;   //!
   TBranch        *b_ph_passLooseId;   //!
   TBranch        *b_ph_passMediumId;   //!
   TBranch        *b_ph_passTightId;   //!
   TBranch        *b_ph_mvaVal;   //!
   TBranch        *b_ph_mvaCat;   //!
   TBranch        *b_ph_passEleVeto;   //!
   //TBranch        *b_el_N;   //!
   //TBranch        *b_el_pdgId;   //!
   //TBranch        *b_el_charge;   //!
   //TBranch        *b_el_e;   //!
   //TBranch        *b_el_eta;   //!
   //TBranch        *b_el_phi;   //!
   //TBranch        *b_el_mass;   //!
   //TBranch        *b_el_pt;   //!
   //TBranch        *b_el_et;   //!
   //TBranch        *b_el_superCluster_eta;   //!
   //TBranch        *b_el_isVetoElectron;   //!
   //TBranch        *b_el_isMediumElectron;   //!
   //TBranch        *b_el_isTightElectron;   //!
   //TBranch        *b_el_isHeepElectron;   //!
   //TBranch        *b_el_isHeep51Electron;   //!
   //TBranch        *b_el_isLooseElectron;   //!
   //TBranch        *b_el_isVetoElectronBoosted;   //!
   //TBranch        *b_el_isMediumElectronBoosted;   //!
   //TBranch        *b_el_isTightElectronBoosted;   //!
   //TBranch        *b_el_isHeepElectronBoosted;   //!
   //TBranch        *b_el_isHeep51ElectronBoosted;   //!
   //TBranch        *b_el_isLooseElectronBoosted;   //!
   //TBranch        *b_mu_N;   //!
   //TBranch        *b_mu_pdgId;   //!
   //TBranch        *b_mu_charge;   //!
   //TBranch        *b_mu_e;   //!
   //TBranch        *b_mu_eta;   //!
   //TBranch        *b_mu_phi;   //!
   //TBranch        *b_mu_mass;   //!
   //TBranch        *b_mu_pt;   //!
   //TBranch        *b_mu_isHighPtMuon;   //!
   //TBranch        *b_mu_isTightMuon;   //!
   //TBranch        *b_mu_isLooseMuon;   //!
   //TBranch        *b_mu_isPFMuon;   //!
   //TBranch        *b_mu_isSoftMuon;   //!
   TBranch        *b_rho;   //!
   //TBranch        *b_jetAK4_N;   //!
   //TBranch        *b_jetAK4_pt;   //!
   //TBranch        *b_jetAK4_eta;   //!
   //TBranch        *b_jetAK4_mass;   //!
   //TBranch        *b_jetAK4_phi;   //!
   //TBranch        *b_jetAK4_e;   //!
   //TBranch        *b_jetAK4_jec;   //!
   //TBranch        *b_jetAK4_IDLoose;   //!
   //TBranch        *b_jetAK4_IDTight;   //!
   //TBranch        *b_jetAK4_IDTightLepVeto;   //!
   //TBranch        *b_jetAK4_charge;   //!
   ////TBranch        *b_jetAK4_cisv;   //!
   //TBranch        *b_jetAK4_vtxMass;   //!
   //TBranch        *b_jetAK4_vtxNtracks;   //!
   //TBranch        *b_jetAK4_vtx3DVal;   //!
   //TBranch        *b_jetAK4_vtx3DSig;   //!
   //TBranch        *b_jetAK4_partonFlavour;   //!
   //TBranch        *b_jetAK4_hadronFlavour;   //!
   //TBranch        *b_jetAK4_genParton_pdgID;   //!
   //TBranch        *b_jetAK4_nbHadrons;   //!
   //TBranch        *b_jetAK4_ncHadrons;   //!
   TBranch        *b_jetAK8_N;   //!
   TBranch        *b_jetAK8_pt;   //!
   TBranch        *b_jetAK8_eta;   //!
   TBranch        *b_jetAK8_mass;   //!
   TBranch        *b_jetAK8_phi;   //!
   TBranch        *b_jetAK8_e;   //!
   TBranch        *b_jetAK8_jec;   //!
   TBranch        *b_jetAK8_jecUp;   //!
   TBranch        *b_jetAK8_jecDown;   //!
   TBranch        *b_jetAK8_IDLoose;   //!
   TBranch        *b_jetAK8_IDTight;   //!
   //TBranch        *b_jetAK8_IDTightLepVeto;   //!
   TBranch        *b_jetAK8_charge;   //!
   TBranch        *b_jetAK8_DDB;   //!
   //TBranch        *b_jetAK8_partonFlavour;   //!
   //TBranch        *b_jetAK8_hadronFlavour;   //!
   //TBranch        *b_jetAK8_genParton_pdgID;   //!
   //TBranch        *b_jetAK8_nbHadrons;   //!
   //TBranch        *b_jetAK8_ncHadrons;   //!
   TBranch        *b_jetAK8_csv;   //!
   TBranch        *b_jetAK8_tau1;   //!
   TBranch        *b_jetAK8_tau2;   //!
   TBranch        *b_jetAK8_tau3;   //!
   TBranch        *b_jetAK8_softdrop_mass;   //!
   TBranch        *b_jetAK8_softdrop_massCorr;   //!
   TBranch        *b_jetAK8_softdrop_jec;   //!
   //TBranch        *b_subjetAK8_softdrop_N;   //!
   //TBranch        *b_subjetAK8_softdrop_pt;   //!
   //TBranch        *b_subjetAK8_softdrop_eta;   //!
   //TBranch        *b_subjetAK8_softdrop_mass;   //!
   //TBranch        *b_subjetAK8_softdrop_phi;   //!
   //TBranch        *b_subjetAK8_softdrop_e;   //!
   //TBranch        *b_subjetAK8_softdrop_charge;   //!
   //TBranch        *b_subjetAK8_softdrop_partonFlavour;   //!
   //TBranch        *b_subjetAK8_softdrop_hadronFlavour;   //!
   //TBranch        *b_subjetAK8_pruned_N;   //!
   //TBranch        *b_subjetAK8_pruned_pt;   //!
   //TBranch        *b_subjetAK8_pruned_eta;   //!
   //TBranch        *b_subjetAK8_pruned_mass;   //!
   //TBranch        *b_subjetAK8_pruned_phi;   //!
   //TBranch        *b_subjetAK8_pruned_e;   //!
   //TBranch        *b_subjetAK8_pruned_charge;   //!
   //TBranch        *b_subjetAK8_pruned_partonFlavour;   //!
   //TBranch        *b_subjetAK8_pruned_hadronFlavour;   //!
   //TBranch        *b_genJetAK4_N;   //!
   //TBranch        *b_genJetAK4_pt;   //!
   //TBranch        *b_genJetAK4_eta;   //!
   //TBranch        *b_genJetAK4_mass;   //!
   //TBranch        *b_genJetAK4_phi;   //!
   //TBranch        *b_genJetAK4_e;   //!
   //TBranch        *b_genJetNoNuAK4_pt;   //!
   //TBranch        *b_genJetNoNuAK4_mass;   //!
   //TBranch        *b_genJetNoNuAK4_e;   //!
   //TBranch        *b_genJetAK8_N;   //!
   //TBranch        *b_genJetAK8_pt;   //!
   //TBranch        *b_genJetAK8_eta;   //!
   //TBranch        *b_genJetAK8_mass;   //!
   //TBranch        *b_genJetAK8_phi;   //!
   //TBranch        *b_genJetAK8_e;   //!
   //TBranch        *b_genJetAK8_prunedmass;   //!
   //TBranch        *b_genJetAK8_softdropmass;   //!
   //TBranch        *b_subjetAK8_pruned_csv;   //!
   TBranch        *b_HLT_isFired;   //!
   TBranch        *b_passFilter_HBHE_;   //!
   TBranch        *b_passFilter_HBHEIso_;   //!
   TBranch        *b_passFilter_CSCTightHalo2015_;   //!
   TBranch        *b_passFilter_GoodVtx_;   //!
   TBranch        *b_passFilter_EEBadSc_;   //!
   TBranch        *b_passFilter_muonBadTrack_;   //!
   TBranch        *b_EVENT_event;   //!
   TBranch        *b_EVENT_run;   //!
   TBranch        *b_EVENT_lumiBlock;   //!
   //TBranch        *b_passFilter_ECALlaser_;   //!
   //TBranch        *b_passFilter_TrkPOG_;   //!
   //TBranch        *b_passFilter_TrkPOG_manystrip_;   //!
   //TBranch        *b_passFilter_TrkPOG_toomanystrip_;   //!
   //TBranch        *b_passFilter_TrkPOG_logError_;   //!
   //TBranch        *b_passFilter_METFilters_;   //!
   //TBranch        *b_METraw_et;   //!
   //TBranch        *b_METraw_phi;   //!
   //TBranch        *b_METraw_sumEt;   //!
   //TBranch        *b_MET_corrPx;   //!
   //TBranch        *b_MET_corrPy;   //!
   //TBranch        *b_MET_et;   //!
   //TBranch        *b_MET_phi;   //!
   //TBranch        *b_MET_sumEt;   //!
   //TBranch        *b_EVENT_event;   //!
   //TBranch        *b_EVENT_run;   //!
   //TBranch        *b_EVENT_lumiBlock;   //!
   //TBranch        *b_nPuVtxTrue;   //!
   //TBranch        *b_nPuVtx;   //!
   //TBranch        *b_bX;   //!
   //TBranch        *b_PV_N;   //!
   //TBranch        *b_PV_filter;   //!
   //TBranch        *b_PV_chi2;   //!
   //TBranch        *b_PV_ndof;   //!
   //TBranch        *b_PV_rho;   //!
   //TBranch        *b_PV_z;   //!

   //std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >* eventMap;

   HgammaSelector(TTree *tree=0);
   virtual ~HgammaSelector();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(int analysis, string outputFileName, int btagVariation=0, int phSFvariation = 0, float mcWeight=1);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   //virtual unsigned short     FindEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event);

   
   float computeOverallSF(std::string category, float jetPt, float jetDDBtag, float photonPt, float photonEta, bool debug = false, int btagVariation=0, int phSFvariation=0);
   float computePhotonSF(float photonPt, float photonEta, bool debug = false, int phSFvariation = 0);
   float computeBtagSF(std::string category, float jetPt, float jetDDBtag, bool debug = false, int btagVariation=0);

   //leadingSubjets getLeadingSubjets(vector<float> prunedJet);
   //passSubjetCuts getSubjetCutDecisions(leadingSubjets subjets);
};

#endif

#ifdef HgammaSelector_cxx
HgammaSelector::HgammaSelector(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
       exit(EXIT_FAILURE);

   }
   Init(tree);
}

HgammaSelector::~HgammaSelector()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t HgammaSelector::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t HgammaSelector::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void HgammaSelector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   //genParticle_pt = 0;
   //genParticle_px = 0;
   //genParticle_py = 0;
   //genParticle_pz = 0;
   //genParticle_e = 0;
   //genParticle_eta = 0;
   //genParticle_phi = 0;
   //genParticle_mass = 0;
   //genParticle_pdgId = 0;
   //genParticle_status = 0;
   //genParticle_mother = 0;
   //genParticle_nMoth = 0;
   //genParticle_nDau = 0;
   //genParticle_dau = 0;
   //PDF_x = 0;
   //PDF_xPDF = 0;
   //PDF_id = 0;
   ph_pdgId = 0;
   ph_charge = 0;
   ph_e = 0;
   ph_eta = 0;
   ph_phi = 0;
   ph_mass = 0;
   ph_pt = 0;
   ph_et = 0;
   ph_rho = 0;
   ph_superCluster_eta = 0;
   ph_superCluster_phi = 0;
   ph_sigmaIetaIeta = 0;
   ph_hOverE = 0;
   ph_isoGamma = 0;
   ph_isoCh = 0;
   ph_passLooseId = 0;
   ph_passMediumId = 0;
   ph_passTightId = 0;
   ph_mvaVal = 0;
   ph_mvaCat = 0;
   ph_passEleVeto = 0;
   //el_pdgId = 0;
   //el_charge = 0;
   //el_e = 0;
   //el_eta = 0;
   //el_phi = 0;
   //el_mass = 0;
   //el_pt = 0;
   //el_et = 0;
   //el_superCluster_eta = 0;
   //el_isVetoElectron = 0;
   //el_isMediumElectron = 0;
   //el_isTightElectron = 0;
   //el_isHeepElectron = 0;
   //el_isHeep51Electron = 0;
   //el_isLooseElectron = 0;
   //el_isVetoElectronBoosted = 0;
   //el_isMediumElectronBoosted = 0;
   //el_isTightElectronBoosted = 0;
   //el_isHeepElectronBoosted = 0;
   //el_isHeep51ElectronBoosted = 0;
   //el_isLooseElectronBoosted = 0;
   //mu_pdgId = 0;
   //mu_charge = 0;
   //mu_e = 0;
   //mu_eta = 0;
   //mu_phi = 0;
   //mu_mass = 0;
   //mu_pt = 0;
   //mu_isHighPtMuon = 0;
   //mu_isTightMuon = 0;
   //mu_isLooseMuon = 0;
   //mu_isPFMuon = 0;
   //mu_isSoftMuon = 0;
   //jetAK4_pt = 0;
   //jetAK4_eta = 0;
   //jetAK4_mass = 0;
   //jetAK4_phi = 0;
   //jetAK4_e = 0;
   //jetAK4_jec = 0;
   //jetAK4_IDLoose = 0;
   //jetAK4_IDTight = 0;
   //jetAK4_IDTightLepVeto = 0;
   //jetAK4_charge = 0;
   ////jetAK4_cisv = 0;
   //jetAK4_vtxMass = 0;
   //jetAK4_vtxNtracks = 0;
   //jetAK4_vtx3DVal = 0;
   //jetAK4_vtx3DSig = 0;
   ////jetAK4_partonFlavour = 0;
   ////jetAK4_hadronFlavour = 0;
   ////jetAK4_genParton_pdgID = 0;
   ////jetAK4_nbHadrons = 0;
   ////jetAK4_ncHadrons = 0;
   jetAK8_pt = 0;
   jetAK8_eta = 0;
   jetAK8_mass = 0;
   jetAK8_phi = 0;
   jetAK8_e = 0;
   jetAK8_jec = 0;
   jetAK8_jecUp = 0;
   jetAK8_jecDown = 0;
   jetAK8_IDLoose = 0;
   jetAK8_IDTight = 0;
   //jetAK8_IDTightLepVeto = 0;
   jetAK8_charge = 0;
   jetAK8_DDB = 0;
   //jetAK8_partonFlavour = 0;
   //jetAK8_hadronFlavour = 0;
   //jetAK8_genParton_pdgID = 0;
   //jetAK8_nbHadrons = 0;
   //jetAK8_ncHadrons = 0;
   jetAK8_csv = 0;
   jetAK8_tau1 = 0;
   jetAK8_tau2 = 0;
   jetAK8_tau3 = 0;
   jetAK8_pt = 0;
   jetAK8_eta = 0;
   jetAK8_phi = 0;
   jetAK8_e = 0;
   jetAK8_tau1 = 0;
   jetAK8_tau2 = 0;
   jetAK8_softdrop_mass = 0;
   jetAK8_softdrop_massCorr = 0;
   jetAK8_softdrop_mass = 0;
   jetAK8_softdrop_massCorr = 0;
   jetAK8_softdrop_jec = 0;
   HLT_isFired = 0;
   //subjetAK8_softdrop_N = 0;
   //subjetAK8_softdrop_pt = 0;
   //subjetAK8_softdrop_eta = 0;
   //subjetAK8_softdrop_mass = 0;
   //subjetAK8_softdrop_phi = 0;
   //subjetAK8_softdrop_e = 0;
   //subjetAK8_softdrop_charge = 0;
   //subjetAK8_softdrop_partonFlavour = 0;
   //subjetAK8_softdrop_hadronFlavour = 0;
   //subjetAK8_pruned_N = 0;
   //subjetAK8_pruned_pt = 0;
   //subjetAK8_pruned_eta = 0;
   //subjetAK8_pruned_mass = 0;
   //subjetAK8_pruned_phi = 0;
   //subjetAK8_pruned_e = 0;
   //subjetAK8_pruned_charge = 0;
   //subjetAK8_pruned_partonFlavour = 0;
   //subjetAK8_pruned_hadronFlavour = 0;
   //subjetAK8_pruned_csv = 0;
   //genJetAK4_pt = 0;
   //genJetAK4_eta = 0;
   //genJetAK4_mass = 0;
   //genJetAK4_phi = 0;
   //genJetAK4_e = 0;
   //genJetNoNuAK4_pt = 0;
   //genJetNoNuAK4_mass = 0;
   //genJetNoNuAK4_e = 0;
   //genJetAK8_pt = 0;
   //genJetAK8_eta = 0;
   //genJetAK8_mass = 0;
   //genJetAK8_phi = 0;
   //genJetAK8_e = 0;
   //genJetAK8_prunedmass = 0;
   //genJetAK8_softdropmass = 0;
   //METraw_et = 0;
   //METraw_phi = 0;
   //METraw_sumEt = 0;
   //MET_corrPx = 0;
   //MET_corrPy = 0;
   //MET_et = 0;
   //MET_phi = 0;
   //MET_sumEt = 0;
   //nPuVtxTrue = 0;
   //nPuVtx = 0;
   //bX = 0;
   //PV_chi2 = 0;
   //PV_ndof = 0;
   //PV_rho = 0;
   //PV_z = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   //fChain->SetBranchAddress("genParticle_N", &genParticle_N, &b_genParticle_N);
   //fChain->SetBranchAddress("genParticle_pt", &genParticle_pt, &b_genParticle_pt);
   //fChain->SetBranchAddress("genParticle_px", &genParticle_px, &b_genParticle_px);
   //fChain->SetBranchAddress("genParticle_py", &genParticle_py, &b_genParticle_py);
   //fChain->SetBranchAddress("genParticle_pz", &genParticle_pz, &b_genParticle_pz);
   //fChain->SetBranchAddress("genParticle_e", &genParticle_e, &b_genParticle_e);
   //fChain->SetBranchAddress("genParticle_eta", &genParticle_eta, &b_genParticle_eta);
   //fChain->SetBranchAddress("genParticle_phi", &genParticle_phi, &b_genParticle_phi);
   //fChain->SetBranchAddress("genParticle_mass", &genParticle_mass, &b_genParticle_mass);
   //fChain->SetBranchAddress("genParticle_pdgId", &genParticle_pdgId, &b_genParticle_pdgId);
   //fChain->SetBranchAddress("genParticle_status", &genParticle_status, &b_genParticle_status);
   //fChain->SetBranchAddress("genParticle_mother", &genParticle_mother, &b_genParticle_mother);
   //fChain->SetBranchAddress("genParticle_nMoth", &genParticle_nMoth, &b_genParticle_nMoth);
   //fChain->SetBranchAddress("genParticle_nDau", &genParticle_nDau, &b_genParticle_nDau);
   //fChain->SetBranchAddress("genParticle_dau", &genParticle_dau, &b_genParticle_dau);
   //fChain->SetBranchAddress("lheV_pt", &lheV_pt, &b_lheV_pt);
   //fChain->SetBranchAddress("lheHT", &lheHT, &b_lheHT);
   //fChain->SetBranchAddress("lheNj", &lheNj, &b_lheNj);
   //fChain->SetBranchAddress("genWeight", &genWeight, &b_genWeight);
   //fChain->SetBranchAddress("qScale", &qScale, &b_qScale);
   //fChain->SetBranchAddress("PDF_x", &PDF_x, &b_PDF_x);
   //fChain->SetBranchAddress("PDF_xPDF", &PDF_xPDF, &b_PDF_xPDF);
   //fChain->SetBranchAddress("PDF_id", &PDF_id, &b_PDF_id);
   fChain->SetBranchAddress("ph_N", &ph_N, &b_ph_N);
   fChain->SetBranchAddress("ph_pdgId", &ph_pdgId, &b_ph_pdgId);
   fChain->SetBranchAddress("ph_charge", &ph_charge, &b_ph_charge);
   fChain->SetBranchAddress("ph_e", &ph_e, &b_ph_e);
   fChain->SetBranchAddress("ph_eta", &ph_eta, &b_ph_eta);
   fChain->SetBranchAddress("ph_phi", &ph_phi, &b_ph_phi);
   fChain->SetBranchAddress("ph_mass", &ph_mass, &b_ph_mass);
   fChain->SetBranchAddress("ph_pt", &ph_pt, &b_ph_pt);
   fChain->SetBranchAddress("ph_et", &ph_et, &b_ph_et);
   fChain->SetBranchAddress("ph_rho", &ph_rho, &b_ph_rho);
   fChain->SetBranchAddress("ph_superCluster_eta", &ph_superCluster_eta, &b_ph_superCluster_eta);
   fChain->SetBranchAddress("ph_superCluster_phi", &ph_superCluster_phi, &b_ph_superCluster_phi);
   fChain->SetBranchAddress("ph_sigmaIetaIeta", &ph_sigmaIetaIeta, &b_ph_sigmaIetaIeta);
   fChain->SetBranchAddress("ph_hOverE", &ph_hOverE, &b_ph_hOverE);
   fChain->SetBranchAddress("ph_isoGamma", &ph_isoGamma, &b_ph_isoGamma);
   fChain->SetBranchAddress("ph_isoCh", &ph_isoCh, &b_ph_isoCh);
   fChain->SetBranchAddress("ph_passEleVeto", &ph_passEleVeto, &b_ph_passEleVeto);
   fChain->SetBranchAddress("ph_passLooseId", &ph_passLooseId, &b_ph_passLooseId);
   fChain->SetBranchAddress("ph_passMediumId", &ph_passMediumId, &b_ph_passMediumId);
   fChain->SetBranchAddress("ph_passTightId", &ph_passTightId, &b_ph_passTightId);
   fChain->SetBranchAddress("ph_mvaVal", &ph_mvaVal, &b_ph_mvaVal);
   fChain->SetBranchAddress("ph_mvaCat", &ph_mvaCat, &b_ph_mvaCat);
   //fChain->SetBranchAddress("el_N", &el_N, &b_el_N);
   //fChain->SetBranchAddress("el_pdgId", &el_pdgId, &b_el_pdgId);
   //fChain->SetBranchAddress("el_charge", &el_charge, &b_el_charge);
   //fChain->SetBranchAddress("el_e", &el_e, &b_el_e);
   //fChain->SetBranchAddress("el_eta", &el_eta, &b_el_eta);
   //fChain->SetBranchAddress("el_phi", &el_phi, &b_el_phi);
   //fChain->SetBranchAddress("el_mass", &el_mass, &b_el_mass);
   //fChain->SetBranchAddress("el_pt", &el_pt, &b_el_pt);
   //fChain->SetBranchAddress("el_et", &el_et, &b_el_et);
   //fChain->SetBranchAddress("el_superCluster_eta", &el_superCluster_eta, &b_el_superCluster_eta);
   //fChain->SetBranchAddress("el_isVetoElectron", &el_isVetoElectron, &b_el_isVetoElectron);
   //fChain->SetBranchAddress("el_isMediumElectron", &el_isMediumElectron, &b_el_isMediumElectron);
   //fChain->SetBranchAddress("el_isTightElectron", &el_isTightElectron, &b_el_isTightElectron);
   //fChain->SetBranchAddress("el_isHeepElectron", &el_isHeepElectron, &b_el_isHeepElectron);
   //fChain->SetBranchAddress("el_isHeep51Electron", &el_isHeep51Electron, &b_el_isHeep51Electron);
   //fChain->SetBranchAddress("el_isLooseElectron", &el_isLooseElectron, &b_el_isLooseElectron);
   //fChain->SetBranchAddress("el_isVetoElectronBoosted", &el_isVetoElectronBoosted, &b_el_isVetoElectronBoosted);
   //fChain->SetBranchAddress("el_isMediumElectronBoosted", &el_isMediumElectronBoosted, &b_el_isMediumElectronBoosted);
   //fChain->SetBranchAddress("el_isTightElectronBoosted", &el_isTightElectronBoosted, &b_el_isTightElectronBoosted);
   //fChain->SetBranchAddress("el_isHeepElectronBoosted", &el_isHeepElectronBoosted, &b_el_isHeepElectronBoosted);
   //fChain->SetBranchAddress("el_isHeep51ElectronBoosted", &el_isHeep51ElectronBoosted, &b_el_isHeep51ElectronBoosted);
   //fChain->SetBranchAddress("el_isLooseElectronBoosted", &el_isLooseElectronBoosted, &b_el_isLooseElectronBoosted);
   //fChain->SetBranchAddress("mu_N", &mu_N, &b_mu_N);
   //fChain->SetBranchAddress("mu_pdgId", &mu_pdgId, &b_mu_pdgId);
   //fChain->SetBranchAddress("mu_charge", &mu_charge, &b_mu_charge);
   //fChain->SetBranchAddress("mu_e", &mu_e, &b_mu_e);
   //fChain->SetBranchAddress("mu_eta", &mu_eta, &b_mu_eta);
   //fChain->SetBranchAddress("mu_phi", &mu_phi, &b_mu_phi);
   //fChain->SetBranchAddress("mu_mass", &mu_mass, &b_mu_mass);
   //fChain->SetBranchAddress("mu_pt", &mu_pt, &b_mu_pt);
   //fChain->SetBranchAddress("mu_isHighPtMuon", &mu_isHighPtMuon, &b_mu_isHighPtMuon);
   //fChain->SetBranchAddress("mu_isTightMuon", &mu_isTightMuon, &b_mu_isTightMuon);
   //fChain->SetBranchAddress("mu_isLooseMuon", &mu_isLooseMuon, &b_mu_isLooseMuon);
   //fChain->SetBranchAddress("mu_isPFMuon", &mu_isPFMuon, &b_mu_isPFMuon);
   //fChain->SetBranchAddress("mu_isSoftMuon", &mu_isSoftMuon, &b_mu_isSoftMuon);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   //fChain->SetBranchAddress("jetAK4_N", &jetAK4_N, &b_jetAK4_N);
   //fChain->SetBranchAddress("jetAK4_pt", &jetAK4_pt, &b_jetAK4_pt);
   //fChain->SetBranchAddress("jetAK4_eta", &jetAK4_eta, &b_jetAK4_eta);
   //fChain->SetBranchAddress("jetAK4_mass", &jetAK4_mass, &b_jetAK4_mass);
   //fChain->SetBranchAddress("jetAK4_phi", &jetAK4_phi, &b_jetAK4_phi);
   //fChain->SetBranchAddress("jetAK4_e", &jetAK4_e, &b_jetAK4_e);
   //fChain->SetBranchAddress("jetAK4_jec", &jetAK4_jec, &b_jetAK4_jec);
   //fChain->SetBranchAddress("jetAK4_IDLoose", &jetAK4_IDLoose, &b_jetAK4_IDLoose);
   //fChain->SetBranchAddress("jetAK4_IDTight", &jetAK4_IDTight, &b_jetAK4_IDTight);
   //fChain->SetBranchAddress("jetAK4_IDTightLepVeto", &jetAK4_IDTightLepVeto, &b_jetAK4_IDTightLepVeto);
   //fChain->SetBranchAddress("jetAK4_charge", &jetAK4_charge, &b_jetAK4_charge);
   ////fChain->SetBranchAddress("jetAK4_cisv", &jetAK4_cisv, &b_jetAK4_cisv);
   //fChain->SetBranchAddress("jetAK4_vtxMass", &jetAK4_vtxMass, &b_jetAK4_vtxMass);
   //fChain->SetBranchAddress("jetAK4_vtxNtracks", &jetAK4_vtxNtracks, &b_jetAK4_vtxNtracks);
   //fChain->SetBranchAddress("jetAK4_vtx3DVal", &jetAK4_vtx3DVal, &b_jetAK4_vtx3DVal);
   //fChain->SetBranchAddress("jetAK4_vtx3DSig", &jetAK4_vtx3DSig, &b_jetAK4_vtx3DSig);
   ////fChain->SetBranchAddress("jetAK4_partonFlavour", &jetAK4_partonFlavour, &b_jetAK4_partonFlavour);
   ////fChain->SetBranchAddress("jetAK4_hadronFlavour", &jetAK4_hadronFlavour, &b_jetAK4_hadronFlavour);
   ////fChain->SetBranchAddress("jetAK4_genParton_pdgID", &jetAK4_genParton_pdgID, &b_jetAK4_genParton_pdgID);
   ////fChain->SetBranchAddress("jetAK4_nbHadrons", &jetAK4_nbHadrons, &b_jetAK4_nbHadrons);
   ////fChain->SetBranchAddress("jetAK4_ncHadrons", &jetAK4_ncHadrons, &b_jetAK4_ncHadrons);
   fChain->SetBranchAddress("jetAK8_N", &jetAK8_N, &b_jetAK8_N);
   fChain->SetBranchAddress("jetAK8_pt", &jetAK8_pt, &b_jetAK8_pt);
   fChain->SetBranchAddress("jetAK8_eta", &jetAK8_eta, &b_jetAK8_eta);
   fChain->SetBranchAddress("jetAK8_mass", &jetAK8_mass, &b_jetAK8_mass);
   fChain->SetBranchAddress("jetAK8_phi", &jetAK8_phi, &b_jetAK8_phi);
   fChain->SetBranchAddress("jetAK8_e", &jetAK8_e, &b_jetAK8_e);
   fChain->SetBranchAddress("jetAK8_jec", &jetAK8_jec, &b_jetAK8_jec);
   fChain->SetBranchAddress("jetAK8_jecUp", &jetAK8_jecUp, &b_jetAK8_jecUp);
   fChain->SetBranchAddress("jetAK8_jecDown", &jetAK8_jecDown, &b_jetAK8_jecDown);
   fChain->SetBranchAddress("jetAK8_IDLoose", &jetAK8_IDLoose, &b_jetAK8_IDLoose);
   fChain->SetBranchAddress("jetAK8_IDTight", &jetAK8_IDTight, &b_jetAK8_IDTight);
   //fChain->SetBranchAddress("jetAK8_IDTightLepVeto", &jetAK8_IDTightLepVeto, &b_jetAK8_IDTightLepVeto);
   fChain->SetBranchAddress("jetAK8_charge", &jetAK8_charge, &b_jetAK8_charge);
   fChain->SetBranchAddress("jetAK8_DDB", &jetAK8_DDB, &b_jetAK8_DDB);
   //fChain->SetBranchAddress("jetAK8_partonFlavour", &jetAK8_partonFlavour, &b_jetAK8_partonFlavour);
   //fChain->SetBranchAddress("jetAK8_hadronFlavour", &jetAK8_hadronFlavour, &b_jetAK8_hadronFlavour);
   //fChain->SetBranchAddress("jetAK8_genParton_pdgID", &jetAK8_genParton_pdgID, &b_jetAK8_genParton_pdgID);
   //fChain->SetBranchAddress("jetAK8_nbHadrons", &jetAK8_nbHadrons, &b_jetAK8_nbHadrons);
   //fChain->SetBranchAddress("jetAK8_ncHadrons", &jetAK8_ncHadrons, &b_jetAK8_ncHadrons);
   fChain->SetBranchAddress("jetAK8_csv", &jetAK8_csv, &b_jetAK8_csv);
   fChain->SetBranchAddress("jetAK8_tau1", &jetAK8_tau1, &b_jetAK8_tau1);
   fChain->SetBranchAddress("jetAK8_tau2", &jetAK8_tau2, &b_jetAK8_tau2);
   fChain->SetBranchAddress("jetAK8_tau3", &jetAK8_tau3, &b_jetAK8_tau3);
   fChain->SetBranchAddress("jetAK8_pt", &jetAK8_pt, &b_jetAK8_pt);
   fChain->SetBranchAddress("jetAK8_eta", &jetAK8_eta, &b_jetAK8_eta);
   fChain->SetBranchAddress("jetAK8_phi", &jetAK8_phi, &b_jetAK8_phi);
   fChain->SetBranchAddress("jetAK8_e", &jetAK8_e, &b_jetAK8_e);
   fChain->SetBranchAddress("jetAK8_tau1", &jetAK8_tau1, &b_jetAK8_tau1);
   fChain->SetBranchAddress("jetAK8_tau2", &jetAK8_tau2, &b_jetAK8_tau2);
   fChain->SetBranchAddress("jetAK8_softdrop_mass", &jetAK8_softdrop_mass, &b_jetAK8_softdrop_mass);
   fChain->SetBranchAddress("jetAK8_softdrop_massCorr", &jetAK8_softdrop_massCorr, &b_jetAK8_softdrop_massCorr);
   fChain->SetBranchAddress("jetAK8_softdrop_mass", &jetAK8_softdrop_mass, &b_jetAK8_softdrop_mass);
   fChain->SetBranchAddress("jetAK8_softdrop_massCorr", &jetAK8_softdrop_massCorr, &b_jetAK8_softdrop_massCorr);
   fChain->SetBranchAddress("jetAK8_softdrop_jec", &jetAK8_softdrop_jec, &b_jetAK8_softdrop_jec);
   //fChain->SetBranchAddress("subjetAK8_softdrop_N", &subjetAK8_softdrop_N, &b_subjetAK8_softdrop_N);
   //fChain->SetBranchAddress("subjetAK8_softdrop_pt", &subjetAK8_softdrop_pt, &b_subjetAK8_softdrop_pt);
   //fChain->SetBranchAddress("subjetAK8_softdrop_eta", &subjetAK8_softdrop_eta, &b_subjetAK8_softdrop_eta);
   //fChain->SetBranchAddress("subjetAK8_softdrop_mass", &subjetAK8_softdrop_mass, &b_subjetAK8_softdrop_mass);
   //fChain->SetBranchAddress("subjetAK8_softdrop_phi", &subjetAK8_softdrop_phi, &b_subjetAK8_softdrop_phi);
   //fChain->SetBranchAddress("subjetAK8_softdrop_e", &subjetAK8_softdrop_e, &b_subjetAK8_softdrop_e);
   //fChain->SetBranchAddress("subjetAK8_softdrop_charge", &subjetAK8_softdrop_charge, &b_subjetAK8_softdrop_charge);
   //fChain->SetBranchAddress("subjetAK8_softdrop_partonFlavour", &subjetAK8_softdrop_partonFlavour, &b_subjetAK8_softdrop_partonFlavour);
   //fChain->SetBranchAddress("subjetAK8_softdrop_hadronFlavour", &subjetAK8_softdrop_hadronFlavour, &b_subjetAK8_softdrop_hadronFlavour);
   //fChain->SetBranchAddress("subjetAK8_pruned_N", &subjetAK8_pruned_N, &b_subjetAK8_pruned_N);
   //fChain->SetBranchAddress("subjetAK8_pruned_pt", &subjetAK8_pruned_pt, &b_subjetAK8_pruned_pt);
   //fChain->SetBranchAddress("subjetAK8_pruned_eta", &subjetAK8_pruned_eta, &b_subjetAK8_pruned_eta);
   //fChain->SetBranchAddress("subjetAK8_pruned_mass", &subjetAK8_pruned_mass, &b_subjetAK8_pruned_mass);
   //fChain->SetBranchAddress("subjetAK8_pruned_phi", &subjetAK8_pruned_phi, &b_subjetAK8_pruned_phi);
   //fChain->SetBranchAddress("subjetAK8_pruned_e", &subjetAK8_pruned_e, &b_subjetAK8_pruned_e);
   //fChain->SetBranchAddress("subjetAK8_pruned_charge", &subjetAK8_pruned_charge, &b_subjetAK8_pruned_charge);
   //fChain->SetBranchAddress("subjetAK8_pruned_partonFlavour", &subjetAK8_pruned_partonFlavour, &b_subjetAK8_pruned_partonFlavour);
   //fChain->SetBranchAddress("subjetAK8_pruned_hadronFlavour", &subjetAK8_pruned_hadronFlavour, &b_subjetAK8_pruned_hadronFlavour);
   //fChain->SetBranchAddress("subjetAK8_pruned_csv", &subjetAK8_pruned_csv, &b_subjetAK8_pruned_csv);
   //fChain->SetBranchAddress("genJetAK4_N", &genJetAK4_N, &b_genJetAK4_N);
   //fChain->SetBranchAddress("genJetAK4_pt", &genJetAK4_pt, &b_genJetAK4_pt);
   //fChain->SetBranchAddress("genJetAK4_eta", &genJetAK4_eta, &b_genJetAK4_eta);
   //fChain->SetBranchAddress("genJetAK4_mass", &genJetAK4_mass, &b_genJetAK4_mass);
   //fChain->SetBranchAddress("genJetAK4_phi", &genJetAK4_phi, &b_genJetAK4_phi);
   //fChain->SetBranchAddress("genJetAK4_e", &genJetAK4_e, &b_genJetAK4_e);
   //fChain->SetBranchAddress("genJetNoNuAK4_pt", &genJetNoNuAK4_pt, &b_genJetNoNuAK4_pt);
   //fChain->SetBranchAddress("genJetNoNuAK4_mass", &genJetNoNuAK4_mass, &b_genJetNoNuAK4_mass);
   //fChain->SetBranchAddress("genJetNoNuAK4_e", &genJetNoNuAK4_e, &b_genJetNoNuAK4_e);
   //fChain->SetBranchAddress("genJetAK8_N", &genJetAK8_N, &b_genJetAK8_N);
   //fChain->SetBranchAddress("genJetAK8_pt", &genJetAK8_pt, &b_genJetAK8_pt);
   //fChain->SetBranchAddress("genJetAK8_eta", &genJetAK8_eta, &b_genJetAK8_eta);
   //fChain->SetBranchAddress("genJetAK8_mass", &genJetAK8_mass, &b_genJetAK8_mass);
   //fChain->SetBranchAddress("genJetAK8_phi", &genJetAK8_phi, &b_genJetAK8_phi);
   //fChain->SetBranchAddress("genJetAK8_e", &genJetAK8_e, &b_genJetAK8_e);
   //fChain->SetBranchAddress("genJetAK8_prunedmass", &genJetAK8_prunedmass, &b_genJetAK8_prunedmass);
   //fChain->SetBranchAddress("genJetAK8_softdropmass", &genJetAK8_softdropmass, &b_genJetAK8_softdropmass);
   fChain->SetBranchAddress("HLT_isFired", &HLT_isFired, &b_HLT_isFired);
   fChain->SetBranchAddress("passFilter_HBHE", &passFilter_HBHE, &b_passFilter_HBHE_);
   fChain->SetBranchAddress("passFilter_HBHEIso", &passFilter_HBHEIso, &b_passFilter_HBHEIso_);
   fChain->SetBranchAddress("passFilter_CSCTightHalo2015", &passFilter_CSCTightHalo2015, &b_passFilter_CSCTightHalo2015_);
   fChain->SetBranchAddress("passFilter_GoodVtx", &passFilter_GoodVtx, &b_passFilter_GoodVtx_);
   fChain->SetBranchAddress("passFilter_EEBadSc", &passFilter_EEBadSc, &b_passFilter_EEBadSc_);
   fChain->SetBranchAddress("passFilter_muonBadTrack", &passFilter_muonBadTrack, &b_passFilter_muonBadTrack_);
   //fChain->SetBranchAddress("passFilter_ECALlaser", &passFilter_ECALlaser, &b_passFilter_ECALlaser_);
   //fChain->SetBranchAddress("passFilter_TrkPOG", &passFilter_TrkPOG, &b_passFilter_TrkPOG_);
   //fChain->SetBranchAddress("passFilter_TrkPOG_manystrip", &passFilter_TrkPOG_manystrip, &b_passFilter_TrkPOG_manystrip_);
   //fChain->SetBranchAddress("passFilter_TrkPOG_toomanystrip", &passFilter_TrkPOG_toomanystrip, &b_passFilter_TrkPOG_toomanystrip_);
   //fChain->SetBranchAddress("passFilter_TrkPOG_logError", &passFilter_TrkPOG_logError, &b_passFilter_TrkPOG_logError_);
   //fChain->SetBranchAddress("passFilter_METFilters", &passFilter_METFilters, &b_passFilter_METFilters_);
   //fChain->SetBranchAddress("METraw_et", &METraw_et, &b_METraw_et);
   //fChain->SetBranchAddress("METraw_phi", &METraw_phi, &b_METraw_phi);
   //fChain->SetBranchAddress("METraw_sumEt", &METraw_sumEt, &b_METraw_sumEt);
   //fChain->SetBranchAddress("MET_corrPx", &MET_corrPx, &b_MET_corrPx);
   //fChain->SetBranchAddress("MET_corrPy", &MET_corrPy, &b_MET_corrPy);
   //fChain->SetBranchAddress("MET_et", &MET_et, &b_MET_et);
   //fChain->SetBranchAddress("MET_phi", &MET_phi, &b_MET_phi);
   //fChain->SetBranchAddress("MET_sumEt", &MET_sumEt, &b_MET_sumEt);
   fChain->SetBranchAddress("EVENT_event", &EVENT_event, &b_EVENT_event);
   fChain->SetBranchAddress("EVENT_run", &EVENT_run, &b_EVENT_run);
   fChain->SetBranchAddress("EVENT_lumiBlock", &EVENT_lumiBlock, &b_EVENT_lumiBlock);
   //fChain->SetBranchAddress("nPuVtxTrue", &nPuVtxTrue, &b_nPuVtxTrue);
   //fChain->SetBranchAddress("nPuVtx", &nPuVtx, &b_nPuVtx);
   //fChain->SetBranchAddress("bX", &bX, &b_bX);
   //fChain->SetBranchAddress("PV_N", &PV_N, &b_PV_N);
   //fChain->SetBranchAddress("PV_filter", &PV_filter, &b_PV_filter);
   //fChain->SetBranchAddress("PV_chi2", &PV_chi2, &b_PV_chi2);
   //fChain->SetBranchAddress("PV_ndof", &PV_ndof, &b_PV_ndof);
   //fChain->SetBranchAddress("PV_rho", &PV_rho, &b_PV_rho);
   //fChain->SetBranchAddress("PV_z", &PV_z, &b_PV_z);
   Notify();
}

Bool_t HgammaSelector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void HgammaSelector::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t HgammaSelector::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef HgammaSelector_cxx
