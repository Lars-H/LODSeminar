#Defining the properties

#Prefixes

#wbIndicatorPrefix = "http://worldbank.270a.info/dataset/"
wbIndicatorPrefix = "wb:";

#Indicators
nationalIncome = wbIndicatorPrefix + "NY.ADJ.NNTY.CD"
nationalSavings = wbIndicatorPrefix + "NY.ADJ.NNAT.CD"
weaponExports = wbIndicatorPrefix + "MS.MIL.XPRT.KD"
weaponImports = wbIndicatorPrefix + "MS.MIL.MPRT.KD"
foreignDirectInvestment = wbIndicatorPrefix + "BN.KLT.DINV.CD"
BPI = wbIndicatorPrefix + "NY.GDP.MKTP.CD"
BPIPerCapita = wbIndicatorPrefix + "NY.GDP.PCAP.CD"
governmentHealthExpediturePerCapita = wbIndicatorPrefix + "SH.XPD.PCAP.GX"
minimumWage19yearOld = wbIndicatorPrefix + "DB_mw_19apprentice"
wbIndicators = [nationalIncome, nationalSavings, weaponExports, weaponImports, foreignDirectInvestment, BPI, BPIPerCapita, governmentHealthExpediturePerCapita, minimumWage19yearOld]

#Used years
wbAllowedYears = ["2008", "2009", "2010", "2011", "2012"]
