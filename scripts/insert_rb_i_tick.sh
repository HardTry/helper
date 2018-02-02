#!/bin/sh
python tbcsv2mongo.py /data/sean/20170508 rb1710_Tick.csv 10.10.10.13:29875 rb1710 > /tmp/t2m.log
python tbcsv2mongo.py /data/sean/20170508 rb1801_Tick.csv 10.10.10.13:29875 rb1801 > /tmp/t2m.log 
python tbcsv2mongo.py /data/sean/20170508 rb888_Tick.csv 10.10.10.13:29875 rb888 > /tmp/t2m.log 
python tbcsv2mongo.py /data/sean/20170508 rb000_Tick.csv 10.10.10.13:29875 rb000 > /tmp/t2m.log 

python tbcsv2mongo.py /data/sean/20170508 i1709_Tick.csv 10.10.10.13:29875 i1709 > /tmp/t2m.log
python tbcsv2mongo.py /data/sean/20170508 i1801_Tick.csv 10.10.10.13:29875 i1801 > /tmp/t2m.log 
python tbcsv2mongo.py /data/sean/20170508 i9888_Tick.csv 10.10.10.13:29875 i9888 > /tmp/t2m.log
python tbcsv2mongo.py /data/sean/20170508 i9000_Tick.csv 10.10.10.13:29875 i9000 > /tmp/t2m.log 
