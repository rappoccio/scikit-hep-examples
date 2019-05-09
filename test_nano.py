#!/usr/bin/env python
import os, sys
import ROOT
import time
from array import array as arr
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class DetectorResponse(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)
        rbins = arr('f' ,(i * 0.01 for i in range(300)))
        ptbins = arr('f', (10,20,30,40,50,60,80,100,150,200,250,300,350,400,500,600,700,800,900,1000,2000))
        etabins = arr('f', (-1.305, -1.218, -1.131, -1.044, -0.957, -0.879, -0.783, -0.696, -0.609, -0.522, -0.435, -0.348, -0.261, -0.174, -0.087, 0, 0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.879, 0.957, 1.044, 1.131, 1.218, 1.305))
        num_rbins = int(len(rbins)-1)
        num_ptbins = int(len(ptbins)-1)
        num_etabins = int(len(etabins)-1)
      
	self.h_recoJetpT=ROOT.TH1F('recoJet_pT',   'recoJet_pT',   200, 0, 2000)
        self.addObject(self.h_recoJetpT )

        self.h_genJetpT=ROOT.TH1F('genJet_pT',   'genJet_pT',   200, 0, 2000)
        self.addObject(self.h_genJetpT )

        self.h_Response=ROOT.TH1F('Response',   'Response',   300, 0, 3)
        self.addObject(self.h_Response )

        self.h_pT_v_corrFac=ROOT.TH2F('pT_v_corrFac',   'pT_v_corrFac',   num_ptbins, ptbins, num_rbins, rbins)
        self.addObject(self.h_pT_v_corrFac )
        
        self.h_genpT_v_R=ROOT.TH2F('genpT_v_R',   'genpT_v_R',   num_ptbins, ptbins, num_rbins, rbins)
        self.addObject(self.h_genpT_v_R )

        self.h_recoEta_v_R=ROOT.TH2F('recoEta_v_R',   'recoEta_v_R',   num_etabins, etabins, num_rbins, rbins)
        self.addObject(self.h_recoEta_v_R )

    def analyze(self, event):
        genJets = Collection(event, "GenJet")
        corrJets = Collection(event, "Jet")

        v_recoJet = ROOT.TLorentzVector()
        v_genJet = ROOT.TLorentzVector()

        for i in range(len(corrJets)) :       #loop on reco jets
          # cuts on recojet pT and eta
          if ( corrJets[i].p4().Pt() < 20. or  abs(corrJets[i].p4().Eta()) > 1.3): continue
          v_corrJet = corrJets[i].p4()
          corrJet_pT = v_corrJet.Pt()
          recoJet_pT = corrJet_pT*(1.- corrJets[i].rawFactor)
          recoJet_eta = v_corrJet.Eta()
          self.h_pT_v_corrFac.Fill(corrJet_pT,(1.- corrJets[i].rawFactor))

          r_min = 1e8
          index = -1
          for j in range(len(genJets)) :       #loop on gen jets
            v_genJet = genJets[j].p4()
            deltaR = v_genJet.DeltaR(v_corrJet)
            if (deltaR < r_min):
              r_min = deltaR
              index = j
            else:
              continue
          if (r_min < 0.2):
            self.h_recoJetpT.Fill(recoJet_pT)      #fill histograms
            genJet_pT = (genJets[index].p4()).Pt()
            self.h_genJetpT.Fill(genJet_pT)
            R = recoJet_pT/genJet_pT
            self.h_Response.Fill(R)
            self.h_genpT_v_R.Fill(genJet_pT, R)
            self.h_recoEta_v_R.Fill(recoJet_eta, R)
        
        return True


preselection="(Jet_pt>20.) && (abs(Jet_eta) < 1.3)"
#files=["root://cmsxrootd.fnal.gov//store/mc/RunIIFall18NanoAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/NANOAODSIM/NoPU_102X_upgrade2018_realistic_v12-v1/60000/E7149FB3-669D-5E4C-B516-C4C44821C84B.root","root://cmsxrootd.fnal.gov//store/mc/RunIIFall18NanoAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/NANOAODSIM/NoPU_102X_upgrade2018_realistic_v12-v1/270000/8FBF0E5F-EF18-F744-97AA-A9A614C5BF66.root","root://cmsxrootd.fnal.gov//store/mc/RunIIFall18NanoAOD/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/NANOAODSIM/NoPU_102X_upgrade2018_realistic_v12-v1/120000/F9A95EAC-D89A-7446-99F0-7259A2FA507D.root"]
files = ['root://cmsxrootd.fnal.gov://store/mc/RunIIFall17NanoAODv4/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_102X_mc2017_realistic_v6-v1/10000/9D0F80E3-0098-6E49-95D0-DB32523E776B.root']
files = ['9D0F80E3-0098-6E49-95D0-DB32523E776B.root']
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DetectorResponse()],noOut=True,histFileName="histOut.root",histDirName="plots")
start_time = time.clock()
p.run()
cpu_time = time.clock() - start_time
print "CPU time = " + repr(cpu_time) + " seconds"
