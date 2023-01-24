import matplotlib.pyplot as plt

def f1():
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.plot([0,1,2], [10,20,3])
    fig.legend()
    fig.savefig('to.png')   # save the figure to file
    plt.close(fig)    # close the figure window

def f2():
    plt.plot([0,1,2], [10,20,3])
    plt.savefig('to.png')   # save the figure to file
    

f1()