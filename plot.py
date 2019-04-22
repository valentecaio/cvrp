import matplotlib.pyplot as plt
from datetime import datetime

# save plot result as png in ./results/
def save_plot():
  filename = 'results/' + str(datetime.now()).replace(' ', '_') + '.png'
  plt.savefig(filename, bbox_inches='tight')

# draw client points based on their x, y axis values
def draw_initial_state(depot, clients):
  # draw clients
  x_list = []
  y_list = []
  for client in clients:
    x_list.append(client.x)
    y_list.append(client.y)
  plt.scatter(x_list, y_list, s=10)

  # draw depot
  plt.scatter(depot.x, depot.y, s=10)

  # Set chart title.
  plt.title("Initial state", fontsize=19)
  
  # save plot result as png in ./results/
  filename = 'results/' + str(datetime.now()).replace(' ', '_') + '.png'
  plt.savefig(filename, bbox_inches='tight')

  # display the plot in the matplotlib's viewer
  plt.show()
