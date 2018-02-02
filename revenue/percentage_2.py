import matplotlib.pyplot as plt
import pandas as pd
from mongoengine import *
import sys, time, datetime
import numpy as np
import re
import math

long_margin = dict({'SR807':0.05,'CF709':0.05,'TA709':0.05,'SR811':0.05,'CF805':0.05,'SR805':0.05,'TA805':0.05,'TA712':0.05,'CF711':0.05,'TA711':0.05,'TA710':0.05,'TA804':0.05,'CF801':0.05,'TA801':0.05,'SR803':0.05,'bu1803':0.1,'SR711':0.05,'bu1712':0.1,'a1711':0.05,'jd1804':0.08,'fu1807':0.2,'sc1807':0.05,'ag1802':0.08,'al1802':0.1,'cu1802':0.09,'hc1802':0.1,'ni1802':0.1,'pb1802':0.1,'rb1802':0.1,'sn1802':0.09,'wr1802':0.2,'zn1802':0.1,'fu1806':0.2,'ZC804':0.05,'ZC802':0.05,'T1803':0.02,'TF1803':0.012,'IF1710':0.2,'jd1808':0.08,'cu1805':0.09,'hc1805':0.1,'ni1805':0.1,'pb1805':0.1,'rb1805':0.1,'ru1805':0.1,'sn1805':0.09,'wr1805':0.2,'zn1805':0.1,'ZC805':0.05,'jd1807':0.08,'TA802':0.05,'FG802':0.05,'MA802':0.07,'SF802':0.05,'SM802':0.05,'bb1802':0.2,'fb1802':0.2,'i1802':0.05,'j1802':0.05,'jd1802':0.08,'jm1802':0.05,'l1802':0.05,'p1802':0.05,'pp1802':0.05,'v1802':0.05,'fu1803':0.2,'sc2006':0.05,'ag1808':0.08,'al1808':0.1,'au1711':0.08,'bu1802':0.1,'cu1808':0.09,'hc1808':0.1,'ni1808':0.1,'pb1808':0.1,'rb1808':0.1,'ru1808':0.1,'sn1808':0.09,'wr1808':0.2,'zn1808':0.1,'ag1804':0.08,'al1804':0.1,'bu1710':0.1,'cu1804':0.09,'hc1804':0.1,'ni1804':0.1,'pb1804':0.1,'rb1804':0.1,'ru1804':0.1,'sn1804':0.09,'wr1804':0.2,'zn1804':0.1,'IC1803':0.3,'IF1803':0.2,'IH1803':0.2,'ZC806':0.05,'sc1808':0.05,'ZC808':0.05,'CY801':0.05,'CY802':0.05,'CY803':0.05,'CY804':0.05,'CY805':0.05,'CY806':0.05,'CY807':0.05,'CY808':0.05,'ag1806':0.08,'al1806':0.1,'au1709':0.08,'bu1906':0.1,'cu1806':0.09,'hc1806':0.1,'ni1806':0.1,'pb1806':0.1,'rb1806':0.1,'ru1806':0.1,'sn1806':0.09,'wr1806':0.2,'zn1806':0.1,'ag1803':0.08,'al1803':0.1,'au1804':0.08,'bu1903':0.1,'cu1803':0.09,'hc1803':0.1,'ni1803':0.1,'pb1803':0.1,'rb1803':0.1,'ru1803':0.1,'sn1803':0.09,'wr1803':0.2,'zn1803':0.1,'IC1712':0.3,'IF1712':0.2,'IH1712':0.2,'T1709':0.02,'TF1709':0.012,'SR801':0.05,'a1801':0.05,'ag1710':0.08,'al1710':0.1,'cu1710':0.09,'hc1710':0.1,'ni1710':0.1,'pb1710':0.1,'rb1710':0.1,'ru1710':0.1,'sn1710':0.09,'wr1710':0.2,'zn1710':0.1,'FG712':0.05,'MA712':0.07,'SF712':0.05,'SM712':0.05,'bb1712':0.2,'fb1712':0.2,'i1712':0.05,'j1712':0.05,'jd1712':0.08,'jm1712':0.05,'l1712':0.05,'m1712':0.05,'p1712':0.05,'pp1712':0.05,'v1712':0.05,'y1712':0.05,'ag1712':0.08,'al1712':0.1,'bu1812':0.1,'cu1712':0.09,'hc1712':0.1,'ni1712':0.1,'pb1712':0.1,'rb1712':0.1,'sn1712':0.09,'wr1712':0.2,'zn1712':0.1,'ag1711':0.08,'al1711':0.1,'au1712':0.08,'cu1711':0.09,'hc1711':0.1,'ni1711':0.1,'pb1711':0.1,'rb1711':0.1,'ru1711':0.1,'sn1711':0.09,'wr1711':0.2,'zn1711':0.1,'fu1711':0.2,'a1803':0.05,'b1709':0.05,'bb1709':0.2,'c1709':0.05,'cs1709':0.05,'fb1709':0.2,'i1709':0.05,'j1709':0.05,'jd1709':0.08,'jm1709':0.05,'l1709':0.05,'m1709':0.05,'p1709':0.05,'pp1709':0.05,'v1709':0.05,'y1709':0.05,'FG709':0.05,'JR709':0.05,'LR709':0.05,'MA709':0.07,'OI709':0.05,'PM709':0.05,'RI709':0.05,'RM709':0.05,'RS709':0.05,'bu1709':0.1,'ZC801':0.05,'IC1709':0.3,'IF1709':0.2,'IH1709':0.2,'ag1709':0.08,'al1709':0.1,'au1710':0.08,'bu1809':0.1,'cu1709':0.09,'hc1709':0.1,'ni1709':0.1,'pb1708':0.1,'pb1709':0.1,'rb1709':0.1,'ru1709':0.1,'sn1709':0.09,'wr1709':0.2,'zn1709':0.1,'SF709':0.05,'SM709':0.05,'WH709':0.05,'bb1710':0.2,'fb1710':0.2,'jd1803':0.08,'fu1804':0.2,'sc1710':0.05,'sc1711':0.05,'sc1712':0.05,'sc1801':0.05,'sc1802':0.05,'sc1803':0.05,'sc1804':0.05,'sc1806':0.05,'sc1809':0.05,'sc1812':0.05,'sc1903':0.05,'sc1906':0.05,'sc1909':0.05,'sc1912':0.05,'sc2003':0.05,'a1811':0.05,'b1805':0.05,'bb1805':0.2,'c1805':0.05,'cs1805':0.05,'fb1805':0.2,'ZC803':0.05,'T1712':0.02,'TF1712':0.012,'CF803':0.05,'SR809':0.05,'TA803':0.05,'a1809':0.05,'b1803':0.05,'bb1803':0.2,'c1803':0.05,'cs1803':0.05,'fb1803':0.2,'i1803':0.05,'j1803':0.05,'jm1803':0.05,'l1803':0.05,'m1803':0.05,'p1803':0.05,'pp1803':0.05,'v1803':0.05,'y1803':0.05,'FG803':0.05,'JR803':0.05,'LR803':0.05,'MA803':0.07,'OI803':0.05,'PM803':0.05,'RI803':0.05,'RM803':0.05,'i1710':0.05,'j1710':0.05,'jd1710':0.08,'jm1710':0.05,'l1710':0.05,'p1710':0.05,'pp1710':0.05,'v1710':0.05,'FG710':0.05,'MA710':0.07,'SF710':0.05,'SM710':0.05,'a1807':0.05,'b1801':0.05,'bb1801':0.2,'c1801':0.05,'cs1801':0.05,'fb1801':0.2,'i1801':0.05,'j1801':0.05,'jd1801':0.08,'jm1801':0.05,'l1801':0.05,'m1801':0.05,'ZC709':0.05,'ZC710':0.05,'ZC711':0.05,'ag1805':0.08,'al1805':0.1,'au1806':0.08,'bu1711':0.1,'jd1805':0.08,'i1805':0.05,'j1805':0.05,'jm1805':0.05,'l1805':0.05,'m1805':0.05,'p1805':0.05,'pp1805':0.05,'v1805':0.05,'y1805':0.05,'FG805':0.05,'JR805':0.05,'LR805':0.05,'MA805':0.07,'OI805':0.05,'PM805':0.05,'RI805':0.05,'RM805':0.05,'SF805':0.05,'SM805':0.05,'WH805':0.05,'ag1807':0.08,'SF803':0.05,'SM803':0.05,'WH803':0.05,'bb1804':0.2,'fb1804':0.2,'i1804':0.05,'j1804':0.05,'jm1804':0.05,'l1804':0.05,'p1804':0.05,'FG804':0.05,'pp1804':0.05,'v1804':0.05,'MA804':0.07,'SF804':0.05,'SM804':0.05,'sc1805':0.05,'ZC807':0.05,'SR901':0.05,'CF807':0.05,'TA807':0.05,'FG807':0.05,'JR807':0.05,'LR807':0.05,'MA807':0.07,'OI807':0.05,'PM807':0.05,'RI807':0.05,'RM807':0.05,'MA711':0.07,'OI711':0.05,'PM711':0.05,'RI711':0.05,'RM711':0.05,'RS711':0.05,'SF711':0.05,'SM711':0.05,'WH711':0.05,'a1805':0.05,'b1711':0.05,'bb1711':0.2,'c1711':0.05,'cs1711':0.05,'fb1711':0.2,'i1711':0.05,'j1711':0.05,'jd1711':0.08,'jm1711':0.05,'l1711':0.05,'m1711':0.05,'p1711':0.05,'pp1711':0.05,'v1711':0.05,'y1711':0.05,'FG711':0.05,'al1807':0.1,'au1808':0.08,'bu1801':0.1,'cu1807':0.09,'hc1807':0.1,'ni1807':0.1,'pb1807':0.1,'rb1807':0.1,'ru1807':0.1,'sn1807':0.09,'wr1807':0.2,'zn1807':0.1,'jd1806':0.08,'RS807':0.05,'SF807':0.05,'SM807':0.05,'WH807':0.05,'a1901':0.05,'b1807':0.05,'bb1807':0.2,'c1807':0.05,'cs1807':0.05,'fb1807':0.2,'i1807':0.05,'j1807':0.05,'jm1807':0.05,'l1807':0.05,'m1807':0.05,'p1807':0.05,'pp1807':0.05,'v1807':0.05,'y1807':0.05,'TA808':0.05,'bb1808':0.2,'fb1808':0.2,'i1808':0.05,'j1808':0.05,'jm1808':0.05,'l1808':0.05,'m1808':0.05,'p1808':0.05,'fu1710':0.2,'fu1712':0.2,'p1801':0.05,'pp1801':0.05,'v1801':0.05,'y1801':0.05,'FG801':0.05,'JR801':0.05,'LR801':0.05,'MA801':0.07,'OI801':0.05,'PM801':0.05,'RI801':0.05,'RM801':0.05,'SF801':0.05,'JR711':0.05,'LR711':0.05,'ZC712':0.05,'pp1808':0.05,'v1808':0.05,'y1808':0.05,'FG808':0.05,'MA808':0.07,'RM808':0.05,'RS808':0.05,'SF808':0.05,'SM808':0.05,'fu1801':0.2,'SM801':0.05,'WH801':0.05,'ag1801':0.08,'al1801':0.1,'au1802':0.08,'cu1801':0.09,'hc1801':0.1,'ni1801':0.1,'pb1801':0.1,'rb1801':0.1,'ru1801':0.1,'sn1801':0.09,'wr1801':0.2,'zn1801':0.1,'IC1710':0.3,'IH1710':0.2,'fu1805':0.2,'bu1806':0.1,'SR709':0.05,'TA806':0.05,'FG806':0.05,'MA806':0.07,'SF806':0.05,'SM806':0.05,'bb1806':0.2,'fb1806':0.2,'i1806':0.05,'j1806':0.05,'jm1806':0.05,'l1806':0.05,'p1806':0.05,'pp1806':0.05,'v1806':0.05,'fu1808':0.2,'a1709':0.05,'fu1809':0,'sc2009':0,'scefp':0})
short_margin = dict({'SR807':0.05,'CF709':0.05,'TA709':0.05,'SR811':0.05,'CF805':0.05,'SR805':0.05,'TA805':0.05,'TA712':0.05,'CF711':0.05,'TA711':0.05,'TA710':0.05,'TA804':0.05,'CF801':0.05,'TA801':0.05,'SR803':0.05,'bu1803':0.1,'SR711':0.05,'bu1712':0.1,'a1711':0.05,'jd1804':0.08,'fu1807':0.2,'sc1807':0.05,'ag1802':0.08,'al1802':0.1,'cu1802':0.09,'hc1802':0.1,'ni1802':0.1,'pb1802':0.1,'rb1802':0.1,'sn1802':0.09,'wr1802':0.2,'zn1802':0.1,'fu1806':0.2,'ZC804':0.05,'ZC802':0.05,'T1803':0.02,'TF1803':0.012,'IF1710':0.2,'jd1808':0.08,'cu1805':0.09,'hc1805':0.1,'ni1805':0.1,'pb1805':0.1,'rb1805':0.1,'ru1805':0.1,'sn1805':0.09,'wr1805':0.2,'zn1805':0.1,'ZC805':0.05,'jd1807':0.08,'TA802':0.05,'FG802':0.05,'MA802':0.07,'SF802':0.05,'SM802':0.05,'bb1802':0.2,'fb1802':0.2,'i1802':0.05,'j1802':0.05,'jd1802':0.08,'jm1802':0.05,'l1802':0.05,'p1802':0.05,'pp1802':0.05,'v1802':0.05,'fu1803':0.2,'sc2006':0.05,'ag1808':0.08,'al1808':0.1,'au1711':0.08,'bu1802':0.1,'cu1808':0.09,'hc1808':0.1,'ni1808':0.1,'pb1808':0.1,'rb1808':0.1,'ru1808':0.1,'sn1808':0.09,'wr1808':0.2,'zn1808':0.1,'ag1804':0.08,'al1804':0.1,'bu1710':0.1,'cu1804':0.09,'hc1804':0.1,'ni1804':0.1,'pb1804':0.1,'rb1804':0.1,'ru1804':0.1,'sn1804':0.09,'wr1804':0.2,'zn1804':0.1,'IC1803':0.3,'IF1803':0.2,'IH1803':0.2,'ZC806':0.05,'sc1808':0.05,'ZC808':0.05,'CY801':0.05,'CY802':0.05,'CY803':0.05,'CY804':0.05,'CY805':0.05,'CY806':0.05,'CY807':0.05,'CY808':0.05,'ag1806':0.08,'al1806':0.1,'au1709':0.08,'bu1906':0.1,'cu1806':0.09,'hc1806':0.1,'ni1806':0.1,'pb1806':0.1,'rb1806':0.1,'ru1806':0.1,'sn1806':0.09,'wr1806':0.2,'zn1806':0.1,'ag1803':0.08,'al1803':0.1,'au1804':0.08,'bu1903':0.1,'cu1803':0.09,'hc1803':0.1,'ni1803':0.1,'pb1803':0.1,'rb1803':0.1,'ru1803':0.1,'sn1803':0.09,'wr1803':0.2,'zn1803':0.1,'IC1712':0.3,'IF1712':0.2,'IH1712':0.2,'T1709':0.02,'TF1709':0.012,'SR801':0.05,'a1801':0.05,'ag1710':0.08,'al1710':0.1,'cu1710':0.09,'hc1710':0.1,'ni1710':0.1,'pb1710':0.1,'rb1710':0.1,'ru1710':0.1,'sn1710':0.09,'wr1710':0.2,'zn1710':0.1,'FG712':0.05,'MA712':0.07,'SF712':0.05,'SM712':0.05,'bb1712':0.2,'fb1712':0.2,'i1712':0.05,'j1712':0.05,'jd1712':0.08,'jm1712':0.05,'l1712':0.05,'m1712':0.05,'p1712':0.05,'pp1712':0.05,'v1712':0.05,'y1712':0.05,'ag1712':0.08,'al1712':0.1,'bu1812':0.1,'cu1712':0.09,'hc1712':0.1,'ni1712':0.1,'pb1712':0.1,'rb1712':0.1,'sn1712':0.09,'wr1712':0.2,'zn1712':0.1,'ag1711':0.08,'al1711':0.1,'au1712':0.08,'cu1711':0.09,'hc1711':0.1,'ni1711':0.1,'pb1711':0.1,'rb1711':0.1,'ru1711':0.1,'sn1711':0.09,'wr1711':0.2,'zn1711':0.1,'fu1711':0.2,'a1803':0.05,'b1709':0.05,'bb1709':0.2,'c1709':0.05,'cs1709':0.05,'fb1709':0.2,'i1709':0.05,'j1709':0.05,'jd1709':0.08,'jm1709':0.05,'l1709':0.05,'m1709':0.05,'p1709':0.05,'pp1709':0.05,'v1709':0.05,'y1709':0.05,'FG709':0.05,'JR709':0.05,'LR709':0.05,'MA709':0.07,'OI709':0.05,'PM709':0.05,'RI709':0.05,'RM709':0.05,'RS709':0.05,'bu1709':0.1,'ZC801':0.05,'IC1709':0.3,'IF1709':0.2,'IH1709':0.2,'ag1709':0.08,'al1709':0.1,'au1710':0.08,'bu1809':0.1,'cu1709':0.09,'hc1709':0.1,'ni1709':0.1,'pb1708':0.1,'pb1709':0.1,'rb1709':0.1,'ru1709':0.1,'sn1709':0.09,'wr1709':0.2,'zn1709':0.1,'SF709':0.05,'SM709':0.05,'WH709':0.05,'bb1710':0.2,'fb1710':0.2,'jd1803':0.08,'fu1804':0.2,'sc1710':0.05,'sc1711':0.05,'sc1712':0.05,'sc1801':0.05,'sc1802':0.05,'sc1803':0.05,'sc1804':0.05,'sc1806':0.05,'sc1809':0.05,'sc1812':0.05,'sc1903':0.05,'sc1906':0.05,'sc1909':0.05,'sc1912':0.05,'sc2003':0.05,'a1811':0.05,'b1805':0.05,'bb1805':0.2,'c1805':0.05,'cs1805':0.05,'fb1805':0.2,'ZC803':0.05,'T1712':0.02,'TF1712':0.012,'CF803':0.05,'SR809':0.05,'TA803':0.05,'a1809':0.05,'b1803':0.05,'bb1803':0.2,'c1803':0.05,'cs1803':0.05,'fb1803':0.2,'i1803':0.05,'j1803':0.05,'jm1803':0.05,'l1803':0.05,'m1803':0.05,'p1803':0.05,'pp1803':0.05,'v1803':0.05,'y1803':0.05,'FG803':0.05,'JR803':0.05,'LR803':0.05,'MA803':0.07,'OI803':0.05,'PM803':0.05,'RI803':0.05,'RM803':0.05,'i1710':0.05,'j1710':0.05,'jd1710':0.08,'jm1710':0.05,'l1710':0.05,'p1710':0.05,'pp1710':0.05,'v1710':0.05,'FG710':0.05,'MA710':0.07,'SF710':0.05,'SM710':0.05,'a1807':0.05,'b1801':0.05,'bb1801':0.2,'c1801':0.05,'cs1801':0.05,'fb1801':0.2,'i1801':0.05,'j1801':0.05,'jd1801':0.08,'jm1801':0.05,'l1801':0.05,'m1801':0.05,'ZC709':0.05,'ZC710':0.05,'ZC711':0.05,'ag1805':0.08,'al1805':0.1,'au1806':0.08,'bu1711':0.1,'jd1805':0.08,'i1805':0.05,'j1805':0.05,'jm1805':0.05,'l1805':0.05,'m1805':0.05,'p1805':0.05,'pp1805':0.05,'v1805':0.05,'y1805':0.05,'FG805':0.05,'JR805':0.05,'LR805':0.05,'MA805':0.07,'OI805':0.05,'PM805':0.05,'RI805':0.05,'RM805':0.05,'SF805':0.05,'SM805':0.05,'WH805':0.05,'ag1807':0.08,'SF803':0.05,'SM803':0.05,'WH803':0.05,'bb1804':0.2,'fb1804':0.2,'i1804':0.05,'j1804':0.05,'jm1804':0.05,'l1804':0.05,'p1804':0.05,'FG804':0.05,'pp1804':0.05,'v1804':0.05,'MA804':0.07,'SF804':0.05,'SM804':0.05,'sc1805':0.05,'ZC807':0.05,'SR901':0.05,'CF807':0.05,'TA807':0.05,'FG807':0.05,'JR807':0.05,'LR807':0.05,'MA807':0.07,'OI807':0.05,'PM807':0.05,'RI807':0.05,'RM807':0.05,'MA711':0.07,'OI711':0.05,'PM711':0.05,'RI711':0.05,'RM711':0.05,'RS711':0.05,'SF711':0.05,'SM711':0.05,'WH711':0.05,'a1805':0.05,'b1711':0.05,'bb1711':0.2,'c1711':0.05,'cs1711':0.05,'fb1711':0.2,'i1711':0.05,'j1711':0.05,'jd1711':0.08,'jm1711':0.05,'l1711':0.05,'m1711':0.05,'p1711':0.05,'pp1711':0.05,'v1711':0.05,'y1711':0.05,'FG711':0.05,'al1807':0.1,'au1808':0.08,'bu1801':0.1,'cu1807':0.09,'hc1807':0.1,'ni1807':0.1,'pb1807':0.1,'rb1807':0.1,'ru1807':0.1,'sn1807':0.09,'wr1807':0.2,'zn1807':0.1,'jd1806':0.08,'RS807':0.05,'SF807':0.05,'SM807':0.05,'WH807':0.05,'a1901':0.05,'b1807':0.05,'bb1807':0.2,'c1807':0.05,'cs1807':0.05,'fb1807':0.2,'i1807':0.05,'j1807':0.05,'jm1807':0.05,'l1807':0.05,'m1807':0.05,'p1807':0.05,'pp1807':0.05,'v1807':0.05,'y1807':0.05,'TA808':0.05,'bb1808':0.2,'fb1808':0.2,'i1808':0.05,'j1808':0.05,'jm1808':0.05,'l1808':0.05,'m1808':0.05,'p1808':0.05,'fu1710':0.2,'fu1712':0.2,'p1801':0.05,'pp1801':0.05,'v1801':0.05,'y1801':0.05,'FG801':0.05,'JR801':0.05,'LR801':0.05,'MA801':0.07,'OI801':0.05,'PM801':0.05,'RI801':0.05,'RM801':0.05,'SF801':0.05,'JR711':0.05,'LR711':0.05,'ZC712':0.05,'pp1808':0.05,'v1808':0.05,'y1808':0.05,'FG808':0.05,'MA808':0.07,'RM808':0.05,'RS808':0.05,'SF808':0.05,'SM808':0.05,'fu1801':0.2,'SM801':0.05,'WH801':0.05,'ag1801':0.08,'al1801':0.1,'au1802':0.08,'cu1801':0.09,'hc1801':0.1,'ni1801':0.1,'pb1801':0.1,'rb1801':0.1,'ru1801':0.1,'sn1801':0.09,'wr1801':0.2,'zn1801':0.1,'IC1710':0.3,'IH1710':0.2,'fu1805':0.2,'bu1806':0.1,'SR709':0.05,'TA806':0.05,'FG806':0.05,'MA806':0.07,'SF806':0.05,'SM806':0.05,'bb1806':0.2,'fb1806':0.2,'i1806':0.05,'j1806':0.05,'jm1806':0.05,'l1806':0.05,'p1806':0.05,'pp1806':0.05,'v1806':0.05,'fu1808':0.2,'a1709':0.05,'fu1809':0,'sc2009':0,'scefp':0})
unit = dict({'SR807':10,'CF709':5,'TA709':5,'SR811':10,'CF805':5,'SR805':10,'TA805':5,'TA712':5,'CF711':5,'TA711':5,'TA710':5,'TA804':5,'CF801':5,'TA801':5,'SR803':10,'bu1803':10,'SR711':10,'bu1712':10,'a1711':10,'jd1804':10,'fu1807':50,'sc1807':1000,'ag1802':15,'al1802':5,'cu1802':5,'hc1802':10,'ni1802':1,'pb1802':5,'rb1802':10,'sn1802':1,'wr1802':10,'zn1802':5,'fu1806':50,'ZC804':100,'ZC802':100,'T1803':10000,'TF1803':10000,'IF1710':300,'jd1808':10,'cu1805':5,'hc1805':10,'ni1805':1,'pb1805':5,'rb1805':10,'ru1805':10,'sn1805':1,'wr1805':10,'zn1805':5,'ZC805':100,'jd1807':10,'TA802':5,'FG802':20,'MA802':10,'SF802':5,'SM802':5,'bb1802':500,'fb1802':500,'i1802':100,'j1802':100,'jd1802':10,'jm1802':60,'l1802':5,'p1802':10,'pp1802':5,'v1802':5,'fu1803':50,'sc2006':1000,'ag1808':15,'al1808':5,'au1711':1000,'bu1802':10,'cu1808':5,'hc1808':10,'ni1808':1,'pb1808':5,'rb1808':10,'ru1808':10,'sn1808':1,'wr1808':10,'zn1808':5,'ag1804':15,'al1804':5,'bu1710':10,'cu1804':5,'hc1804':10,'ni1804':1,'pb1804':5,'rb1804':10,'ru1804':10,'sn1804':1,'wr1804':10,'zn1804':5,'IC1803':200,'IF1803':300,'IH1803':300,'ZC806':100,'sc1808':1000,'ZC808':100,'CY801':5,'CY802':5,'CY803':5,'CY804':5,'CY805':5,'CY806':5,'CY807':5,'CY808':5,'ag1806':15,'al1806':5,'au1709':1000,'bu1906':10,'cu1806':5,'hc1806':10,'ni1806':1,'pb1806':5,'rb1806':10,'ru1806':10,'sn1806':1,'wr1806':10,'zn1806':5,'ag1803':15,'al1803':5,'au1804':1000,'bu1903':10,'cu1803':5,'hc1803':10,'ni1803':1,'pb1803':5,'rb1803':10,'ru1803':10,'sn1803':1,'wr1803':10,'zn1803':5,'IC1712':200,'IF1712':300,'IH1712':300,'T1709':10000,'TF1709':10000,'SR801':10,'a1801':10,'ag1710':15,'al1710':5,'cu1710':5,'hc1710':10,'ni1710':1,'pb1710':5,'rb1710':10,'ru1710':10,'sn1710':1,'wr1710':10,'zn1710':5,'FG712':20,'MA712':10,'SF712':5,'SM712':5,'bb1712':500,'fb1712':500,'i1712':100,'j1712':100,'jd1712':10,'jm1712':60,'l1712':5,'m1712':10,'p1712':10,'pp1712':5,'v1712':5,'y1712':10,'ag1712':15,'al1712':5,'bu1812':10,'cu1712':5,'hc1712':10,'ni1712':1,'pb1712':5,'rb1712':10,'sn1712':1,'wr1712':10,'zn1712':5,'ag1711':15,'al1711':5,'au1712':1000,'cu1711':5,'hc1711':10,'ni1711':1,'pb1711':5,'rb1711':10,'ru1711':10,'sn1711':1,'wr1711':10,'zn1711':5,'fu1711':50,'a1803':10,'b1709':10,'bb1709':500,'c1709':10,'cs1709':10,'fb1709':500,'i1709':100,'j1709':100,'jd1709':10,'jm1709':60,'l1709':5,'m1709':10,'p1709':10,'pp1709':5,'v1709':5,'y1709':10,'FG709':20,'JR709':20,'LR709':20,'MA709':10,'OI709':10,'PM709':50,'RI709':20,'RM709':10,'RS709':10,'bu1709':10,'ZC801':100,'IC1709':200,'IF1709':300,'IH1709':300,'ag1709':15,'al1709':5,'au1710':1000,'bu1809':10,'cu1709':5,'hc1709':10,'ni1709':1,'pb1708':5,'pb1709':5,'rb1709':10,'ru1709':10,'sn1709':1,'wr1709':10,'zn1709':5,'SF709':5,'SM709':5,'WH709':20,'bb1710':500,'fb1710':500,'jd1803':10,'fu1804':50,'sc1710':1000,'sc1711':1000,'sc1712':1000,'sc1801':1000,'sc1802':1000,'sc1803':1000,'sc1804':1000,'sc1806':1000,'sc1809':1000,'sc1812':1000,'sc1903':1000,'sc1906':1000,'sc1909':1000,'sc1912':1000,'sc2003':1000,'a1811':10,'b1805':10,'bb1805':500,'c1805':10,'cs1805':10,'fb1805':500,'ZC803':100,'T1712':10000,'TF1712':10000,'CF803':5,'SR809':10,'TA803':5,'a1809':10,'b1803':10,'bb1803':500,'c1803':10,'cs1803':10,'fb1803':500,'i1803':100,'j1803':100,'jm1803':60,'l1803':5,'m1803':10,'p1803':10,'pp1803':5,'v1803':5,'y1803':10,'FG803':20,'JR803':20,'LR803':20,'MA803':10,'OI803':10,'PM803':50,'RI803':20,'RM803':10,'i1710':100,'j1710':100,'jd1710':10,'jm1710':60,'l1710':5,'p1710':10,'pp1710':5,'v1710':5,'FG710':20,'MA710':10,'SF710':5,'SM710':5,'a1807':10,'b1801':10,'bb1801':500,'c1801':10,'cs1801':10,'fb1801':500,'i1801':100,'j1801':100,'jd1801':10,'jm1801':60,'l1801':5,'m1801':10,'ZC709':100,'ZC710':100,'ZC711':100,'ag1805':15,'al1805':5,'au1806':1000,'bu1711':10,'jd1805':10,'i1805':100,'j1805':100,'jm1805':60,'l1805':5,'m1805':10,'p1805':10,'pp1805':5,'v1805':5,'y1805':10,'FG805':20,'JR805':20,'LR805':20,'MA805':10,'OI805':10,'PM805':50,'RI805':20,'RM805':10,'SF805':5,'SM805':5,'WH805':20,'ag1807':15,'SF803':5,'SM803':5,'WH803':20,'bb1804':500,'fb1804':500,'i1804':100,'j1804':100,'jm1804':60,'l1804':5,'p1804':10,'FG804':20,'pp1804':5,'v1804':5,'MA804':10,'SF804':5,'SM804':5,'sc1805':1000,'ZC807':100,'SR901':10,'CF807':5,'TA807':5,'FG807':20,'JR807':20,'LR807':20,'MA807':10,'OI807':10,'PM807':50,'RI807':20,'RM807':10,'MA711':10,'OI711':10,'PM711':50,'RI711':20,'RM711':10,'RS711':10,'SF711':5,'SM711':5,'WH711':20,'a1805':10,'b1711':10,'bb1711':500,'c1711':10,'cs1711':10,'fb1711':500,'i1711':100,'j1711':100,'jd1711':10,'jm1711':60,'l1711':5,'m1711':10,'p1711':10,'pp1711':5,'v1711':5,'y1711':10,'FG711':20,'al1807':5,'au1808':1000,'bu1801':10,'cu1807':5,'hc1807':10,'ni1807':1,'pb1807':5,'rb1807':10,'ru1807':10,'sn1807':1,'wr1807':10,'zn1807':5,'jd1806':10,'RS807':10,'SF807':5,'SM807':5,'WH807':20,'a1901':10,'b1807':10,'bb1807':500,'c1807':10,'cs1807':10,'fb1807':500,'i1807':100,'j1807':100,'jm1807':60,'l1807':5,'m1807':10,'p1807':10,'pp1807':5,'v1807':5,'y1807':10,'TA808':5,'bb1808':500,'fb1808':500,'i1808':100,'j1808':100,'jm1808':60,'l1808':5,'m1808':10,'p1808':10,'fu1710':50,'fu1712':50,'p1801':10,'pp1801':5,'v1801':5,'y1801':10,'FG801':20,'JR801':20,'LR801':20,'MA801':10,'OI801':10,'PM801':50,'RI801':20,'RM801':10,'SF801':5,'JR711':20,'LR711':20,'ZC712':100,'pp1808':5,'v1808':5,'y1808':10,'FG808':20,'MA808':10,'RM808':10,'RS808':10,'SF808':5,'SM808':5,'fu1801':50,'SM801':5,'WH801':20,'ag1801':15,'al1801':5,'au1802':1000,'cu1801':5,'hc1801':10,'ni1801':1,'pb1801':5,'rb1801':10,'ru1801':10,'sn1801':1,'wr1801':10,'zn1801':5,'IC1710':200,'IH1710':300,'fu1805':50,'bu1806':10,'SR709':10,'TA806':5,'FG806':20,'MA806':10,'SF806':5,'SM806':5,'bb1806':500,'fb1806':500,'i1806':100,'j1806':100,'jm1806':60,'l1806':5,'p1806':10,'pp1806':5,'v1806':5,'fu1808':50,'a1709':10,'fu1809':50,'sc2009':1000,'scefp':1000})

class Money:
    def __init__(self):
        self.all_money = 200000000
        self.all_deposit = 0.0
        self.my_money = 600000
        self.my_ratio = self.my_money / self.all_money
        self.my_deposit = 0.0
        self.dpst_pcnt = 1.0
        self.max_dpst = self.my_money * self.dpst_pcnt
        self.commitment = 0.5 / 10000


    def __init__(self, am, mm, dpst_pcnt, commitment):
        self.reset(am, mm, dpst_pcnt, commitment)


    def reset(self, am, mm, dpst_pcnt, commitment):
        self.all_money = am
        self.all_deposit = 0.0
        self.my_money = mm
        self.my_ratio = self.my_money / self.all_money
        self.my_deposit = 0.0
        self.dpst_pcnt = dpst_pcnt
        self.max_dpst = self.my_money * self.dpst_pcnt
        self.commitment = commitment


    def to_json(self):
        return '{ all_money: ' + str(self.all_money  ) +\
                ', all_deposit: ' + str(self.all_deposit) +\
                ', my_ratio: ' + str(self.my_ratio   ) +\
                ', my_money: ' + str(self.my_money   ) +\
                ', my_deposit: ' + str(self.my_deposit ) + \
                ', dpst_pcnt: ' + str(self.dpst_pcnt) + \
                ', max_dpst: ' + str(self.max_dpst) + \
                ', commitment: ' + str(self.commitment ) + '}'


mmm = Money(200000000, 600000, 1.0, 0.0005)

def get_margin(inst, is_long):
    if is_long:
        return long_margin[inst]
    else:
        return short_margin[inst]


class Order:
    def __init__(self):
        self.direct = ''
        self.pos_ = 0
        self.price = 0
        self.posrev = 0
        self.rev = 0

    def __init__(self, direct, pos, price):
        self.direct = direct
        self.pos_ = pos
        self.price = price
        self.posrev = 0  # current revenue
        self.rev = 0  # revenue


class Trade:
    order = []
    allrev = 0

    def __init__(self, dm):
        self.dm = dm

    def openLong(self, cur_pos):
        if (0 == len(self.order) % 2):
            print 'Long ', cur_pos, self.dm.price[cur_pos]
            self.order.append(Order('a', cur_pos, self.dm.price[cur_pos]))
            return True
        else:
            return False

    def openShort(self, cur_pos):
        if (0 == len(self.order) % 2):
            print 'Short ', cur_pos, self.dm.price[cur_pos]
            self.order.append(Order('b', cur_pos, self.dm.price[cur_pos]))
            return True
        else:
            return False

    def closePosition(self, cur_pos):
        if (1 == len(self.order) % 2):
            c = Order('c', cur_pos, self.dm.price[cur_pos])
            if self.order[-1].direct == 'a':
                c.posrev = (c.price - self.order[-1].price) * 10
                c.rev = (c.price - self.order[-1].price) * 10 \
                        - (c.price + self.order[-1].price) * 0.0015
            else:
                c.posrev = (self.order[-1].price - c.price) * 10
                c.rev = (self.order[-1].price - c.price) * 10 \
                        - (c.price + self.order[-1].price) * 0.0015
            self.order.append(c)
            self.allrev += c.rev
            print 'Close', cur_pos, self.dm.price[cur_pos], c.posrev, c.rev, self.allrev
            return True
        else:
            return False


class CandleData(Document):
    High = FloatField()
    period = StringField()
    strDate = StringField()
    Volume = FloatField()
    instrument = StringField()
    Low = FloatField()
    Close = FloatField()
    openInterest = FloatField()
    Open = FloatField()
    strTime = StringField()
    fltTime = FloatField()

    meta = {
        'collection': 'candledata'
    }

class PositionStatus:
    vol = int(0)           # volume
    price = 0              # price
    deposit = 0.0          # deposit
    pct_trade = 0.0        # percent of trade
    rev = 0.0              # revenue
    pct_all = 0.0          # percent of all
    ut = 0.0               # update time
    myvol = int(0)         # my volume
    myprice = 0.0          # my price
    mydpst = 0.0           # my deposit
    myrev = 0.0            # my revenue of close
    mypct_trade  = 0.0     # my percent in all my deposit
    mypct_all    = 0.0     # my percent in all my money
    unit = 0
    margin = 0

    def to_json(self):
        return "{'vol      ':" + str(self.vol      ) +\
                "'price    ':" + str(self.price    ) +\
                "'deposit  ':" + str(self.deposit  ) +\
                "'pct_trade':" + str(self.pct_trade) +\
                "'rev      ':" + str(self.rev      ) +\
                "'pct_all  ':" + str(self.pct_all  ) +\
                "'ut       ':" + str(self.ut       ) +\
                "'myvol    ':" + str(self.myvol    ) +\
                "'myprice  ':" + str(self.myprice  ) +\
                "'mydpst   ':" + str(self.mydpst   ) + "}"

class Position:
    day = 0         # the trade day
    date = 0        # trade date
    time = 0        # trade stime
    inst = ''       # instrument name
    ls = PositionStatus() #long position
    ss = PositionStatus() #short position
    ts = PositionStatus() #total status

    def __init__(self, day, date, time, inst):
        self.day = day
        self.date = date
        self.time = time
        self.inst = inst

    def set_to_prev_pos(self, prev_pos):
        self.ls = prev_pos.ls
        self.ss = prev_pos.ss
        self.ts = prev_pos.ts
        # do not set percent, calculate every day
        self.ls.percent = self.ss.percent = self.ts.percent = 0.0
        # and do not set revenue, calculate every day
        self.ls.rev = self.ss.rev = self.t.rev = 0.0




def get_data_source(filepath):
    ds = pd.read_csv(filepath)

    ds['dir'] = ds[['dir', 'action']].apply(lambda x: x['dir'] if x['action'] > 0 else -x['dir'], axis=1)
    # get the margin by dir and instrumet code
    ds['margin'] = ds[['dir', 'inst']].apply(lambda x: long_margin[x['inst']] if x['dir'] > 0 else short_margin[x['inst']], axis=1)
    # get one unit number by instrument code
    ds['unit'] = ds.inst.map(unit)
    # set the money
    ds['money'] = ds.price * ds.volume * ds.unit * ds.margin

    #sort
    ds = ds.sort_values(['date', 'time', 'inst', 'action', 'dir'],
                        ascending = [True, True, True, False, False])

    #get all instruments
    instruments = ds['inst'].unique()
    #get all trade days
    trade_days = ds['trade_day'].unique()

    # set index
    # ds.index.names = [None]
    # ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return ds, instruments, trade_days


def get_instrument_code(inst):
    match = re.match(r"([a-z]+)([0-9]+)", inst, re.I)
    code = ''
    code_continue = ''
    if match:
        items = match.groups()
        code = items[0]
        if len(code) == 1:
            code_continue = code + '9888'
        else:
            code_continue = code + '888'

    return code, code_continue


def get_all_instrument_code(instruments):
    inst_codes = set()
    cl = set()
    ccl = dict()
    for inst in instruments:
        code, cc = get_instrument_code(inst)
        cl.add(code)
    ic = np.array(list(cl))
    ic = ic.astype(object)
    ic.sort()
    return ic


def get_float_time(row):
    d = str(row.time)
    if (len(d) < 6):
        d = '0' * (6 - len(d)) + d
    # print self.strDate + d
    if (len(d) == 6):
        dt = datetime.datetime.strptime(str(row.date) + d, "%Y%m%d%H%M%S")
        dt = dt.replace(second = 0)
        fltTime = float(time.mktime(dt.timetuple()))  # + ms
        ok = True
    else:
        fltTime = float(0)
        ok = False
    return fltTime, ok

def get_candel_1m_from_10s(candles):
    c = CandleData()
    c.High = 0
    c.period = '1m'
    c.strDate = candles[0].strDate
    c.Volume = 0
    c.instrument = candles[0].instrument
    c.Low = 0
    c.Close = candles[len(candles) - 1].Close
    c.openInterest = candles[len(candles) - 1].openInterest
    c.Open = candles[0].Open
    c.strTime = candles[0].strTime
    c.fltTime = candles[0].fltTime

    cmax = -1e20
    cmin = 1e20
    csum = 0
    for cc in candles:
        cmax = max(cmax, cc.High)
        cmin = min(cmin, cc.Low)
        csum += cc.Volume
    c.High = cmax
    c.Volume = csum
    c.Low = cmin
    return c


def get_1m_candle(cc, row):
    fltTime, ok = get_float_time(row)
    if (not ok):
        return None

    candles = CandleData.objects(instrument=cc, period='10s', fltTime__gt=fltTime - 1, fltTime__lt=fltTime + 60)
    if len(candles) < 1:
        print "can not get 10s candle data: ", cc, ', @', row.date, row.time
        return None
    return get_candel_1m_from_10s(candles)


def cal_invecment(ps, trade, is_open, is_long):
    ret = 0
    code, cc = get_instrument_code(trade.inst)
    candle = get_1m_candle(cc, trade)
    ps.unit = trade.unit
    ps.margin = trade.margin

    if is_open:
        ps.vol += trade.volume
        ps.deposit += trade.money
        if (ps.vol * trade.unit * trade.margin == 0):
            print 'Error vol', ps.vol, trade.unit, trade.margin, trade
        ps.price = ps.deposit / (ps.vol * trade.unit * trade.margin)
        ps.ut = candle.fltTime
        mmm.all_deposit += trade.money
        ps.pct_all = ps.deposit / mmm.all_money
        ps.pct_trade = ps.deposit / mmm.all_deposit

        # this instrument-deposit would take how many my money
        this_deposit = ps.pct_all * mmm.my_money
        # new add deposit
        new_delta = this_deposit - ps.mydpst
        if new_delta <= 0:
            # cant understand if it's negative
            new_delta = 0
        else:
            if new_delta + mmm.my_deposit > mmm.max_dpst:
                print "can not open new position", trade.inst, trade.trade_day
                # can i make a part of new position?
                new_delta = mmm.max_dpst - mmm.my_deposit
                if new_delta <= 0:
                    # can not understatnd
                    new_delta = 0
        #cal how many volume i can open
        if new_delta > 0:
            vol = int(new_delta / (trade.price * trade.unit * trade.margin))
            if vol > 0:
                new_delta = trade.price * vol * trade.unit * trade.margin
                ps.myvol += vol
                ps.mydpst += new_delta
                ps.myprice = ps.mydpst / (ps.myvol * trade.unit * trade.margin)
                mmm.my_deposit += new_delta
                ps.mypct_trade = ps.mydpst / mmm.my_deposit  # my percent in all my deposit
                ps.mypct_all = ps.mydpst / mmm.my_money  # my percent in all my money
                # print 'Open ', trade.inst, vol, ps.myvol, trade.dir, ps.price, ps.myprice
        # keep ps.revenue, calculate when close?
    else: #close
        if ps.vol < trade.volume:
            vdelta = ps.vol
            print "close error: ", trade.inst, trade.trade_day, ps.vol - trade.volume
        else:
            vdelta = trade.volume
        ps.vol -= vdelta
        delta = ps.price * vdelta * trade.unit * trade.margin
        ps.deposit -= delta
        # keep ps.price
        revenue = (trade.price - ps.price) * vdelta * trade.unit * trade.margin
        if not is_long:
            revenue = -revenue
        revenue -= (trade.price + ps.price) * vdelta * trade.unit * trade.margin * mmm.commitment
        ps.rev += revenue
        ps.ut = candle.fltTime
        mmm.all_deposit -= delta
        ps.pct_all = ps.deposit / mmm.all_money
        ps.pct_trade = ps.deposit / mmm.all_deposit

        if ps.myvol > 0:
            #how many deposit of this instrument i should take?
            delta = ps.mydpst - ps.pct_all * mmm.my_money
            if delta > 0:
                vol = int(delta / (ps.myprice * trade.unit * trade.margin))
                if (vol > 0):
                    if vol > ps.myvol:
                        vol = ps.myvol
                        delta = ps.mydpst
                    else:
                        delta = ps.myprice * trade.unit * trade.margin * vol
                    ps.myvol -= vol
                    ps.mydpst -= delta
                    mmm.my_deposit -= delta
                    myrev = (trade.price - ps.myprice) * vol * trade.unit * trade.margin
                    if not is_long:
                        myrev = -myrev
                    ps.myrev += myrev
                    ps.mypct_trade = ps.mydpst / mmm.my_deposit  # my percent in all my deposit
                    ps.mypct_all = ps.mydpst / mmm.my_money  # my percent in all my money
                    # print 'Close ', ps.myrev, trade.inst, vol, ps.myvol, trade.dir, ps.mydpst, mmm.my_deposit, ps.mypct_trade, ps.mypct_all


def on_new_trade_event(pso_row, trade):
    if (trade.action > 0):
        #open
        if (trade.dir > 0):
            #open long
            cal_invecment(pso_row.long, trade, True, True)
        else:
            #open short
            cal_invecment(pso_row.short, trade, True, False)
    else:
        #close
        if (trade.dir > 0):
            #close long
            cal_invecment(pso_row.long, trade, False, True)
        else:
            #close short
            cal_invecment(pso_row.short, trade, False, False)


def check_candle(ds):
    no_exists = set()
    for i in np.arange(ds.shape[0]):
        row = ds.iloc[i]
        code, cc = get_instrument_code(row.inst)

        # p = Position(row.trade_day, row.date, row.time, code)
        candle = get_1m_candle(cc, row)
        if candle is None:
            no_exists.add(cc)
    return no_exists

def init_position_status(ic):
    pso = pd.DataFrame(columns=(['long', 'short']), index=ic)
    for i in np.arange(pso.shape[0]):
        for j in np.arange(pso.shape[1]):
            pso.iloc[i][j] = PositionStatus()
    return pso

def init_psodf(ic):
    psodf = pd.DataFrame(columns=[
                               'L_vol',
                               'L_price',
                               'L_deposit',
                               'L_pct_trade',
                               'L_crev',
                               'L_pct_all',
                               'L_ut',
                               'L_myvol',
                               'L_mydpst',
                               'L_myrev',
                               'L_mypct_trade',
                               'L_mypct_all',
                               'S_vol',
                               'S_price',
                               'S_deposit',
                               'S_pct_trade',
                               'S_crev',
                               'S_pct_all',
                               'S_ut',
                               'S_myvol',
                               'S_mydpst',
                               'S_myrev',
                               'S_mypct_trade',
                               'S_mypct_all'],
                               index=ic)
    for i in np.arange(psodf.shape[0]):
        for j in np.arange(psodf.shape[1]):
            psodf.iloc[i][j] = 0.0
    return psodf

def ps_to_df(ps, pdf, prefix):
    pdf[prefix + 'vol'      ] = ps.vol
    pdf[prefix + 'price'    ] = ps.price
    pdf[prefix + 'deposit'  ] = ps.deposit
    pdf[prefix + 'pct_trade'] = ps.pct_trade
    pdf[prefix + 'rev'      ] = ps.rev
    pdf[prefix + 'pct_all'  ] = ps.pct_all
    pdf[prefix + 'ut'       ] = ps.ut
    pdf[prefix + 'myvol'    ] = ps.myvol
    pdf[prefix + 'mydpst'   ] = ps.mydpst
    pdf[prefix + 'myrev'    ] = ps.myrev
    pdf[prefix + 'mypct_trade'] = ps.mypct_trade
    pdf[prefix + 'mypct_all'  ] = ps.mypct_all



def pso_to_dataframe(ic, pso, psodf):
    for c in ic:
        pdf = psodf.loc[c]
        ps_to_df(pso.loc[c].long, pdf, 'L_')
        ps_to_df(pso.loc[c].short, pdf, 'S_')
        # print c, pdf.to_json()


def init_revenue_df(ic):
    psodf = pd.DataFrame(columns=[
                               'L_crev',
                               'L_pct_all',
                               'L_ut',
                               'L_myvol',
                               'L_mydpst',
                               'L_myrev',
                               'L_mypct_trade',
                               'L_mypct_all',
                               'S_vol',
                               'S_price',
                               'S_deposit',
                               'S_pct_trade',
                               'S_crev',
                               'S_pct_all',
                               'S_ut',
                               'S_myvol',
                               'S_mydpst',
                               'S_myrev',
                               'S_mypct_trade',
                               'S_mypct_all'],
                               index=ic)
    return psodf


def get_instrument_cc(code):
    if len(code) < 2:
        inst = code + '9888'
    else:
        inst = code + '888'
    return inst



def cheack_finished_candle(ic, trade_days):
    close_price = pd.DataFrame(columns=ic, index=trade_days)
    for trade_day in trade_days:
        cp = close_price.loc[trade_day]
        dt = datetime.datetime.strptime(str(trade_day) + '145900', "%Y%m%d%H%M%S")
        fltTime = float(time.mktime(dt.timetuple()))
        for code in ic:
            inst = get_instrument_cc(code)
            candles = CandleData.objects(instrument=inst, period='10s', fltTime__gt=fltTime - 1, fltTime__lt=fltTime + 60)
            if len(candles) < 1:
                print 'cheack_finished_candle error @ ', inst, trade_day
            else:
                candle = get_candel_1m_from_10s(candles)
                cp[code] = candle.Close
    return close_price



def get_trade_day_finished_candle(code, trade_day):
    inst = get_instrument_cc(code)
    dt = datetime.datetime.strptime(str(trade_day) + '145900', "%Y%m%d%H%M%S")
    fltTime = float(time.mktime(dt.timetuple()))
    candles = CandleData.objects(instrument=inst, period='10s', fltTime__gt=fltTime - 1, fltTime__lt=fltTime + 60)
    if len(candles) < 1:
        print "can not get 10s candle data: ", inst, ', @', str(trade_day) + '145900'
        return None
    return get_candel_1m_from_10s(candles)

def get_revenue(ps, price, is_all, is_long):
    rev = 0
    if is_all:
        rev = (price - ps.price) * ps.unit * ps.margin * ps.vol
    else:
        rev = (price - ps.myprice) * ps.unit * ps.margin * ps.myvol

    if not is_long:
        rev = -rev
    rev -= (price + ps.price) * ps.unit * ps.margin * ps.vol * mmm.commitment
    return rev

def get_daily_revenue(pso, ic, trade_day, cp):
    allrev = myall = 0
    for c in ic:
        lrev = mlrev = srev = msrev = 0
        ps = pso.loc[c]

        price = cp[c]
        if ps.long.vol > 0:
            lrev = ps.long.rev + get_revenue(ps.long, price, True, True)
            mlrev = ps.long.myrev + get_revenue(ps.long, price, False, True)
        if ps.short.vol > 0:
            srev = ps.short.rev + get_revenue(ps.short, price, True, False)
            msrev = ps.short.myrev + get_revenue(ps.short, price, False, False)

        rev = lrev + srev
        myrev = mlrev + msrev
        allrev += rev
        myall += myrev
        # print trade_day, c, rev, myrev, "(", lrev, mlrev, srev, msrev, ")", rev/mmm.all_money, myrev/mmm.my_money
    print trade_day, allrev, myall, mmm.my_deposit, mmm.all_deposit


def get_my_option(ds, instruments, trade_days, ic, cp):
    pso = init_position_status(ic)
    trade_day = ds.iloc[0].trade_day
    # psodf = init_psodf(ic)

    cols = np.append('L_' + ic, 'S_' + ic)

    m = pd.DataFrame(columns=np.append(cols, ['total_money']), index=trade_days)
    p = pd.DataFrame(columns=cols, index=trade_days)
    v = pd.DataFrame(columns=cols, index=trade_days)


    for i in np.arange(ds.shape[0]):
        row = ds.iloc[i]
        if trade_day < row.trade_day:
            # print trade_day, " :"
            # pso_to_dataframe(ic, pso, psodf)
            #for c in ic:
            #    pdf = psodf.loc[c]
            #    print c, pdf.to_json()
            cp = close_price.loc[trade_day]
            get_daily_revenue(pso, ic, trade_day, cp)
            vrow = v.loc[trade_day]
            mrow = m.loc[trade_day]
            prow = m.loc[trade_day]
            mrow.total_money = 0
            for c in ic:
                ps = pso.loc[c]
                vrow['L_' + c] = ps.long.vol
                vrow['S_' + c] = ps.short.vol
                mrow['L_' + c] = ps.long.deposit
                mrow['S_' + c] = ps.short.deposit
                prow['L_' + c] = ps.long.price
                prow['S_' + c] = ps.short.price

                mrow.total_money += mrow['L_' + c] + mrow['S_' + c]

            # if trade_day == 20170704:
            #    break

            trade_day = row.trade_day
            # print row.trade_day, " :"
        elif trade_day == row.trade_day:
            code, cc = get_instrument_code(row.inst)
            on_new_trade_event(pso.loc[code], row)
        else:
            print "trade day error: ", row
            break

    trade_day = 20170830
    cp = close_price.loc[trade_day]
    get_daily_revenue(pso, ic, trade_day, cp)
    vrow = v.loc[trade_day]
    mrow = m.loc[trade_day]
    prow = m.loc[trade_day]

    return m, v, p

'''
myvol = pd.read_csv("/home/sean/Downloads/myvol.csv")
myvol['minus'] = myvol[['ivol', 'before', 'after']].apply(lambda x: int((float(x['before'] - x['after']))/float(x['before']) * float(x['ivol']) + 0.5), axis=1)
myvol['hold'] = myvol['ivol'] - myvol['minus']
myvol.set_index(['code'], inplace=True)
'''

def draw_line(df, inst_code, x, ax, label):
    l = list(df['L_' + inst_code])
    s = list(df['S_' + inst_code])
    ax.set_xlim([min(x), max(x)])
    ax.set_ylim([min(min(s), min(l)), max(max(s), max(l)) * 1.01])
    ax.set_ylabel(label)
    # ax.set_xticklabels(trade_days)
    rects1 = ax.plot(x, l, 'r')
    rects2 = ax.plot(x, s, 'g')
    ax.legend((rects1[0], rects2[0]), ('Long', 'Short'))


def draw_mvp(m, v, inst_code, l):
    x = list(range(l))
    f, axs = plt.subplots(2, 1, figsize=(10, 10))
    # f.suptitle(inst_code + '888', fontsize=14)
    f.canvas.set_window_title(inst_code + '888')

    draw_line(v, inst_code, x, axs[0], 'volume')
    draw_line(m, inst_code, x, axs[1], 'deposits')

    plt.xlabel("trade day")
    f.tight_layout()
    # plt.savefig("/home/sean/tmp/analysis/instrument/" + inst_code + ".png")
    plt.show()
    # plt.close(f)



if __name__ == '__main__':
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    filepath = sys.argv[1]
    ds, instruments, trade_days = get_data_source(filepath)
    ic = get_all_instrument_code(instruments)
    icc = []
    for c in ic:
        icc.append(get_instrument_cc(c))

    #no_exists = check_candle(ds)
    #if (len(no_exists) > 0):
    #    print "Error"
    #    sys.exit(None)

    close_price = cheack_finished_candle(ic, trade_days)
    mmm.reset(100000000, 500000, 1.0, 0.00005)
    m, v, p = get_my_option(ds, instruments, trade_days, ic, close_price)

    for c in ic:
        draw_mvp(m, v, c, m.shape[0])

