import numpy as np
import matplotlib.pyplot as plt
import pickle

n = 5
k = np.arange(2,n)
f = open("none_or_all_n="+str(n)+".pkl", 'rb')
[true_percentage,startingBit_average] = pickle.load(f)
f.close()

print("true_percentage:", true_percentage)
print("startingBit_average:", startingBit_average)

fig = plt.figure("n="+str(n))
ax = fig.add_subplot(111)

label1 = 'starting bit'
label2 = 'true percentage'
data1 = ax.plot(k, startingBit_average, marker='o', markersize=5, color='b', linewidth=2, label = label1)
ax2 = ax.twinx()
data2 = ax2.plot(k, true_percentage, marker='o', markersize=5, color='r', linewidth=2, label = label2)

# added these three lines
lns = data1 + data2
labs = [l.get_label() for l in lns]

ax.grid()
ax.set_xlabel("k")
ax.set_ylabel("starting bit average", color='b')
ax2.set_ylabel("true instances percentage (%)", color="r")

plt.xticks(np.arange(min(k), max(k)+1, 1.0))
ax.set_yticks(np.arange(0, max(k), 1.0))
ax2.set_yticks(np.arange(0, 110, 10))

plt.title("n = " + str(n))
ax.legend(lns, labs, bbox_to_anchor=(1.1, 1.0), loc='upper left')
plt.tight_layout()
plt.show()
