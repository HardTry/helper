import matplotlib.pyplot as plt
import pandas as pd
from mongoengine import *
import time
import numpy as np
import re

long_margin = dict({'SR807':0.05,'CF709':0.05,'TA709':0.05,'SR811':0.05,'CF805':0.05,'SR805':0.05,'TA805':0.05,'TA712':0.05,'CF711':0.05,'TA711':0.05,'TA710':0.05,'TA804':0.05,'CF801':0.05,'TA801':0.05,'SR803':0.05,'bu1803':0.1,'SR711':0.05,'bu1712':0.1,'a1711':0.05,'jd1804':0.08,'fu1807':0.2,'sc1807':0.05,'ag1802':0.08,'al1802':0.1,'cu1802':0.09,'hc1802':0.1,'ni1802':0.1,'pb1802':0.1,'rb1802':0.1,'sn1802':0.09,'wr1802':0.2,'zn1802':0.1,'fu1806':0.2,'ZC804':0.05,'ZC802':0.05,'T1803':0.02,'TF1803':0.012,'IF1710':0.2,'jd1808':0.08,'cu1805':0.09,'hc1805':0.1,'ni1805':0.1,'pb1805':0.1,'rb1805':0.1,'ru1805':0.1,'sn1805':0.09,'wr1805':0.2,'zn1805':0.1,'ZC805':0.05,'jd1807':0.08,'TA802':0.05,'FG802':0.05,'MA802':0.07,'SF802':0.05,'SM802':0.05,'bb1802':0.2,'fb1802':0.2,'i1802':0.05,'j1802':0.05,'jd1802':0.08,'jm1802':0.05,'l1802':0.05,'p1802':0.05,'pp1802':0.05,'v1802':0.05,'fu1803':0.2,'sc2006':0.05,'ag1808':0.08,'al1808':0.1,'au1711':0.08,'bu1802':0.1,'cu1808':0.09,'hc1808':0.1,'ni1808':0.1,'pb1808':0.1,'rb1808':0.1,'ru1808':0.1,'sn1808':0.09,'wr1808':0.2,'zn1808':0.1,'ag1804':0.08,'al1804':0.1,'bu1710':0.1,'cu1804':0.09,'hc1804':0.1,'ni1804':0.1,'pb1804':0.1,'rb1804':0.1,'ru1804':0.1,'sn1804':0.09,'wr1804':0.2,'zn1804':0.1,'IC1803':0.3,'IF1803':0.2,'IH1803':0.2,'ZC806':0.05,'sc1808':0.05,'ZC808':0.05,'CY801':0.05,'CY802':0.05,'CY803':0.05,'CY804':0.05,'CY805':0.05,'CY806':0.05,'CY807':0.05,'CY808':0.05,'ag1806':0.08,'al1806':0.1,'au1709':0.08,'bu1906':0.1,'cu1806':0.09,'hc1806':0.1,'ni1806':0.1,'pb1806':0.1,'rb1806':0.1,'ru1806':0.1,'sn1806':0.09,'wr1806':0.2,'zn1806':0.1,'ag1803':0.08,'al1803':0.1,'au1804':0.08,'bu1903':0.1,'cu1803':0.09,'hc1803':0.1,'ni1803':0.1,'pb1803':0.1,'rb1803':0.1,'ru1803':0.1,'sn1803':0.09,'wr1803':0.2,'zn1803':0.1,'IC1712':0.3,'IF1712':0.2,'IH1712':0.2,'T1709':0.02,'TF1709':0.012,'SR801':0.05,'a1801':0.05,'ag1710':0.08,'al1710':0.1,'cu1710':0.09,'hc1710':0.1,'ni1710':0.1,'pb1710':0.1,'rb1710':0.1,'ru1710':0.1,'sn1710':0.09,'wr1710':0.2,'zn1710':0.1,'FG712':0.05,'MA712':0.07,'SF712':0.05,'SM712':0.05,'bb1712':0.2,'fb1712':0.2,'i1712':0.05,'j1712':0.05,'jd1712':0.08,'jm1712':0.05,'l1712':0.05,'m1712':0.05,'p1712':0.05,'pp1712':0.05,'v1712':0.05,'y1712':0.05,'ag1712':0.08,'al1712':0.1,'bu1812':0.1,'cu1712':0.09,'hc1712':0.1,'ni1712':0.1,'pb1712':0.1,'rb1712':0.1,'sn1712':0.09,'wr1712':0.2,'zn1712':0.1,'ag1711':0.08,'al1711':0.1,'au1712':0.08,'cu1711':0.09,'hc1711':0.1,'ni1711':0.1,'pb1711':0.1,'rb1711':0.1,'ru1711':0.1,'sn1711':0.09,'wr1711':0.2,'zn1711':0.1,'fu1711':0.2,'a1803':0.05,'b1709':0.05,'bb1709':0.2,'c1709':0.05,'cs1709':0.05,'fb1709':0.2,'i1709':0.05,'j1709':0.05,'jd1709':0.08,'jm1709':0.05,'l1709':0.05,'m1709':0.05,'p1709':0.05,'pp1709':0.05,'v1709':0.05,'y1709':0.05,'FG709':0.05,'JR709':0.05,'LR709':0.05,'MA709':0.07,'OI709':0.05,'PM709':0.05,'RI709':0.05,'RM709':0.05,'RS709':0.05,'bu1709':0.1,'ZC801':0.05,'IC1709':0.3,'IF1709':0.2,'IH1709':0.2,'ag1709':0.08,'al1709':0.1,'au1710':0.08,'bu1809':0.1,'cu1709':0.09,'hc1709':0.1,'ni1709':0.1,'pb1708':0.1,'pb1709':0.1,'rb1709':0.1,'ru1709':0.1,'sn1709':0.09,'wr1709':0.2,'zn1709':0.1,'SF709':0.05,'SM709':0.05,'WH709':0.05,'bb1710':0.2,'fb1710':0.2,'jd1803':0.08,'fu1804':0.2,'sc1710':0.05,'sc1711':0.05,'sc1712':0.05,'sc1801':0.05,'sc1802':0.05,'sc1803':0.05,'sc1804':0.05,'sc1806':0.05,'sc1809':0.05,'sc1812':0.05,'sc1903':0.05,'sc1906':0.05,'sc1909':0.05,'sc1912':0.05,'sc2003':0.05,'a1811':0.05,'b1805':0.05,'bb1805':0.2,'c1805':0.05,'cs1805':0.05,'fb1805':0.2,'ZC803':0.05,'T1712':0.02,'TF1712':0.012,'CF803':0.05,'SR809':0.05,'TA803':0.05,'a1809':0.05,'b1803':0.05,'bb1803':0.2,'c1803':0.05,'cs1803':0.05,'fb1803':0.2,'i1803':0.05,'j1803':0.05,'jm1803':0.05,'l1803':0.05,'m1803':0.05,'p1803':0.05,'pp1803':0.05,'v1803':0.05,'y1803':0.05,'FG803':0.05,'JR803':0.05,'LR803':0.05,'MA803':0.07,'OI803':0.05,'PM803':0.05,'RI803':0.05,'RM803':0.05,'i1710':0.05,'j1710':0.05,'jd1710':0.08,'jm1710':0.05,'l1710':0.05,'p1710':0.05,'pp1710':0.05,'v1710':0.05,'FG710':0.05,'MA710':0.07,'SF710':0.05,'SM710':0.05,'a1807':0.05,'b1801':0.05,'bb1801':0.2,'c1801':0.05,'cs1801':0.05,'fb1801':0.2,'i1801':0.05,'j1801':0.05,'jd1801':0.08,'jm1801':0.05,'l1801':0.05,'m1801':0.05,'ZC709':0.05,'ZC710':0.05,'ZC711':0.05,'ag1805':0.08,'al1805':0.1,'au1806':0.08,'bu1711':0.1,'jd1805':0.08,'i1805':0.05,'j1805':0.05,'jm1805':0.05,'l1805':0.05,'m1805':0.05,'p1805':0.05,'pp1805':0.05,'v1805':0.05,'y1805':0.05,'FG805':0.05,'JR805':0.05,'LR805':0.05,'MA805':0.07,'OI805':0.05,'PM805':0.05,'RI805':0.05,'RM805':0.05,'SF805':0.05,'SM805':0.05,'WH805':0.05,'ag1807':0.08,'SF803':0.05,'SM803':0.05,'WH803':0.05,'bb1804':0.2,'fb1804':0.2,'i1804':0.05,'j1804':0.05,'jm1804':0.05,'l1804':0.05,'p1804':0.05,'FG804':0.05,'pp1804':0.05,'v1804':0.05,'MA804':0.07,'SF804':0.05,'SM804':0.05,'sc1805':0.05,'ZC807':0.05,'SR901':0.05,'CF807':0.05,'TA807':0.05,'FG807':0.05,'JR807':0.05,'LR807':0.05,'MA807':0.07,'OI807':0.05,'PM807':0.05,'RI807':0.05,'RM807':0.05,'MA711':0.07,'OI711':0.05,'PM711':0.05,'RI711':0.05,'RM711':0.05,'RS711':0.05,'SF711':0.05,'SM711':0.05,'WH711':0.05,'a1805':0.05,'b1711':0.05,'bb1711':0.2,'c1711':0.05,'cs1711':0.05,'fb1711':0.2,'i1711':0.05,'j1711':0.05,'jd1711':0.08,'jm1711':0.05,'l1711':0.05,'m1711':0.05,'p1711':0.05,'pp1711':0.05,'v1711':0.05,'y1711':0.05,'FG711':0.05,'al1807':0.1,'au1808':0.08,'bu1801':0.1,'cu1807':0.09,'hc1807':0.1,'ni1807':0.1,'pb1807':0.1,'rb1807':0.1,'ru1807':0.1,'sn1807':0.09,'wr1807':0.2,'zn1807':0.1,'jd1806':0.08,'RS807':0.05,'SF807':0.05,'SM807':0.05,'WH807':0.05,'a1901':0.05,'b1807':0.05,'bb1807':0.2,'c1807':0.05,'cs1807':0.05,'fb1807':0.2,'i1807':0.05,'j1807':0.05,'jm1807':0.05,'l1807':0.05,'m1807':0.05,'p1807':0.05,'pp1807':0.05,'v1807':0.05,'y1807':0.05,'TA808':0.05,'bb1808':0.2,'fb1808':0.2,'i1808':0.05,'j1808':0.05,'jm1808':0.05,'l1808':0.05,'m1808':0.05,'p1808':0.05,'fu1710':0.2,'fu1712':0.2,'p1801':0.05,'pp1801':0.05,'v1801':0.05,'y1801':0.05,'FG801':0.05,'JR801':0.05,'LR801':0.05,'MA801':0.07,'OI801':0.05,'PM801':0.05,'RI801':0.05,'RM801':0.05,'SF801':0.05,'JR711':0.05,'LR711':0.05,'ZC712':0.05,'pp1808':0.05,'v1808':0.05,'y1808':0.05,'FG808':0.05,'MA808':0.07,'RM808':0.05,'RS808':0.05,'SF808':0.05,'SM808':0.05,'fu1801':0.2,'SM801':0.05,'WH801':0.05,'ag1801':0.08,'al1801':0.1,'au1802':0.08,'cu1801':0.09,'hc1801':0.1,'ni1801':0.1,'pb1801':0.1,'rb1801':0.1,'ru1801':0.1,'sn1801':0.09,'wr1801':0.2,'zn1801':0.1,'IC1710':0.3,'IH1710':0.2,'fu1805':0.2,'bu1806':0.1,'SR709':0.05,'TA806':0.05,'FG806':0.05,'MA806':0.07,'SF806':0.05,'SM806':0.05,'bb1806':0.2,'fb1806':0.2,'i1806':0.05,'j1806':0.05,'jm1806':0.05,'l1806':0.05,'p1806':0.05,'pp1806':0.05,'v1806':0.05,'fu1808':0.2,'a1709':0.05,'fu1809':0,'sc2009':0,'scefp':0})
short_margin = dict({'SR807':0.05,'CF709':0.05,'TA709':0.05,'SR811':0.05,'CF805':0.05,'SR805':0.05,'TA805':0.05,'TA712':0.05,'CF711':0.05,'TA711':0.05,'TA710':0.05,'TA804':0.05,'CF801':0.05,'TA801':0.05,'SR803':0.05,'bu1803':0.1,'SR711':0.05,'bu1712':0.1,'a1711':0.05,'jd1804':0.08,'fu1807':0.2,'sc1807':0.05,'ag1802':0.08,'al1802':0.1,'cu1802':0.09,'hc1802':0.1,'ni1802':0.1,'pb1802':0.1,'rb1802':0.1,'sn1802':0.09,'wr1802':0.2,'zn1802':0.1,'fu1806':0.2,'ZC804':0.05,'ZC802':0.05,'T1803':0.02,'TF1803':0.012,'IF1710':0.2,'jd1808':0.08,'cu1805':0.09,'hc1805':0.1,'ni1805':0.1,'pb1805':0.1,'rb1805':0.1,'ru1805':0.1,'sn1805':0.09,'wr1805':0.2,'zn1805':0.1,'ZC805':0.05,'jd1807':0.08,'TA802':0.05,'FG802':0.05,'MA802':0.07,'SF802':0.05,'SM802':0.05,'bb1802':0.2,'fb1802':0.2,'i1802':0.05,'j1802':0.05,'jd1802':0.08,'jm1802':0.05,'l1802':0.05,'p1802':0.05,'pp1802':0.05,'v1802':0.05,'fu1803':0.2,'sc2006':0.05,'ag1808':0.08,'al1808':0.1,'au1711':0.08,'bu1802':0.1,'cu1808':0.09,'hc1808':0.1,'ni1808':0.1,'pb1808':0.1,'rb1808':0.1,'ru1808':0.1,'sn1808':0.09,'wr1808':0.2,'zn1808':0.1,'ag1804':0.08,'al1804':0.1,'bu1710':0.1,'cu1804':0.09,'hc1804':0.1,'ni1804':0.1,'pb1804':0.1,'rb1804':0.1,'ru1804':0.1,'sn1804':0.09,'wr1804':0.2,'zn1804':0.1,'IC1803':0.3,'IF1803':0.2,'IH1803':0.2,'ZC806':0.05,'sc1808':0.05,'ZC808':0.05,'CY801':0.05,'CY802':0.05,'CY803':0.05,'CY804':0.05,'CY805':0.05,'CY806':0.05,'CY807':0.05,'CY808':0.05,'ag1806':0.08,'al1806':0.1,'au1709':0.08,'bu1906':0.1,'cu1806':0.09,'hc1806':0.1,'ni1806':0.1,'pb1806':0.1,'rb1806':0.1,'ru1806':0.1,'sn1806':0.09,'wr1806':0.2,'zn1806':0.1,'ag1803':0.08,'al1803':0.1,'au1804':0.08,'bu1903':0.1,'cu1803':0.09,'hc1803':0.1,'ni1803':0.1,'pb1803':0.1,'rb1803':0.1,'ru1803':0.1,'sn1803':0.09,'wr1803':0.2,'zn1803':0.1,'IC1712':0.3,'IF1712':0.2,'IH1712':0.2,'T1709':0.02,'TF1709':0.012,'SR801':0.05,'a1801':0.05,'ag1710':0.08,'al1710':0.1,'cu1710':0.09,'hc1710':0.1,'ni1710':0.1,'pb1710':0.1,'rb1710':0.1,'ru1710':0.1,'sn1710':0.09,'wr1710':0.2,'zn1710':0.1,'FG712':0.05,'MA712':0.07,'SF712':0.05,'SM712':0.05,'bb1712':0.2,'fb1712':0.2,'i1712':0.05,'j1712':0.05,'jd1712':0.08,'jm1712':0.05,'l1712':0.05,'m1712':0.05,'p1712':0.05,'pp1712':0.05,'v1712':0.05,'y1712':0.05,'ag1712':0.08,'al1712':0.1,'bu1812':0.1,'cu1712':0.09,'hc1712':0.1,'ni1712':0.1,'pb1712':0.1,'rb1712':0.1,'sn1712':0.09,'wr1712':0.2,'zn1712':0.1,'ag1711':0.08,'al1711':0.1,'au1712':0.08,'cu1711':0.09,'hc1711':0.1,'ni1711':0.1,'pb1711':0.1,'rb1711':0.1,'ru1711':0.1,'sn1711':0.09,'wr1711':0.2,'zn1711':0.1,'fu1711':0.2,'a1803':0.05,'b1709':0.05,'bb1709':0.2,'c1709':0.05,'cs1709':0.05,'fb1709':0.2,'i1709':0.05,'j1709':0.05,'jd1709':0.08,'jm1709':0.05,'l1709':0.05,'m1709':0.05,'p1709':0.05,'pp1709':0.05,'v1709':0.05,'y1709':0.05,'FG709':0.05,'JR709':0.05,'LR709':0.05,'MA709':0.07,'OI709':0.05,'PM709':0.05,'RI709':0.05,'RM709':0.05,'RS709':0.05,'bu1709':0.1,'ZC801':0.05,'IC1709':0.3,'IF1709':0.2,'IH1709':0.2,'ag1709':0.08,'al1709':0.1,'au1710':0.08,'bu1809':0.1,'cu1709':0.09,'hc1709':0.1,'ni1709':0.1,'pb1708':0.1,'pb1709':0.1,'rb1709':0.1,'ru1709':0.1,'sn1709':0.09,'wr1709':0.2,'zn1709':0.1,'SF709':0.05,'SM709':0.05,'WH709':0.05,'bb1710':0.2,'fb1710':0.2,'jd1803':0.08,'fu1804':0.2,'sc1710':0.05,'sc1711':0.05,'sc1712':0.05,'sc1801':0.05,'sc1802':0.05,'sc1803':0.05,'sc1804':0.05,'sc1806':0.05,'sc1809':0.05,'sc1812':0.05,'sc1903':0.05,'sc1906':0.05,'sc1909':0.05,'sc1912':0.05,'sc2003':0.05,'a1811':0.05,'b1805':0.05,'bb1805':0.2,'c1805':0.05,'cs1805':0.05,'fb1805':0.2,'ZC803':0.05,'T1712':0.02,'TF1712':0.012,'CF803':0.05,'SR809':0.05,'TA803':0.05,'a1809':0.05,'b1803':0.05,'bb1803':0.2,'c1803':0.05,'cs1803':0.05,'fb1803':0.2,'i1803':0.05,'j1803':0.05,'jm1803':0.05,'l1803':0.05,'m1803':0.05,'p1803':0.05,'pp1803':0.05,'v1803':0.05,'y1803':0.05,'FG803':0.05,'JR803':0.05,'LR803':0.05,'MA803':0.07,'OI803':0.05,'PM803':0.05,'RI803':0.05,'RM803':0.05,'i1710':0.05,'j1710':0.05,'jd1710':0.08,'jm1710':0.05,'l1710':0.05,'p1710':0.05,'pp1710':0.05,'v1710':0.05,'FG710':0.05,'MA710':0.07,'SF710':0.05,'SM710':0.05,'a1807':0.05,'b1801':0.05,'bb1801':0.2,'c1801':0.05,'cs1801':0.05,'fb1801':0.2,'i1801':0.05,'j1801':0.05,'jd1801':0.08,'jm1801':0.05,'l1801':0.05,'m1801':0.05,'ZC709':0.05,'ZC710':0.05,'ZC711':0.05,'ag1805':0.08,'al1805':0.1,'au1806':0.08,'bu1711':0.1,'jd1805':0.08,'i1805':0.05,'j1805':0.05,'jm1805':0.05,'l1805':0.05,'m1805':0.05,'p1805':0.05,'pp1805':0.05,'v1805':0.05,'y1805':0.05,'FG805':0.05,'JR805':0.05,'LR805':0.05,'MA805':0.07,'OI805':0.05,'PM805':0.05,'RI805':0.05,'RM805':0.05,'SF805':0.05,'SM805':0.05,'WH805':0.05,'ag1807':0.08,'SF803':0.05,'SM803':0.05,'WH803':0.05,'bb1804':0.2,'fb1804':0.2,'i1804':0.05,'j1804':0.05,'jm1804':0.05,'l1804':0.05,'p1804':0.05,'FG804':0.05,'pp1804':0.05,'v1804':0.05,'MA804':0.07,'SF804':0.05,'SM804':0.05,'sc1805':0.05,'ZC807':0.05,'SR901':0.05,'CF807':0.05,'TA807':0.05,'FG807':0.05,'JR807':0.05,'LR807':0.05,'MA807':0.07,'OI807':0.05,'PM807':0.05,'RI807':0.05,'RM807':0.05,'MA711':0.07,'OI711':0.05,'PM711':0.05,'RI711':0.05,'RM711':0.05,'RS711':0.05,'SF711':0.05,'SM711':0.05,'WH711':0.05,'a1805':0.05,'b1711':0.05,'bb1711':0.2,'c1711':0.05,'cs1711':0.05,'fb1711':0.2,'i1711':0.05,'j1711':0.05,'jd1711':0.08,'jm1711':0.05,'l1711':0.05,'m1711':0.05,'p1711':0.05,'pp1711':0.05,'v1711':0.05,'y1711':0.05,'FG711':0.05,'al1807':0.1,'au1808':0.08,'bu1801':0.1,'cu1807':0.09,'hc1807':0.1,'ni1807':0.1,'pb1807':0.1,'rb1807':0.1,'ru1807':0.1,'sn1807':0.09,'wr1807':0.2,'zn1807':0.1,'jd1806':0.08,'RS807':0.05,'SF807':0.05,'SM807':0.05,'WH807':0.05,'a1901':0.05,'b1807':0.05,'bb1807':0.2,'c1807':0.05,'cs1807':0.05,'fb1807':0.2,'i1807':0.05,'j1807':0.05,'jm1807':0.05,'l1807':0.05,'m1807':0.05,'p1807':0.05,'pp1807':0.05,'v1807':0.05,'y1807':0.05,'TA808':0.05,'bb1808':0.2,'fb1808':0.2,'i1808':0.05,'j1808':0.05,'jm1808':0.05,'l1808':0.05,'m1808':0.05,'p1808':0.05,'fu1710':0.2,'fu1712':0.2,'p1801':0.05,'pp1801':0.05,'v1801':0.05,'y1801':0.05,'FG801':0.05,'JR801':0.05,'LR801':0.05,'MA801':0.07,'OI801':0.05,'PM801':0.05,'RI801':0.05,'RM801':0.05,'SF801':0.05,'JR711':0.05,'LR711':0.05,'ZC712':0.05,'pp1808':0.05,'v1808':0.05,'y1808':0.05,'FG808':0.05,'MA808':0.07,'RM808':0.05,'RS808':0.05,'SF808':0.05,'SM808':0.05,'fu1801':0.2,'SM801':0.05,'WH801':0.05,'ag1801':0.08,'al1801':0.1,'au1802':0.08,'cu1801':0.09,'hc1801':0.1,'ni1801':0.1,'pb1801':0.1,'rb1801':0.1,'ru1801':0.1,'sn1801':0.09,'wr1801':0.2,'zn1801':0.1,'IC1710':0.3,'IH1710':0.2,'fu1805':0.2,'bu1806':0.1,'SR709':0.05,'TA806':0.05,'FG806':0.05,'MA806':0.07,'SF806':0.05,'SM806':0.05,'bb1806':0.2,'fb1806':0.2,'i1806':0.05,'j1806':0.05,'jm1806':0.05,'l1806':0.05,'p1806':0.05,'pp1806':0.05,'v1806':0.05,'fu1808':0.2,'a1709':0.05,'fu1809':0,'sc2009':0,'scefp':0})
unit = dict({'SR807':10,'CF709':5,'TA709':5,'SR811':10,'CF805':5,'SR805':10,'TA805':5,'TA712':5,'CF711':5,'TA711':5,'TA710':5,'TA804':5,'CF801':5,'TA801':5,'SR803':10,'bu1803':10,'SR711':10,'bu1712':10,'a1711':10,'jd1804':10,'fu1807':50,'sc1807':1000,'ag1802':15,'al1802':5,'cu1802':5,'hc1802':10,'ni1802':1,'pb1802':5,'rb1802':10,'sn1802':1,'wr1802':10,'zn1802':5,'fu1806':50,'ZC804':100,'ZC802':100,'T1803':10000,'TF1803':10000,'IF1710':300,'jd1808':10,'cu1805':5,'hc1805':10,'ni1805':1,'pb1805':5,'rb1805':10,'ru1805':10,'sn1805':1,'wr1805':10,'zn1805':5,'ZC805':100,'jd1807':10,'TA802':5,'FG802':20,'MA802':10,'SF802':5,'SM802':5,'bb1802':500,'fb1802':500,'i1802':100,'j1802':100,'jd1802':10,'jm1802':60,'l1802':5,'p1802':10,'pp1802':5,'v1802':5,'fu1803':50,'sc2006':1000,'ag1808':15,'al1808':5,'au1711':1000,'bu1802':10,'cu1808':5,'hc1808':10,'ni1808':1,'pb1808':5,'rb1808':10,'ru1808':10,'sn1808':1,'wr1808':10,'zn1808':5,'ag1804':15,'al1804':5,'bu1710':10,'cu1804':5,'hc1804':10,'ni1804':1,'pb1804':5,'rb1804':10,'ru1804':10,'sn1804':1,'wr1804':10,'zn1804':5,'IC1803':200,'IF1803':300,'IH1803':300,'ZC806':100,'sc1808':1000,'ZC808':100,'CY801':5,'CY802':5,'CY803':5,'CY804':5,'CY805':5,'CY806':5,'CY807':5,'CY808':5,'ag1806':15,'al1806':5,'au1709':1000,'bu1906':10,'cu1806':5,'hc1806':10,'ni1806':1,'pb1806':5,'rb1806':10,'ru1806':10,'sn1806':1,'wr1806':10,'zn1806':5,'ag1803':15,'al1803':5,'au1804':1000,'bu1903':10,'cu1803':5,'hc1803':10,'ni1803':1,'pb1803':5,'rb1803':10,'ru1803':10,'sn1803':1,'wr1803':10,'zn1803':5,'IC1712':200,'IF1712':300,'IH1712':300,'T1709':10000,'TF1709':10000,'SR801':10,'a1801':10,'ag1710':15,'al1710':5,'cu1710':5,'hc1710':10,'ni1710':1,'pb1710':5,'rb1710':10,'ru1710':10,'sn1710':1,'wr1710':10,'zn1710':5,'FG712':20,'MA712':10,'SF712':5,'SM712':5,'bb1712':500,'fb1712':500,'i1712':100,'j1712':100,'jd1712':10,'jm1712':60,'l1712':5,'m1712':10,'p1712':10,'pp1712':5,'v1712':5,'y1712':10,'ag1712':15,'al1712':5,'bu1812':10,'cu1712':5,'hc1712':10,'ni1712':1,'pb1712':5,'rb1712':10,'sn1712':1,'wr1712':10,'zn1712':5,'ag1711':15,'al1711':5,'au1712':1000,'cu1711':5,'hc1711':10,'ni1711':1,'pb1711':5,'rb1711':10,'ru1711':10,'sn1711':1,'wr1711':10,'zn1711':5,'fu1711':50,'a1803':10,'b1709':10,'bb1709':500,'c1709':10,'cs1709':10,'fb1709':500,'i1709':100,'j1709':100,'jd1709':10,'jm1709':60,'l1709':5,'m1709':10,'p1709':10,'pp1709':5,'v1709':5,'y1709':10,'FG709':20,'JR709':20,'LR709':20,'MA709':10,'OI709':10,'PM709':50,'RI709':20,'RM709':10,'RS709':10,'bu1709':10,'ZC801':100,'IC1709':200,'IF1709':300,'IH1709':300,'ag1709':15,'al1709':5,'au1710':1000,'bu1809':10,'cu1709':5,'hc1709':10,'ni1709':1,'pb1708':5,'pb1709':5,'rb1709':10,'ru1709':10,'sn1709':1,'wr1709':10,'zn1709':5,'SF709':5,'SM709':5,'WH709':20,'bb1710':500,'fb1710':500,'jd1803':10,'fu1804':50,'sc1710':1000,'sc1711':1000,'sc1712':1000,'sc1801':1000,'sc1802':1000,'sc1803':1000,'sc1804':1000,'sc1806':1000,'sc1809':1000,'sc1812':1000,'sc1903':1000,'sc1906':1000,'sc1909':1000,'sc1912':1000,'sc2003':1000,'a1811':10,'b1805':10,'bb1805':500,'c1805':10,'cs1805':10,'fb1805':500,'ZC803':100,'T1712':10000,'TF1712':10000,'CF803':5,'SR809':10,'TA803':5,'a1809':10,'b1803':10,'bb1803':500,'c1803':10,'cs1803':10,'fb1803':500,'i1803':100,'j1803':100,'jm1803':60,'l1803':5,'m1803':10,'p1803':10,'pp1803':5,'v1803':5,'y1803':10,'FG803':20,'JR803':20,'LR803':20,'MA803':10,'OI803':10,'PM803':50,'RI803':20,'RM803':10,'i1710':100,'j1710':100,'jd1710':10,'jm1710':60,'l1710':5,'p1710':10,'pp1710':5,'v1710':5,'FG710':20,'MA710':10,'SF710':5,'SM710':5,'a1807':10,'b1801':10,'bb1801':500,'c1801':10,'cs1801':10,'fb1801':500,'i1801':100,'j1801':100,'jd1801':10,'jm1801':60,'l1801':5,'m1801':10,'ZC709':100,'ZC710':100,'ZC711':100,'ag1805':15,'al1805':5,'au1806':1000,'bu1711':10,'jd1805':10,'i1805':100,'j1805':100,'jm1805':60,'l1805':5,'m1805':10,'p1805':10,'pp1805':5,'v1805':5,'y1805':10,'FG805':20,'JR805':20,'LR805':20,'MA805':10,'OI805':10,'PM805':50,'RI805':20,'RM805':10,'SF805':5,'SM805':5,'WH805':20,'ag1807':15,'SF803':5,'SM803':5,'WH803':20,'bb1804':500,'fb1804':500,'i1804':100,'j1804':100,'jm1804':60,'l1804':5,'p1804':10,'FG804':20,'pp1804':5,'v1804':5,'MA804':10,'SF804':5,'SM804':5,'sc1805':1000,'ZC807':100,'SR901':10,'CF807':5,'TA807':5,'FG807':20,'JR807':20,'LR807':20,'MA807':10,'OI807':10,'PM807':50,'RI807':20,'RM807':10,'MA711':10,'OI711':10,'PM711':50,'RI711':20,'RM711':10,'RS711':10,'SF711':5,'SM711':5,'WH711':20,'a1805':10,'b1711':10,'bb1711':500,'c1711':10,'cs1711':10,'fb1711':500,'i1711':100,'j1711':100,'jd1711':10,'jm1711':60,'l1711':5,'m1711':10,'p1711':10,'pp1711':5,'v1711':5,'y1711':10,'FG711':20,'al1807':5,'au1808':1000,'bu1801':10,'cu1807':5,'hc1807':10,'ni1807':1,'pb1807':5,'rb1807':10,'ru1807':10,'sn1807':1,'wr1807':10,'zn1807':5,'jd1806':10,'RS807':10,'SF807':5,'SM807':5,'WH807':20,'a1901':10,'b1807':10,'bb1807':500,'c1807':10,'cs1807':10,'fb1807':500,'i1807':100,'j1807':100,'jm1807':60,'l1807':5,'m1807':10,'p1807':10,'pp1807':5,'v1807':5,'y1807':10,'TA808':5,'bb1808':500,'fb1808':500,'i1808':100,'j1808':100,'jm1808':60,'l1808':5,'m1808':10,'p1808':10,'fu1710':50,'fu1712':50,'p1801':10,'pp1801':5,'v1801':5,'y1801':10,'FG801':20,'JR801':20,'LR801':20,'MA801':10,'OI801':10,'PM801':50,'RI801':20,'RM801':10,'SF801':5,'JR711':20,'LR711':20,'ZC712':100,'pp1808':5,'v1808':5,'y1808':10,'FG808':20,'MA808':10,'RM808':10,'RS808':10,'SF808':5,'SM808':5,'fu1801':50,'SM801':5,'WH801':20,'ag1801':15,'al1801':5,'au1802':1000,'cu1801':5,'hc1801':10,'ni1801':1,'pb1801':5,'rb1801':10,'ru1801':10,'sn1801':1,'wr1801':10,'zn1801':5,'IC1710':200,'IH1710':300,'fu1805':50,'bu1806':10,'SR709':10,'TA806':5,'FG806':20,'MA806':10,'SF806':5,'SM806':5,'bb1806':500,'fb1806':500,'i1806':100,'j1806':100,'jm1806':60,'l1806':5,'p1806':10,'pp1806':5,'v1806':5,'fu1808':50,'a1709':10,'fu1809':50,'sc2009':1000,'scefp':1000})

commitment = 0.0005


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
    ds = ds.sort_values(['trade_day', 'inst', 'date', 'time', 'action', 'dir'],
                        ascending = [True, True, True, True, False, False])

    #get all instruments
    instruments = ds['inst'].unique()
    #get all trade days
    trade_days = ds['trade_day'].unique()

    # set index
    ds.index.names = [None]
    ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return ds, instruments, trade_days


class position:
    day = 0         # the trade day
    inst = ''       # instrument name
    lvol = 0        # long position
    lprice = 0      # long position
    lmoney = 0.0    # long position
    lpercent = 0.0  # long position
    lrev = 0.0      # long position
    svol = 0        # short position
    sprice = 0      # short position
    smoney = 0.0    # short position
    spercent = 0.0  # short position
    srev = 0.0      # short position
    tmoney = 0.0    # total
    tpercent = 0.0  # total
    trev = 0.0      # total

    def __init__(self, day, inst):
        self.day = day
        self.inst = inst

    def set_to_prev_pos(self, prev_pos):
        self.lvol   = prev_pos.lvol
        self.lprice = prev_pos.lprice
        self.lmoney = prev_pos.lmoney
        self.svol   = prev_pos.svol
        self.sprice = prev_pos.sprice
        self.smoney = prev_pos.smoney
        self.tmoney = prev_pos.tmoney
        # do not set percent, calculate every day
        self.lpercent = self.spercent = self.tpercent = 0.0
        # and do not set revenue, calculate every day
        self.lrev = self.srev = self.trev = 0.0

    def to_dataframe(self):
        return pd.DataFrame(data=[[
            self.day     , self.inst    , self.lvol    , self.lprice  , self.lmoney  , self.lpercent,
            self.lrev    , self.svol    , self.sprice  , self.smoney  , self.spercent, self.srev    ,
            self.tmoney  , self.tpercent, self.trev]],
            columns = [
                'day', 'inst', 'lvol', 'lprice', 'lmoney', 'lpercent', 'lrev', 'svol', 'sprice',
                'smoney', 'spercent', 'srev', 'tmoney', 'tpercent', 'trev'])


class MVP:
    v = 0
    m = 0
    p = 0

def get_vol_money_from_group_(key, keys, gb):
    mvp = MVP()
    if (key in keys):
        g = gb.get_group(key)
        mvp.v, mvp.m = g[['volume', 'money']].sum()
        if mvp.v != 0:
            mvp.p = mvp.m / (mvp.v * g.iloc[0].unit * g.iloc[0].margin)
    return mvp

class InstPosition:
    ol = MVP()
    cl = MVP()
    os = MVP()
    cs = MVP()

    def show(self):
        print 'OL: ', self.ol.m, self.ol.v, self.ol.p
        print 'CL: ', self.cl.m, self.cl.v, self.cl.p
        print 'OS: ', self.os.m, self.os.v, self.os.p
        print 'CS: ', self.cs.m, self.cs.v, self.cs.p
        print



def get_all_position_(day, keys, gb, inst):
    inst_pos = InstPosition()
    key = (day, inst, 1, 1)  # open long position
    inst_pos.ol = get_vol_money_from_group_(key, keys, gb)
    key = (day, inst, -1, 1)  # close long position
    inst_pos.cl = get_vol_money_from_group_(key, keys, gb)
    key = (day, inst, 1, -1) # open short position
    inst_pos.os = get_vol_money_from_group_(key, keys, gb)
    key = (day, inst, -1, -1) # close long position
    inst_pos.cs = get_vol_money_from_group_(key, keys, gb)

    return inst_pos


def cal_vol_price_money_(i, inst, pos, ip, p, day):
    if ip.cl.v > ip.ol.v:
        # close yesterday position
        if (i == 0):
            print 'Error 1: long: ', inst, day, i
        else:
            # position of previous day
            pp = pos.iloc[i - 1][inst]
            ip.ol.v = pp.lvol - (ip.cl.v - ip.ol.v)
            if (ip.ol.v < 0):
                print 'Error 2: long: ', inst, day, i
            else:
                ip.ol.p = pp.lprice
                ip.ol.m = ip.ol.v * ip.ol.p * unit[inst] * long_margin[inst]
    else:
        # close today position
        if ip.ol.v > 0:
            # today have opend posion
            ip.ol.v = ip.ol.v - ip.cl.v
            ip.ol.m = ip.ol.v * ip.ol.p * unit[inst] * long_margin[inst]
            if i > 0:
                # position of previous day
                pp = pos.iloc[i - 1][inst]
                if (pp.lvol > 0):
                    ip.ol.v += pp.lvol
                    ip.ol.m += pp.lmoney
                    ip.ol.p = ip.ol.m / (ip.ol.v * unit[inst] * long_margin[inst])
        elif i > 0 and ip.ol.v == 0:
            # today did not open, get position of previous day
            pp = pos.iloc[i - 1][inst]
            ip.ol.v = pp.lvol
            ip.ol.m = pp.lmoney
            ip.ol.p = pp.lprice




    if ip.cs.v > ip.os.v:
        # csose yesterday position
        if (i == 0):
            print 'Error 3: Short: ', inst, day, i
        else:
            # position of previous day
            pp = pos.iloc[i - 1][inst]
            ip.os.v = pp.svol - (ip.cs.v - ip.os.v)
            if (ip.os.v < 0):
                print 'Error 4: Short: ', inst, day, i
            else:
                ip.os.p = pp.sprice
                ip.os.m = ip.os.v * ip.os.p * unit[inst] * long_margin[inst]
    else:
        # csose today position
        if ip.os.v > 0:
            # today have opend posion
            ip.os.v = ip.os.v - ip.cs.v
            ip.os.m = ip.os.v * ip.os.p * unit[inst] * long_margin[inst]
            if i > 0:
                # position of previous day
                pp = pos.iloc[i - 1][inst]
                if pp.svol > 0:
                    ip.os.v += pp.svol
                    ip.os.m += pp.smoney
                    ip.os.p = ip.os.m / (ip.os.v * unit[inst] * long_margin[inst])
        elif i > 0 and ip.os.v == 0:
            # today did not open, get position of previous day
            pp = pos.iloc[i - 1][inst]
            ip.os.v = pp.svol
            ip.os.m = pp.smoney
            ip.os.p = pp.sprice

    p.lvol = ip.ol.v
    p.lprice = ip.ol.p
    p.lmoney = ip.ol.m
    p.svol = ip.os.v
    p.sprice = ip.os.p
    p.smoney = ip.os.m
    p.tmoney = p.lmoney + p.smoney
    pos.iloc[i]['total_money'] += p.tmoney


def get_positions_(i, day, inst, gb, pos, keys):
    # add new position object to dataframe
    p = position(day, inst)
    pos.iloc[i][inst] = p

    inst_pos = get_all_position_(day, keys, gb, inst)
    cal_vol_price_money_(i, inst, pos, inst_pos, p, day)


def get_position_without_trade_(i, day, inst, pos):
    # add new position object to dataframe
    p = position(day, inst)
    pos.iloc[i][inst] = p
    if i > 0:
        # first row we do not anything, start from 2nd row
        p.set_to_prev_pos(pos.iloc[i - 1][inst])

    # sum the total_money of the day
    pos.iloc[i]['total_money'] += p.tmoney


def get_position_with_trade_(i, day, inst, day_df, gb, pos, keys):
    if (inst in day_df.index.get_level_values('inst')):
        get_positions_(i, day, inst, gb, pos, keys)
    else:
        # this instrument has no trade in the day
        get_position_without_trade_(i, day, inst, pos)


def get_percentage_(i, pos, instruments):
    tm = pos.iloc[i]['total_money']
    if int(tm) != 0:
        for inst in instruments:
            p = pos.iloc[i][inst]
            p.tpercent = p.tmoney / tm
            p.lpercent = p.lmoney / tm
            p.spercent = p.smoney / tm


def get_daily_position(ds, gb, pos, instruments):
    i = 0
    keys = gb.groups.keys()

    for day in trade_days:
        pos.iloc[i]['trade_day'] = day
        pos.iloc[i]['total_money'] = 0.0
        # loop for all day
        if day in ds.index.get_level_values('trade_day'):
            # has trade in the day
            day_df = ds.xs(day)
            #set total money to zero
            # loop for all instruments
            for inst in instruments:
                get_position_with_trade_(i, day, inst, day_df, gb, pos, keys)
        else:
            # no trade in the day
            for inst in instruments:
                get_position_without_trade_(i, day, inst, pos)

        get_percentage_(i, pos, instruments)
        # next day
        i += 1


def get_money(pos):
    for i in range(0, pos.shape[0]):
        for inst in instruments:
            money.iloc[i][inst] = pos.iloc[i][inst].tmoney
        money.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        money.iloc[i]['total_money'] = pos.iloc[i]['total_money']
    return money


def get_percent_vol(pos, trade_days):
    cols = np.append('L_' + instruments, 'S_' + instruments)
    days = list(range(0, len(trade_days)))
    m = pd.DataFrame(columns=np.append(cols, ['trade_day', 'total_money']), index=days)
    p = pd.DataFrame(columns=np.append(cols, 'trade_day'), index=days)
    v = pd.DataFrame(columns=np.append(cols, 'trade_day'), index=days)

    for i in range(0, pos.shape[0]):
        for inst in instruments:
            pp = pos.iloc[i][inst]
            p.iloc[i]['L_' + inst] = pp.lpercent
            p.iloc[i]['S_' + inst] = pp.spercent
            v.iloc[i]['L_' + inst] = pp.lvol
            v.iloc[i]['S_' + inst] = pp.svol
            m.iloc[i]['S_' + inst] = pp.smoney
            m.iloc[i]['L_' + inst] = pp.lmoney
        p.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        m.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        v.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        m.iloc[i]['total_money'] = pos.iloc[i]['total_money']
    return m, v, p


def draw_total_money_instrument(money):
    # show total money
    ax = money.total_money.plot(title='Deposit', figsize=(16, 9))
    ax.set_xlabel("Trade Days")
    ax.set_ylabel("Deposit")
    plt.savefig("/home/sean/tmp/analysis/deposit.png")
    #plt.show()
    plt.close(ax.get_figure())


def get_instrument_code(inst):
    match = re.match(r"([a-z]+)([0-9]+)", inst, re.I)
    if match:
        items = match.groups()
        return items[0]
    else:
        return ''


def get_all_instrument_code(instruments):
    inst_codes = set()
    for inst in instruments:
        inst_codes.add(get_instrument_code(inst))
    ic = np.array(list(inst_codes))
    ic = ic.astype(object)
    return ic


def init_mpv(trade_days, ic):
    cols = np.append('L_' + ic, 'S_' + ic)
    days = list(range(0, len(trade_days)))
    m = pd.DataFrame(columns=np.append(cols, ['trade_day', 'total_money']), index=days)
    p = pd.DataFrame(columns=np.append(cols, 'trade_day'), index=days)
    v = pd.DataFrame(columns=np.append(cols, 'trade_day'), index=days)
    for i in range(0, pos.shape[0]):
        for inst in instruments:
            code = get_instrument_code(inst)
            lc = 'L_' + code
            sc = 'S_' + code

            p.iloc[i][lc] = 0
            p.iloc[i][sc] = 0
            v.iloc[i][lc] = 0
            v.iloc[i][sc] = 0
            m.iloc[i][lc] = 0
            m.iloc[i][sc] = 0
    return m, v, p

def get_mvp(pos, instruments, m, v, p):
    for i in range(0, pos.shape[0]):
        for inst in instruments:
            code = get_instrument_code(inst)
            lc = 'L_' + code
            sc = 'S_' + code

            pp = pos.iloc[i][inst]
            p.iloc[i][lc] += pp.lpercent * 100
            p.iloc[i][sc] += pp.spercent * 100
            v.iloc[i][lc] += pp.lvol
            v.iloc[i][sc] += pp.svol
            m.iloc[i][lc] += pp.lmoney
            m.iloc[i][sc] += pp.smoney

        p.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        m.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        v.iloc[i]['trade_day'] = pos.iloc[i]['trade_day']
        m.iloc[i]['total_money'] = pos.iloc[i]['total_money']


def draw_line(df, inst_code, x, ax, label, trade_days):
    l = list(df['L_' + inst_code])
    s = list(df['S_' + inst_code])
    ax.set_xlim([min(x), max(x)])
    ax.set_ylim([min(min(s), min(l)), max(max(s), max(l)) * 1.01])
    ax.set_ylabel(label)
    # ax.set_xticklabels(trade_days)
    rects1 = ax.plot(x, l, 'r')
    rects2 = ax.plot(x, s, 'g')
    ax.legend((rects1[0], rects2[0]), ('Long', 'Short'))

def draw_mvp(m, v, p, inst_code, trade_days):
    x = list(range(0, len(trade_days)))
    f, axs = plt.subplots(3, 1, figsize=(10, 10))
    # f.suptitle(inst_code + '888', fontsize=14)
    f.canvas.set_window_title(inst_code + '888')

    draw_line(v, inst_code, x, axs[0], 'volume', trade_days)
    draw_line(p, inst_code, x, axs[1], 'percent', trade_days)
    draw_line(m, inst_code, x, axs[2], 'deposits', trade_days)

    plt.xlabel("trade day")
    f.tight_layout()
    plt.savefig("/home/sean/tmp/analysis/instrument/" + inst_code + ".png")
    # plt.show()
    plt.close(f)


def get_one_day_percent(i, codes, percent):
    lp = []
    sp = []
    for c in codes:
        lp.append(percent.iloc[i]['L_' + c])
        sp.append(percent.iloc[i]['S_' + c])
    return lp, sp

def draw_percent_diagram(trade_days, percent, ic):
    for i in range(0, len(trade_days)):
        lp, sp = get_one_day_percent(i, ic, percent)
        ind = np.arange(len(ic))  # the x locations for the groups
        width = 0.35  # the width of the bars
        fig, ax = plt.subplots(figsize=(16, 9))
        rects1 = ax.bar(ind, lp, width, color='r')
        rects2 = ax.bar(ind + width, sp, width, color='g')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Percent')
        ax.set_title('Percent @' + str(trade_days[i]))
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(list(ic))
        ax.legend((rects1[0], rects2[0]), ('Long', 'Short'))
        plt.savefig("/home/sean/tmp/analysis/trade-day/" + str(trade_days[i]) + ".png")
        plt.close(ax.get_figure())


if __name__ == '__main__':
    filepath = "/home/sean/Downloads/830-en.csv"
    ds, instruments, trade_days = get_data_source(filepath)
    dsgb = ds.groupby(['trade_day', 'inst', 'action', 'dir'])

    pos = pd.DataFrame(columns=np.append(instruments, ['trade_day', 'total_money']), index=trade_days)
    get_daily_position(ds, dsgb, pos, instruments)

    ic = get_all_instrument_code(instruments)
    money, volume, percent = init_mpv(trade_days, ic)
    get_mvp(pos, instruments, money, volume, percent)


    draw_total_money_instrument(money)

    # draw_mvp(money, volume, percent, 'CF', trade_days)
    for code in ic:
        draw_mvp(money, volume, percent, code, trade_days)

    draw_percent_diagram(trade_days, percent, ic)

'''
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    xs = np.arange(20)
    ys = np.random.rand(20)

    # You can provide either a single color or an array. To demonstrate this,
    # the first bar of each set will be colored cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
'''

'''
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt


N = 5
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, menMeans, width, color='#d62728', yerr=menStd)
p2 = plt.bar(ind, womenMeans, width,
             bottom=menMeans, yerr=womenStd)

plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 81, 10))
plt.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.show()
'''

def get_iv(filepath):
    iv = pd.read_csv(filepath)
    for i in np.arange(32):
        pp = pos.iloc[42][iv.iloc[i]['inst']]
        price = 0
        margin = 0
        u = unit[iv.iloc[i]['inst']]
        vol = iv.iloc[i]['volume']
        if iv.iloc[i]['dir'] > 0:
            price = pp.lprice
            margin = long_margin[iv.iloc[i]['inst']]
        else:
            price = pp.sprice
            margin = short_margin[iv.iloc[i]['inst']]

        iv.loc[i, 'price'] = price
        iv.loc[i, 'unit'] = u
        iv.loc[i, 'margin'] = margin
        iv.loc[i, 'deposit'] = price * vol * u * margin
    iv.loc[32, 'price'] = 26080
    iv.loc[32, 'unit'] = 5
    iv.loc[32, 'margin'] = 0.1
    iv.loc[32, 'deposit'] = 26080.000000  *   5.0  *  0.10
    return iv
iv = get_iv("/home/sean/Downloads/position-20170904-085939.csv")

# def get_my_real_money(mynony):
ivsum = iv.deposit.sum()
iv['percent'] = iv['deposit'].apply(lambda x: x / ivsum)
iv['code'] = iv['inst'].apply(lambda x: get_instrument_code(x))
ivgb = iv.groupby(['code', 'dir']).agg({'inst':'first','dir':'first', 'volume':'sum', 'price':'first', 'unit':'first',\
                                        'margin':'first', 'deposit':'sum', 'percent':'sum', 'code':'first'})
ivgb = ivgb.sort_values('percent', ascending=False)
ivgb.plot(kind='pie', x='code', y='percent', autopct='%1.1f%%')

def get_myvolume(mynoney):
    ivgb['my'] = ivgb['percent'].apply(lambda x: x * mynoney)
    def get_myvol(s):
        my = s['my']
        p = s['price']
        u = s['unit']
        m = s['margin']
        myvol = my / (p * u * m)
        return pd.Series(dict(myvol=myvol))

    ivgb['myvol'] = ivgb.apply(get_myvol, axis=1)
    ivgb['ivol'] = ivgb['myvol'].apply(lambda x: int(x))
    def get_vol(s):
        p = s['price']
        u = s['unit']
        m = s['margin']
        v = s['ivol']
        imy = p * u * m * v
        return pd.Series(dict(imy=imy))
    ivgb['imy'] = ivgb.apply(get_vol, axis=1)
    print mynoney - ivgb.imy.sum()
    ivgb.plot(kind='bar', y = 'ivol')
    plt.show()

mynoney = 500000
get_myvolume(mynoney)

def generate_margin_uni():
    LongMargin = dict()
    ShortMargin= dict()
    MUnit = dict()
    for key in list(long_margin.keys()):
        code = get_instrument_code(key)
        print key, code
        if code not in LongMargin:
            LongMargin[code] = long_margin[key]
            ShortMargin[code] = short_margin[key]
            MUnit[code] = unit[key]

    print LongMargin
    print ShortMargin
    print MUnit

