#!/bin/bash

#When stacks are created, some policies have to be created in the sandbox compartment
#rather than the stack compartment, so will be missed by delete.py on the stack compartment

#This fetches the OCIDs of the policies with the 5 letter code of the stack, then deletes
#Usage: bash policy-delete.sh <sandbox OCID> <5 letter stack code>

for policy in $(oci iam policy list -c $1 --all | python get.py $2);
do
    echo Deleting $policy
    oci iam policy delete --policy-id $policy --wait-for-state SUCCEEDED  --wait-for-state FAILED
done