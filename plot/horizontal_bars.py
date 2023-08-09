import matplotlib.pyplot as plt

never = [74]
seldom = [18]
undecided = [8]

y = [0]

plt.barh(y, never, color="#b5ffb9", edgecolor="white")
plt.barh(y, seldom, left=never, color="#f9bc86", edgecolor="white")
plt.barh(y, undecided, left=[100 - i for i in undecided], color="#a3acff", edgecolor="white")

plt.show()
