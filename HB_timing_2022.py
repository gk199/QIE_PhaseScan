#!/usr/bin/python

from xml.dom import minidom
from xml.etree.ElementTree import ElementTree, dump
from datetime import date

today = date.today().strftime('%Y-%m-%d')

mapka = {}
corrs = {}

def read_map():
    with open("../Lmap_ngHB_N_20200212.txt") as f:
        next(f)
        for line in f:
            l = line.split()
            geo = [int(l[0])*int(l[1]), int(l[2]), int(l[4])]
            ele = l[6] + l[12] + str((int(l[10])-1)*16 + int(l[11])) #RBX + RM + qiech
            mapka[ele] = geo

            
def read_corr():
    #with open("corr_pdb_collisions2022.txt") as f: # my file is given in QIE delays, not ns. This is adjustments used for November 15 scan
    #with open("corr_pdb_collisions2022_postNovScanEdits.txt") as f: # my file in QIE delays, this is adjustments after November 15 scan
    #with open("corr_pdb_collisions2022_postNovScanEdits_gausFits_TS3.txt") as f: # my file in QIE delays, this is adjustments after November 15 scan from Gaussian fits, relative to Nov 0ns point
    with open("corr_pdb_collisions2022_postNovScanEdits_gausFits_TS3_relativeToOct.txt") as f: # my file in QIE delays, this is adjustments after November 15 scan from Gaussian fits, relative to Oct phases
    #with open("corr_pdb_collisions2022_postNovScanEdits_LEDscan.txt") as f: # my file in QIE delays, this is adjustments after November 15 scan, specifically for aligning LED data to "look like" collisions
        next(f)
        for line in f:
            l = line.split()
            for i in range (1,5):
                ed = l[0] + " " + str(i)
                corrs[ed] = float(l[i])

tree = ElementTree()
tree.parse('HB_upd_collisions2022.xml') # QIE phase settings used in early 2022 run, from June - mid November. Nov scan adjustments are relative to this
#tree.parse('HB_QIEscanSetting_collisions2022.xml') # this is adjusted QIE phases used for November 15 scan, new adjustments after that scan are relative to this file (use this both for collisions adjustments and LED adjustments)
root = tree.getroot()

def loop():
    for sector in root.iter('CFGBrick'):
        sec = sector[3].text
        for delay in sector.iter('Data'):
            if delay.attrib['rm'] == '5':
                pass
            else:
                chan = sec + delay.attrib['rm'] + delay.attrib['qie'] 
                geom = mapka[chan]
                ed = str(geom[0]) + " " + str(geom[2])
                newdel = 64 if "-999" in ed else int(delay.text)+int(round(corrs[ed])) # round(corrs[ed] / 0.5 if file given in ns
                if newdel>113 or newdel<64: print (newdel)
                delay.text = str(newdel)
    
    #tree.write('HB_QIEscanSetting_collisions2022.xml') # for November 15 Scan
    #tree.write('HB_QIEscanSetting_collisions2023_postNovScanEdits_'+today+'.xml') # for adjustments made after analyzing november QIE scan 
    #tree.write('HB_QIEscanSetting_collisions2023_postNovScanEdits_gausFit_TS3_'+today+'.xml') # for adjustments made after analyzing november QIE scan 
    tree.write('HB_QIEscanSetting_collisions2023_postNovScanEdits_gausFit_TS3_relativeToOct_'+today+'.xml') # for adjustments made after analyzing november QIE scan 
    #tree.write('HB_QIEscanSetting_collisions2023_postNovScanEdits_LEDscan_'+today+'.xml') # for adjustments made after analyzing november QIE scan 

def main():
    read_map()
    read_corr()
    loop()

    
if __name__ == "__main__":
    main()
