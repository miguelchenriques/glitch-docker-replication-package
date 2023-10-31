# GLITCH's Docker Replication package
This repository contains the Dockerfile and scripts use to create the replication package used to
evaluate the extension of GLICTH to support Docker

## Download
Download the glitch-docker.tar file from https://figshare.com/articles/dataset/GLITCH_Docker_Replication_Package/24467647

## Instalation
To be able to use the replication package follow the steps:
- Run `docker load < glitch-docker.tar` in the folder with the tar file previously downloaded.
- Run `docker run -it --name glitch-docker-replication -d glitch /bin/bash`
- Run `docker attach glitch-docker-replication`

## Usage
 In the root folder we have the datasets and the oracle classification csv, to get glitch results on the
 datasets run glitch as normal in the dataset mode, for example:
 `glitch --csv --dataset --tech docker datasets/docker/`

 To run dsl use the dsl python script, this script takes an argument, either dataset or oracle.
 `python3 -m scripts.dsl oracle`
 To run GLITCH on the docker oracle use the glitch script. `python3 -m scripts.glitch`
