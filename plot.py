import matplotlib.pyplot as plt
from datetime import datetime

# save plot result as png in ./results/
def save_plot():
  filename = 'results/' + str(datetime.now()).replace(' ', '_') + '.png'
  plt.savefig(filename, bbox_inches='tight')

# plot a line between two points
def draw_line(x1, y1, x2, y2, color):
  x_values = [x1, x2]
  y_values = [y1, y2]

  # plot the number in the list and set the line thickness.
  plt.plot(x_values, y_values, linewidth=3, color=color)

# draw client points based on their x, y axis values
def draw_initial_state(nodes):
  depot = nodes[0]
  clients = nodes[1:]

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

def draw_results(nodes, route):
  # Set chart title.
  plt.title("Final state", fontsize=19)

  depot = nodes[0]
  clients = nodes[1:]

  # draw clients
  x_list = []
  y_list = []
  for client in clients:
    x_list.append(client.x)
    y_list.append(client.y)
  plt.scatter(x_list, y_list, s=50, color='g')

  # draw depot
  plt.scatter(depot.x, depot.y, s=50, color='r')

  # draw route lines
  # colors = ['b', 'g', 'r', 'c', 'm', 'y', 'b']
  # color = colors[i%len(colors)]
  p1 = depot
  for node_id in route:
    p2 = nodes[node_id]
    draw_line(p1.x, p1.y, p2.x, p2.y, 'b')
    p1 = p2

  plt.show()


if __name__ == "__main__":
  draw_line(1, 1, 2, 3, 'b')
  plt.show()
  