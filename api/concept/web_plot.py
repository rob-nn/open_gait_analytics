import matplotlib.pyplot as plt, mpld3

fig = plt.figure()
plt.plot([3, 1, 4, 1, 5])
plt.show()
str = mpld3.fig_to_html(fig)

f = open('test.html', 'w')
f.write(str)
f.close()
print str
plt.show()
