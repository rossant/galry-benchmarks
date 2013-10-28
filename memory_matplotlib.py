import matplotlib.pyplot as plt

def load(data):
    fig = plt.figure(figsize=(7.5, 7.5), dpi=80)
    ax = plt.subplot(111)
    ax.plot(data)
    fig.show()
    plt.close(fig)
