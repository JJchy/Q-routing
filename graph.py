import matplotlib.pyplot as plt

line2, caps2, bars2 = plt.errorbar(
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # X
    [9.84,9.67,9.89, 9.51, 10.2, 9.80, 9.33, 10.2, 9.47], # Y
    yerr=[0.914, 1.09, 1.33, 1.17, 0.639, 1.32, 1.08, 0.935, 1.36],     # Y-errors
    fmt="b.-", # format line like for plot()
    linewidth=2,	# width of plot line
    elinewidth=2,# width of error bar line
    ecolor='k',    # color of error bar
    capsize=4,     # cap length for error bar
    capthick=2   # cap thickness for error bar
    )
plt.setp(line2,label="Q-routing")#give label to returned line
plt.legend(numpoints=1,             #Set the number of markers in label
           loc=('upper left'))      #Set label location

line, caps, bars = plt.errorbar(
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # X
    [4.57,4.76,5.42,4.56, 4.76, 5.27, 4.43, 4.77, 6.54], # Y
    yerr=[0.786, 1.25, 1.42, 1.08, 1.28, 1.17, 0.758, 1.53, 2.93],     # Y-errors
    fmt="r.-", # format line like for plot()
    linewidth=2,	# width of plot line
    elinewidth=2,# width of error bar line
    ecolor='k',    # color of error bar
    capsize=4,     # cap length for error bar
    capthick=2   # cap thickness for error bar
    )
plt.setp(line,label="Q$^2$-routing")#give label to returned line
plt.legend(numpoints=1,             #Set the number of markers in label
           loc=('upper left'))      #Set label location


"""
line2, caps2, bars2 = plt.errorbar(
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # X
    [9.86,9.68,9.89,9.46, 10.3, 9.86, 9.49, 10.2, 9.44], # Y
    yerr=[0.905, 1.07, 1.30, 1.18, 0.614, 1.42, 1.00, 0.986, 1.48],     # Y-errors
    fmt="b.-", # format line like for plot()
    linewidth=2,	# width of plot line
    elinewidth=2,# width of error bar line
    ecolor='k',    # color of error bar
    capsize=4,     # cap length for error bar
    capthick=2   # cap thickness for error bar
    )
plt.setp(line2,label="Q-routing")#give label to returned line
plt.legend(numpoints=1,             #Set the number of markers in label
           loc=('upper left'))      #Set label location

line, caps, bars = plt.errorbar(
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # X
    [3.87,3.50,3.28,2.83, 2.76, 2.86, 2.76, 2.77, 3.09], # Y
    yerr=[0.667, 0.660, 0.446, 0.416, 0.324, 0.395, 0.352, 0.436, 0.457],     # Y-errors
    fmt="r.-", # format line like for plot()
    linewidth=2,	# width of plot line
    elinewidth=2,# width of error bar line
    ecolor='k',    # color of error bar
    capsize=4,     # cap length for error bar
    capthick=2   # cap thickness for error bar
    )
plt.setp(line,label="Q$^2$-routing")#give label to returned line
plt.legend(numpoints=1,             #Set the number of markers in label
           loc=('upper left'))      #Set label location
"""

plt.xlim((0, 1))                 #Set X-axis limits
plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], fontsize=12)               #get only ticks we want
plt.yticks([0, 2, 4, 6, 8, 10, 12, 14], fontsize=12)
plt.xlabel ('ratio of high priority packet', fontsize=12)
plt.ylabel ('average delay', fontsize=12)
plt.grid(linestyle = ':')
plt.show()