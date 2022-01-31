import ROOT, os

f_name = 'simulate_dummy.py'

inf = open(f_name, 'r')
lines = inf.readlines()
inf.close()

njobs = 500

outpath = '/eos/cms/store/group/phys_heavyions/osuranyi/ZDC_output/onlyCA/'
os.system('rm -rf '+outpath)
os.system('mkdir -p '+outpath)

allfiles = []

logdir = 'submission_onlyCA'
os.system('rm -rf '+logdir)
os.system('mkdir -p '+logdir)

for i in range(1,njobs+1):

    f_new = logdir+'/'+f_name.replace('dummy',str(i))

    f_new_open = open(f_new, 'w')

    tmp_out = outpath+'file_{i}.root'.format(i=i)

    for line in lines:
        writeline = line.replace('FILENAME','file:/eos/cms/store/group/phys_heavyions/osuranyi/ZDC_singleNeutrons/onlyCA/onlyCA_pPb_HepMC_{i}.dat'.format(i=i))
        writeline = writeline.replace('OUTPUT',str(tmp_out))

        f_new_open.write(writeline)

    f_new_open.close()

    allfiles.append(f_new)


tmp_condor = open('{ld}/submitFile.condor'.format(ld=logdir), 'w')
tmp_condor.write('''Executable = dummy_exec.sh
use_x509userproxy = True
getenv      = True
Log        = {ld}/log_running_$(ProcId).log
Output     = {ld}/log_running_$(ProcId).out
Error      = {ld}/log_running_$(ProcId).error

requirements = (OpSysAndVer =?= "SLCern6")

environment = "LS_SUBCWD={here}"
+MaxRuntime = 14000 \n\n'''.format(ld=logdir,here=os.environ['PWD']))
for pyfile in allfiles:
    tmp_condor.write('arguments = {cmssw} {pyfile} $(ClusterId) $(ProcId)\n'.format(cmssw=os.environ['PWD'], pyfile=os.environ['PWD']+'/'+pyfile  ) )
    tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit {ld}/submitFile.condor'.format(ld=logdir)
