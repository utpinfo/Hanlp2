#!/bin/bash
scp -r * root@192.168.201.24:/opt/Hanlp2 && ssh root@192.168.201.24 "systemctl restart hanlp-api"