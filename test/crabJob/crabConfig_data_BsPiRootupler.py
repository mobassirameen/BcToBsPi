from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'BcToBsPi_analysis_v1'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../BsPiRootupler.py'
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.inputDataset = '/Charmonium/Run2018C-PromptReco-v2/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 50
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
#config.Data.runRange = '319678-319687'
config.Data.outLFNDirBase = '/store/user/moameen/'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
