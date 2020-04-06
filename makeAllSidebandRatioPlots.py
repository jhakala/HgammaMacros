from sidebandRatioPlot import makeRatioPlots

sidebands = []
for i in range(0, 11):
  lowerBound = 10*i+20
  upperBound = 10*i+50
  sidebands.append([lowerBound, upperBound])


#for i in range(0, 10):
#  makeRatioPlots([sidebands[i], sidebands[i+1]])

rebin = 50
makeRatioPlots([[50., 70.], [100., 110.]], rebin)
makeRatioPlots([[100., 110.], [110., 140.]], rebin)
