import FWCore.ParameterSet.Config as cms

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.load('Geometry.CMSCommonData.cmsExtendedGeometryXML_cfi')
#process.load('SimG4CMS.Forward.zdcGeometryXML_cfi')
process.load('Geometry.ForwardCommonData.zdcGeometry_cfi')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.VtxSmearedNoSmear_cff')
process.load('Configuration.StandardSequences.Sim_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger = cms.Service("MessageLogger",
   cerr = cms.untracked.PSet(
     threshold = cms.untracked.string('DEBUG'),
     DEBUG     = cms.untracked.PSet(
       limit = cms.untracked.int32(0)
     ),
     FwkReport = cms.untracked.PSet(
       optionalPSet = cms.untracked.bool(True),
       reportEvery = cms.untracked.int32(500),
       limit = cms.untracked.int32(1000000)
     )
   ),
   destinations = cms.untracked.vstring('cerr'),
)

# Input source
process.source = cms.Source("MCFileSource",
    fileNames = cms.untracked.vstring('file:/eos/cms/store/group/phys_heavyions/osuranyi/ZDC_singleNeutrons/cascade/cascade_pPb_HepMC_150.dat')
#    fileNames = cms.untracked.vstring('file:/eos/cms/store/group/phys_heavyions/osuranyi/ZDC_singleNeutrons/gdrCollective/gdrCollective_pPb_HepMC_1.dat')
    )

# Generator
#process.load('ZdcPhysics.ZdcNeutronGun.ZdcNeutronGun_cfi')
#process.zdcneutrongun.physicsProcess = cms.int32(1)

# Output definition
process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *'),#process.FEVTDEBUGEventContent.outputCommands,
    fileName = cms.untracked.string('simevent.root'),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM'),
        filterName = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Special settings
process.g4SimHits.UseMagneticField = cms.bool(False)
process.g4SimHits.Physics.DefaultCutValue = cms.double(10.)
process.g4SimHits.Generator.HepMCProductLabel = 'LHCTransport'
#process.g4SimHits.Generator.HepMCProductLabel = 'source'
process.g4SimHits.Generator.MinEtaCut = cms.double(-9.0)
process.g4SimHits.Generator.MaxEtaCut =  cms.double(1000.0)
process.g4SimHits.Watchers = cms.VPSet(cms.PSet(
    type = cms.string('ZdcTestAnalysis'),
    ZdcTestAnalysis = cms.PSet(
        Verbosity = cms.int32(0),
		StepNtupleFlag = cms.int32(0),
        EventNtupleFlag = cms.int32(0),
        StepNtupleFileName = cms.string('stepNtuple.root'),
        EventNtupleFileName = cms.string('eventNtuple.root')
	)
))
process.g4SimHits.ZdcSD.UseShowerLibrary = cms.bool(False)
process.g4SimHits.ZdcSD.UseShowerHits = cms.bool(True)
process.RandomNumberGeneratorService.g4SimHits.initialSeed = cms.untracked.uint32(93021885)
#process.g4SimHits.StackingAction.MaxTrackTime = cms.double(100000.)
#process.g4SimHits.CaloSD.TmaxHit = cms.double(100000.)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('/eos/cms/store/group/phys_heavyions/osuranyi/ZDC_output/cascade/file_150.root')
)

process.analyzer = cms.EDAnalyzer('zdcSimAnalyzer'
     ,simhits = cms.InputTag("g4SimHits","ZDCHITS","SIM")
)

# Path and EndPath definitions
process.VtxSmeared.src = "source" #"zdcneutrongun"
process.genParticles.src = "source" #"zdcneutrongun"
process.LHCTransport.HepMCProductLabel = "source" #"zdcneutrongun"

#process.ProductionFilterSequence = cms.Sequence(process.zdcneutrongun)
#process.generator_step = cms.Path(process.zdcneutrongun)
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.endjob_step = cms.Path(process.endOfProcess)
process.out_step = cms.EndPath(process.output)
process.analyzer_step = cms.Path(process.analyzer)

# Schedule definition
process.schedule = cms.Schedule(
    #process.generator_step,
    process.generation_step,
    process.simulation_step,
    #process.out_step,
    #process.endjob_step)
    process.analyzer_step)

'''def customise(process):
    #Adding SimpleMemoryCheck service:
    process.SimpleMemoryCheck=cms.Service("SimpleMemoryCheck",
                                          ignoreTotal=cms.untracked.int32(1),
                                          oncePerEventMode=cms.untracked.bool(True))
    #Adding Timing service:
    process.Timing=cms.Service("Timing")

    #Tweak Message logger to dump G4cout and G4cerr messages in G4msg.log
    #print process.MessageLogger.__dict__
    process.MessageLogger.destinations=cms.untracked.vstring('cout'
                                                             ,'cerr'
                                                             #,'G4msg'
                                                             )
    process.MessageLogger.categories=cms.untracked.vstring('FwkJob'
                                                           ,'FwkReport'
                                                           ,'FwkSummary'
                                                           #,'Root_NoDictionary'
                                                           #,'TimeReport'
                                                           #,'TimeModule'
                                                           #,'TimeEvent'
                                                           #,'MemoryCheck'
                                                           #,'PhysicsList'
                                                           #,'G4cout'
                                                           #,'G4cerr'
                                                           #,'CaloSim'
                                                           #,'ForwardSim'
    )

    process.MessageLogger.debugModules=cms.untracked.vstring('g4SimHits')

    #Configuring the G4msg.log output
    process.MessageLogger.G4msg =  cms.untracked.PSet(
        noTimeStamps = cms.untracked.bool(True)
        #First eliminate unneeded output
        ,threshold = cms.untracked.string('INFO')
        ,INFO = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkReport = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkSummary = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,Root_NoDictionary = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,FwkJob = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeReport = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeModule = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,TimeEvent = cms.untracked.PSet(limit = cms.untracked.int32(0))
        ,MemoryCheck = cms.untracked.PSet(limit = cms.untracked.int32(0))
        #TimeModule, TimeEvent, TimeReport are written to LogAsbolute instead of LogInfo with a category
        #so they cannot be eliminated from any destination (!) unless one uses the summaryOnly option
        #in the Timing Service... at the price of silencing the output needed for the TimingReport profiling
        #
        #Then add the wanted ones:
        ,PhysicsList = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,G4cout = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,G4cerr = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,CaloSim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        ,ForwardSim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
        )

    #Add these 3 lines to put back the summary for timing information at the end of the logfile
    #(needed for TimeReport report)
    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True)
        )

#    process.g4SimHits.G4Commands = cms.vstring('/tracking/verbose 1')

    return(process)

# End of customisation function definition

process = customise(process)'''
