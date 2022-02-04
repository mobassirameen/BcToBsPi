#!/bin/bash

## make local directory
echo 'i am in this directory'
echo $PWD

echo ls of this directory:
ls ./

echo 'these are all arguments'
echo $*


echo moving to cmssw directory ${1}

cd $1
## do cmsenv and go back
echo doing cmsenv
eval `scramv1 runtime -sh`

echo 'moving back to local directory'

cd -

echo i am here now
pwd

echo 'setting seed'
echo $3
echo $4
let "SEED = ($3 + $3 * $4)/10"
echo "the seed is ${SEED}"
sed -i "s/SEED/${SEED}/g" $2

echo 'running cmsRun on the file'
echo cmsRun $2

echo 'doing a which on cmsRun first'
which cmsRun

echo 'now running for good'

cmsRun $2

echo 'done'


