import matplotlib.pyplot as plt
import pandas as pd

colors = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'black']

n = 5
df = pd.read_pickle("n=" + str(n) + ".pkl")
print(df)

# multiple line plots
for i in range(2, n):
    label = "l=" + str(i)
    column = "l" + str(i)
    plt.plot('k', column, data=df, marker='o', markersize=10,
             color=colors[i - 2], linewidth=2, label=label)

plt.title("n = " + str(n))
plt.xlabel('k')
plt.ylabel('starting bit')
plt.legend()
plt.show()
