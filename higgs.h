//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jul 18 15:14:43 2018 by ROOT version 6.10/08
// from TTree higgs/higgs
// found on file: organize_DDs_btag-nom_phSF-nom/signals/ddTree_sig_m1900.root
//////////////////////////////////////////////////////////

#ifndef higgs_h
#define higgs_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class higgs {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         higgsJett2t1;
   Float_t         higgsJet_HbbTag;
   Float_t         cosThetaStar;
   Float_t         phPtOverMgammaj;
   Float_t         leadingPhEta;
   Float_t         leadingPhPhi;
   Float_t         leadingPhPt;
   Float_t         leadingPhAbsEta;
   Float_t         phJetInvMass_puppi_softdrop_higgs;
   Float_t         phJetDeltaR_higgs;
   Float_t         higgsJet_puppi_abseta;
   Float_t         higgsJet_puppi_eta;
   Float_t         higgsJet_puppi_phi;
   Float_t         higgsJet_puppi_pt;
   Float_t         higgsPuppi_softdropJetCorrMass;
   Bool_t          triggerFired_165HE10;
   Bool_t          triggerFired_175;
   Float_t         antibtagSF;
   Float_t         btagSF;
   Float_t         weightFactor;
   Float_t         mcWeight;

   // List of branches
   TBranch        *b_higgsJett2t1;   //!
   TBranch        *b_higgsJet_HbbTag;   //!
   TBranch        *b_cosThetaStar;   //!
   TBranch        *b_phPtOverMgammaj;   //!
   TBranch        *b_leadingPhEta;   //!
   TBranch        *b_leadingPhPhi;   //!
   TBranch        *b_leadingPhPt;   //!
   TBranch        *b_leadingPhAbsEta;   //!
   TBranch        *b_phJetInvMass_puppi_softdrop_higgs;   //!
   TBranch        *b_phJetDeltaR_higgs;   //!
   TBranch        *b_higgsJet_puppi_abseta;   //!
   TBranch        *b_higgsJet_puppi_eta;   //!
   TBranch        *b_higgsJet_puppi_phi;   //!
   TBranch        *b_higgsJet_puppi_pt;   //!
   TBranch        *b_higgsPuppi_softdropJetCorrMass;   //!
   TBranch        *b_triggerFired_165HE10;   //!
   TBranch        *b_triggerFired_175;   //!
   TBranch        *b_antibtagSF;   //!
   TBranch        *b_btagSF;   //!
   TBranch        *b_weightFactor;   //!
   TBranch        *b_mcWeight;   //!

   higgs(TTree *tree=0);
   virtual ~higgs();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef higgs_cxx
higgs::higgs(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("organize_DDs_btag-nom_phSF-nom/signals/ddTree_sig_m1900.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("organize_DDs_btag-nom_phSF-nom/signals/ddTree_sig_m1900.root");
      }
      f->GetObject("higgs",tree);

   }
   Init(tree);
}

higgs::~higgs()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t higgs::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t higgs::LoadTree(Long64_t entry)
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

void higgs::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("higgsJett2t1", &higgsJett2t1, &b_higgsJett2t1);
   fChain->SetBranchAddress("higgsJet_HbbTag", &higgsJet_HbbTag, &b_higgsJet_HbbTag);
   fChain->SetBranchAddress("cosThetaStar", &cosThetaStar, &b_cosThetaStar);
   fChain->SetBranchAddress("phPtOverMgammaj", &phPtOverMgammaj, &b_phPtOverMgammaj);
   fChain->SetBranchAddress("leadingPhEta", &leadingPhEta, &b_leadingPhEta);
   fChain->SetBranchAddress("leadingPhPhi", &leadingPhPhi, &b_leadingPhPhi);
   fChain->SetBranchAddress("leadingPhPt", &leadingPhPt, &b_leadingPhPt);
   fChain->SetBranchAddress("leadingPhAbsEta", &leadingPhAbsEta, &b_leadingPhAbsEta);
   fChain->SetBranchAddress("phJetInvMass_puppi_softdrop_higgs", &phJetInvMass_puppi_softdrop_higgs, &b_phJetInvMass_puppi_softdrop_higgs);
   fChain->SetBranchAddress("phJetDeltaR_higgs", &phJetDeltaR_higgs, &b_phJetDeltaR_higgs);
   fChain->SetBranchAddress("higgsJet_puppi_abseta", &higgsJet_puppi_abseta, &b_higgsJet_puppi_abseta);
   fChain->SetBranchAddress("higgsJet_puppi_eta", &higgsJet_puppi_eta, &b_higgsJet_puppi_eta);
   fChain->SetBranchAddress("higgsJet_puppi_phi", &higgsJet_puppi_phi, &b_higgsJet_puppi_phi);
   fChain->SetBranchAddress("higgsJet_puppi_pt", &higgsJet_puppi_pt, &b_higgsJet_puppi_pt);
   fChain->SetBranchAddress("higgsPuppi_softdropJetCorrMass", &higgsPuppi_softdropJetCorrMass, &b_higgsPuppi_softdropJetCorrMass);
   fChain->SetBranchAddress("triggerFired_165HE10", &triggerFired_165HE10, &b_triggerFired_165HE10);
   fChain->SetBranchAddress("triggerFired_175", &triggerFired_175, &b_triggerFired_175);
   fChain->SetBranchAddress("antibtagSF", &antibtagSF, &b_antibtagSF);
   fChain->SetBranchAddress("btagSF", &btagSF, &b_btagSF);
   fChain->SetBranchAddress("weightFactor", &weightFactor, &b_weightFactor);
   fChain->SetBranchAddress("mcWeight", &mcWeight, &b_mcWeight);
   Notify();
}

Bool_t higgs::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void higgs::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t higgs::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef higgs_cxx
