## Cluster usage

We have available a cluster for running computationally demanding jobs.
To access the cluster, you need to be on our local network on VPN. Accessing the managing server
can be done by

```commandline
ssh nmgmt
```

This management server belong to the 'old' cluster. We have also a 'new' cluster
in a process of being set-up. Up to this day (20.2.2025), the new cluster is not ready yet. The overall logic of the
usage of the new cluster should be fairly similar to the old one, but some details may vary. This
tutorials refers to the 'old' cluster.

The cluster uses [Slurm](https://slurm.schedmd.com/) system to handle the submission of computational jobs by the users.
You can list a basic overview of the  available computational nodes by the command
```commandline
sinfo
```

