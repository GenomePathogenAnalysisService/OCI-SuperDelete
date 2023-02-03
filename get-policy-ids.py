'''Parse the JSON output of `oci iam policy list` to get the OCID of
the policies who's names contain `sp3-<code>` where `<code>` is the 
5 letter code of the stack. Ensure that they are one of the ones created 
by the terraform
'''
import json
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        #We have the 5 letters so lets find the OCIDs

        #Get from stdin
        try:
            #JSON parsing doesn't like an empty string, so exit nicely if JSON parsing errors
            policies = json.loads(sys.stdin.read().strip())
        except json.decoder.JSONDecodeError:
            print("No policies to delete")
            sys.exit(0)

        #Strict list of the policies to delete based on policies created
        whitelist = [f"sp3-{sys.argv[1]}_HeadNode_Artifacts",
                        f"sp3-{sys.argv[1]}_HeadNode_Object",
                        f"sp3-{sys.argv[1]}_Stack_Object",
                        f"sp3-{sys.argv[1]}_HeadNode_Secrets"]

        #Iter the JSON, match name on whitelist to get OCID
        for policy in policies['data']:
            if policy['name'] in whitelist:
                print(policy['id'])
    else:
        print("Usage: python get.py <5 letter ID>")
