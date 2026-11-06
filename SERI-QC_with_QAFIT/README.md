                                         SERI-QC SOFTWARE VERSION 1.1.0: 
                           Automated Irradiance Data Quality Assessment Tool Package

Data quality assessment for irradiance measurement is a method by which particular errors of irradiance data can be detected by automatic screening algorithms. One of these algorithms is SERI-QC. The original SERI-QC software package which was written in the C programming language, was developed by the Solar Energy Research Institute (SERI) now the National Renewable Energy Laboratory (NREL) to address the need for performing quality assessment on large sets of irradiance measurement (Maxwell et al. 1993). NREL also applied subsequent visual changes to the software by including color-coded plots of SERI QC flags (Wilcox, 1996). The original SERI QC and associated programs are available from https://www.osti.gov/biblio/1231498-seri-qc-solar-data-quality-assessment-software. The original package also includes a companion program, QCFIT, which is a standalone Windows application that provides support files for the SERI QC function (data quality boundaries). The QCFIT software can also be used as an analytical tool for visualizing solar data quality independent of the SERI QC function.
The new version 1.1.0 is written in Python programming language by NREL and contains SERI-QC and QCFIT software. Further, this new version compared to the original package, contains few changes which are detailed below.

About QCFIT:

QCFIT is a stand-alone utility to assist users of SERI QC in selecting Ktmax and Knmax limits and Gompertz boundaries that define the limits of expected solar irradiance data for a solar monitoring site. By examining subsets of a site's historical solar data, best-fit limits and Gompertz boundaries can be selected for each of the three SERI QC air mass ranges associated within a station data (Maxwell, 1993). The data output by QCFIT is required by the SERI-QC to assess global, direct, and diffuse irradiance data.
QCFIT displays a Kt versus Kn scatter plot of the data and provides several options for fitting predefined curve shapes to the plot. If no limits have been defined, QCFIT automatically makes an initial fit. The user may adjust the automatic fit or use other boundaries based on experience and known attributes of the data.

Advanced features:
- data formatting is not required for input file (illustrated in instruction manual.) 
- included elevation as a parameter while creating a new QA0 file
- covers extra points with Kt and Kn >=0
- displays the points those fails by 3-component filtering 
- data point list saved as *.csv and *.txt

About SERI-QC:

SERI-QC is a mathematical software package that assesses the quality of solar radiation data. Flags are set to inform the user of any departure of the data from expected values. These flags indicate the magnitude and direction of such departures. Flags only indicate that data do or do not fall within expected ranges. This does not mean that the data are or are not valid. Check Maxwell, 1993 for description of flags.

Advanced features:
- data formatting is not required for input file (illustrated in instruction manual.)
- provides UI based selection (no programing experience required)
- gives a color-coded cylinder plot of all the flags
- gives a *.csv file with all the calculations happened during the QC process

References:

• Maxwell, E., Wilcox, S., Rymes, M., 1993. Users Manual for SERI QC Software: Assessing the Quality of Solar Radiation Data: Nrel/tp-463-5608 de93018210. http://www.nrel.gov/docs/legosti/old/5608.pdf.

• Wilcox, S., A Visual Quality Assessment Tool for Solar Radiation Data, Proceedings of the 1996 Annual Conference of the American Solar Energy Society, Boulder, Colorado, April 1996

• Wilcox, S.M., McCormack, P., 2011. Implementing Best Practices for Data Quality Assessment of the National Renewable Energy Laboratory’s Solar Resource and Meteorological Assessment Project.

• Reda, I.; Andreas, A. (2003). Solar Position Algorithm for Solar Radiation Applications. 55 pp.; NREL Report No. TP-560-34302, Revised January 2008.PDF

• solar position package - https://github.nrel.gov/PXS/nsrdb/tree/master/nsrdb/solar_position
