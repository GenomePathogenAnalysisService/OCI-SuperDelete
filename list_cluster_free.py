#!/usr/bin/env python3

import json
import oci

config = oci.config.from_file()
identity_client = oci.identity.IdentityClient(config)
file_storage_client = oci.file_storage.FileStorageClient(config)
limits_client = oci.limits.LimitsClient(config)

tenancy_id = "ocid1.tenancy.oc1..aaaaaaaa4mcyyn2h7c37qyuq5ttoaeb4mh4cuprqnlsmmcirop5hgl3ehrvq"

limits = limits_client.get_resource_availability(service_name='container-engine', limit_name='cluster-count', 
    compartment_id=tenancy_id)
print(limits.data)
print(f"root - available = { limits.data.available }")
