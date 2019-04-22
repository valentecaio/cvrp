import matplotlib.pyplot as plt
from datetime import datetime

# save plot result as png in ./results/
def save_plot():
  filename = 'results/' + str(datetime.now()).replace(' ', '_') + '.png'
  plt.savefig(filename, bbox_inches='tight')

# plot a line between two points
def draw_line(x1, y1, x2, y2):
  x_values = [x1, x2]
  y_values = [y1, y2]

  # plot the number in the list and set the line thickness.
  plt.plot(x_values, y_values, linewidth=3)

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
  
  save_plot()
  plt.show()

def draw_results(depot, clients, results):
  # Set chart title.
  plt.title("Final state", fontsize=19)

  # draw clients
  x_list = []
  y_list = []
  for client in clients:
    x_list.append(client.x)
    y_list.append(client.y)
  plt.scatter(x_list, y_list, s=10)

  # draw depot
  plt.scatter(depot.x, depot.y, s=10)

  # draw truck lines
#   for truck in results['trucks']:
#     p1 = depot
#     while len(truck.route) > 0:
#       p2 = clients[int(truck.route[0])]
#       draw_line(p1.x, p1.y, p2.x, p2.y)
#       p1 = p2
#       truck.route = truck.route[1:]

  plt.show()

if __name__ == "__main__":
  draw_line(1, 1, 2, 3)
  plt.show()
  