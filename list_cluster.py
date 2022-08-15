#!/usr/bin/env python3

import json
import oci

def get_clusters(comp, identity_client, ce_client, error_comparments):
    clusters = list()

    try:
        comp_clusters = ce_client.list_clusters(compartment_id=comp.id)
        if len(comp_clusters.data) > 0:
            print(f"{ comp.name } - { comp_clusters.data }")
            clusters += comp_clusters.data
    except Exception as e:
        error_comparments.append((comp.id, comp.name, f'compartment access - {e}'))
        print(f"{ comp.name } - Could not access")
    
    try:
        sub_comps = identity_client.list_compartments(compartment_id=comp.id,
                    lifecycle_state="ACTIVE").data
        
        if len(sub_comps) > 0:
            print(f"{ comp.name } sub_comps - {sub_comps}")
            for sub_comp in sub_comps:
                clusters += get_clusters(sub_comp, identity_client, ce_client, error_comparments)
    except Exception as e:
        print(sub_comps)
        error_comparments.append((comp.id, comp.name, f'sub compartment access - {e}'))
        print(f"{ comp.name } sub_comps - Could not Access")
    
    return clusters

config = oci.config.from_file()
identity_client = oci.identity.IdentityClient(config)
ce_client = oci.container_engine.ContainerEngineClient(config)
limits_client = oci.limits.LimitsClient(config)

tenancy_id = "ocid1.tenancy.oc1..aaaaaaaa4mcyyn2h7c37qyuq5ttoaeb4mh4cuprqnlsmmcirop5hgl3ehrvq"
compartment_id = "ocid1.compartment.oc1..aaaaaaaao4kpjckz2pjmlict2ssrnx45ims7ttvxghlluo2tcwv6pgfdlepq"

compartments = identity_client.list_compartments(compartment_id=compartment_id,
                            lifecycle_state="ACTIVE")

clusters = list()
error_comparments = list()
for comp in compartments.data:
    try:
        comp_clusters = ce_client.list_clusters(compartment_id=comp.id)
        if len(comp_clusters.data) > 0:
            print(f"{ comp.id } / { comp.name } - { comp_clusters.data }")
    except Exception as e:
        error_comparments.append((comp.id, comp.name, f'compartment access - {e}'))
        print(f"{ comp.id } / { comp.name } - Could not access")

    clusters += get_clusters(comp, identity_client, ce_client, error_comparments)

print("clusters_summary")
print(clusters)

print("errors_summary")
print(error_comparments)