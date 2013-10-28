import galry.pyplot as plt

def load(data):
    fig = plt.figure(figsize=(600, 600), autodestruct=100)
    fig.plot(data.T)
    plt.show()
