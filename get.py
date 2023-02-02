'''Parse the JSON output of `oci iam policy list` to get the OCID of
the policies who's names contain `sp3-<code>` where `<code>` is the 
5 letter code of the stack
'''
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        #We have the 5 letters so lets find the OCIDs

        #Get from stdin
        policies = json.loads(sys.stdin.read().strip())

        #Iter the JSON, match on name to get OCID
        for policy in policies['data']:
            if f"sp3-{sys.argv[1]}" in policy['name']:
                print(policy['id'])
    else:
        print("Usage: python get.py <5 letter ID>")
