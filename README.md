# QIE_PhaseScan

Outline of the timing adjustment workflow, with needed scripts specified:

1. Determine adjustments needed to the QIE phases relative to some nominal phases. Save these in a file of the form ``corr_pdb_collisions2022_postNovScanEdits_gausFits_TS3_relativeToOct.txt``, which is read into the timing adjustment code. 

2. Use ``HB_timing_2022.py`` to generate the new set of adjusted QIE phases. This needs to read the files ``HB_upd_collisions2022.xml`` (reference phases), ``corr_pdb_collisions2022_postNovScanEdits_gausFits_TS3_relativeToOct.txt`` (phase adjustments), and ``Lmap_ngHB_N_20200212.txt`` for the HCAL positioning.

3. An output xml file is made with the new phases.

4. Create the QIE phase files for each scan point with ``generate_delays.py``. Copy all these files to the directory on ``nfshome0`` where the scan will be run from and ensure they have sensible names. These are txt files with the new phases listed that are read in with the QIE phase scan scripts.

5. TDC LUT adjustments are made with the script ``IGLOO2_xml_creator_LUT_TDCcoding_9Nov_Flat.py`` and uploaded. This script sets ''flat'' LUTs, i.e., they are not position dependent. An example of a position dependent LUT script is in ``IGLOO2_xml_creator_LUT_TDCcoding_v2.py``. Note that the position dependent script may need some edge-case handling implemented for `t_p2` (already done in flat LUT generator script).

6. Scan script details are in the QIE phase scan README, and the code I used to run is on cmsusr under ``/nfshome0/gkopp/QIEscan``. Some of these files are also in the [hcaltools GitLab repo](https://gitlab.cern.ch/cmshcal/hcaltools/-/tree/master/timingTune), though the May scan required updated versions (to run HB and HE together, for instance). I adapted my code from Pasha's scripts in ``/nfshome0/pparygin/hcaltools/``, and made updates, such as running HB and HE scans in parallel. I recommend we consolidate these scripts and upate the hcaltools repo with the new scripts. 

## 2025 Phase Scan
[Heewon's GitHub](https://github.com/heewob/2025-QIE-PhaseScan) has the improved setup scripts and documentation for the 2025 phase scan. The adjustments made are some ''safety'' selections in the scan scripts to exit the scan if the delay files are not found in the correct directory. 

Nominal phases that the 2025 phase scan is run around are from the 9 May update at the [HCAL DPG](https://indico.cern.ch/event/1545910/#3-phase-scan-studies) meeting. HB is based on a 4 GeV ET cut, while HE is based on a 8 GeV E cut. 