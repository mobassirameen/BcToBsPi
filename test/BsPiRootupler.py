import FWCore.ParameterSet.Config as cms
process = cms.Process("Rootuple")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data')
#process.GlobalTag = GlobalTag(process.GlobalTag, '94X_dataRun2_ReReco_EOY17_v1', '')

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source("PoolSource",
#process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring(

#'file:/asanchez/data/store/data/Run2016G/Charmonium/MINIAOD/23Sep2016-v1/A4B4AC67-B996-E611-9ECD-008CFAFBE8CE.root',

#MiniAOD
#dataset=/Charmonium/Run2018C-PromptReco-v2/MINIAOD
#'/store/data/Run2018C/Charmonium/MINIAOD/PromptReco-v2/000/319/756/00000/EEF6CEC1-698B-E811-8081-02163E00AF5F.root',
#MC
#'/store/mc/RunIIAutumn18MiniAOD/BcToBsPi_JpsiPhiPi_MuMuKKPi_JpsiPhiFilter_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/110000/4E457795-DA2E-7340-9F04-9FD229FE5465.root'
#dataset=/BcToBsPi_JpsiPhiPi_MuMuKKPi_JpsiPhiFilter_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen/RunIIFall18pLHE-102X_upgrade2018_realistic_v11-v1/LHE
'/store/mc/RunIIFall18pLHE/BcToBsPi_JpsiPhiPi_MuMuKKPi_JpsiPhiFilter_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen/LHE/102X_upgrade2018_realistic_v11-v1/90000/57FBC897-4DE6-184A-9883-40427098651E.root'
        
 )
)

process.triggerSelection = cms.EDFilter("TriggerResultsFilter",
                                        triggerConditions = cms.vstring('HLT_Dimuon20_Jpsi_Barrel_Seagulls_v*',
                                                                        'HLT_Dimuon25_Jpsi_v*',
                                                                        'HLT_DoubleMu4_3_Jpsi_Displaced_v*',
                                                                        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v*',
                                                                        'HLT_DoubleMu4_JpsiTrk_Displaced_v*',
                                                                        'HLT_DoubleMu4_Jpsi_Displaced_v*'                                   
                                                                       ),
                                        hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                                        l1tResults = cms.InputTag( "" ),
                                        throw = cms.bool(False)
                                        )

process.load("myAnalyzers.BsPiPAT.slimmedMuonsTriggerMatcher_cfi")  

process.load("myAnalyzers.BsPiPAT.BsPiRootupler_cfi")
process.rootuple.dimuons = cms.InputTag('slimmedMuonsWithTrigger') 
#process.rootuple.dimuons = cms.InputTag('miniaodPATMuonsWithTrigger')                                                                                

process.TFileService = cms.Service("TFileService",
       #fileName = cms.string('Rootuple_BctoBsPi_2018MC_MiniAOD.root'),                                                                            
       #fileName = cms.string('Rootuple_BsToJPsiphi_2018_MiniAOD.root'),                                                                            
       fileName = cms.string('MCBsToJPsiphi.root'),                                                                            
)


process.mySequence = cms.Sequence(
                                   process.triggerSelection *
    				   process.slimmedMuonsWithTriggerSequence *
                                   process.rootuple
				   )

#process.p = cms.Path(process.mySequence)

process.p = cms.Path(process.triggerSelection*process.slimmedMuonsWithTriggerSequence*process.rootuple)
#process.p = cms.Path(process.rootuple)




