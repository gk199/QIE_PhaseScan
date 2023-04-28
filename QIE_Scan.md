# QIE Scan

## Scan plan

### Global scan
1. Update TDC LUT and uMNio word via CfgGit snippet (on hcalmon). Example [CfgGit](http://hcalmon.cms/cgit/HcalCfg/commit/?id=69a7e58fa4f8e4578dc431302fbdcff112938297)
2. RR to reconfigure and pick up new TDC LUT
3. Start scan, each point for 720 seconds (12 mins). Should be done from hcalngccm03 from a tmux session
	For April run, 
	```
	python scan_fine.py --seconds 600 --cycles -1 --hb --he --logfile AprilQIEscan.txt | tee output_global_april.txt 
	```
4. Revert TDC LUT and uMNio word via snippet update. Example [CfgGit](http://hcalmon.cms/cgit/HcalCfg/commit/?id=9162d0bdc5d5474bd9693e99fe03e6b62fbe083c)
5. RR to reconfigure
6. Check TDC LUT, uMNio word, and QIE phases are reverted (on hcalngccm03)
7. Copy files to HCAL DPG EOS space. JetMET dataset, RAW data is needed. 

### Local testing
1. Baseline LED run (multipartition) for comparison
2. Update TDC LUT and uMNio words via CfgGit snippet (on hcalmon)
3. Reconfigure and pick up new TDC LUT - just `reset` and `configure` when we are in local
4. Start a long LED run (20000 events) with a multipartition run from hcalngccm03
	```
	python scan_fine.py --seconds 20 --hb --logfile NovQIEscan_local.txt
	python scan_fine.py --seconds 60 --hb --logfile FebQIEscan_local.txt
	```
	Note the run number. Check ngFEC (TDC LUTs, QIE delays) and uMNioTool (additional user word).
5. Revert TDC LUT and uMNio word before returning to global
6. Reconfigure, check TDC LUT updated, QIE phases, and uMNio words (on hcalngccm03)
7. Check plots in low level DQM, process root files for analysis

### Testing script
```
python scan_fine.py --test-mode --seconds 5 --logfile scan_log_test.txt
```
For testing, to check that script runs ok and accesses needed .txt files.

Time to sleep between steps is set in `fec_jm_fine.py` in L98 as `sleep(10)` meaning to sleep for 10 seconds. Increased for the actual scan to 20 after seeing during the local test that one point was skipped. Tested during local 14 November.

## TDC LUT update
TDC LUT update is done via snippet, from hcalmon: [CfgGit instructions](https://twiki.cern.ch/twiki/bin/view/CMS/HcalCfgGit). TDC LUTs are specified in `HcalCfg/RBX/ngSettings.cfg`, line 96.
```
# TDCLUTOverride = "xmlfile:///nfshome0/pparygin/settings/HBTDCLUT_prompt_delayed_10Oct2022_P5.xml"                                                                         
TDCLUTOverride = "xmlfile:///nfshome0/gkopp/QIEscan/HBTDCLUT_prompt_delayed_9Nov2022_Flat12_P5.xml"
```

QIE delays can also be changed here (though I plan to just do this via the scan script):
```
# DelayOverride = "xmlfile://nfshome0/pparygin/settings/HBHEHF_phases/HB_upd_collisions2022.xml"
DelayOverride = "xmlfile://nfshome0/gkopp/QIEscan/HB_QIEscanSetting_collisions2022.xml"
```

## Update uMNio user words
```
UserDataQieDelay = true
```
on L54 of `HcalCfg/Master/global.xml`.

# Monitoring during the scan
Multiple windows open: 1 on hcalmon to change snippets, 2 in hcalngccm03 for checking ngFEC and uMNioTool, 1 in hcalngccm03 to run the scan. Have monitoring information from HCAL shifter page open as well. 

OMS plot to check timing changes [Timing vs. Lumisection](https://cmsweb.cern.ch/dqm/online/start?runnr=365983;dataset=/Global/Online/ALL;sampletype=online_data;filter=all;referencepos=overlay;referenceshow=customise;referencenorm=True;referenceobj1=refobj;referenceobj2=none;referenceobj3=none;referenceobj4=none;search=;striptype=object;stripruns=;stripaxis=run;stripomit=none;workspace=HCAL;size=M;root=Hcal/DigiTask/TimingvsLS/SubdetPM;focus=;zoom=no;).

## Check QIE phase delay and TDC LUTs
```
ssh hcalngccm03
ngFEC.exe -p 64400
get HBM10-1-QIE[1-64]_PhaseDelay
get HBM06-1-Qie[1-64]_TDCLUT
<this shows QIE delays in hex>
quit

ssh hcalngccm02
ngFEC.exe -p 64000
get HEM10-1-QIE[1-48]_PhaseDelay
<this shows QIE delays in hex>
quit
```

## Check uMNio for user words
```
ssh hcalngccm03
uMNioTool.exe hcal-uhtr-38-12 -o bridge-ho
DAQ
USER
DUMP
<this shows the words, a second line will appear when additional user words enabled>
Ctrl-C if need to quit out safely 
``` 

[twiki](https://twiki.cern.ch/twiki/bin/view/CMS/HcalDaqOnCallHowTo). This links to the most recent DAQ on call slides. 

## Check low level DQM (local run)
HBTrend -> HBTvsEvt to see avgTS vs Event plot for the LED run.

# General notes
Best to run in tmux session to avoid disconnect / dropping connection

Elog: Aug scan [elog](http://cmsonline.cern.ch/cms-elog/1150378), Aug test [elog](http://cmsonline.cern.ch/cms-elog/1150050).

Post and elog after the run.
Elog: Nov test [elog](http://cmsonline.cern.ch/cms-elog/1166125), Nov scan [elog](http://cmsonline.cern.ch/cms-elog/1167101). 

Elog: Feb LED scan [elog](http://cmsonline.cern.ch/cms-elog/1172774).

Elog: April local LED test [elog](http://cmsonline.cern.ch/cms-elog/1179928).

Notes from the scan are also at `/nfshome0/gkopp/QIEscan/Monitoring_QIEscan.txt`.

Confirm that nominal phases are reverted to.

## Locations
`/nfshome0/gkopp/QIEscan`