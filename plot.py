import matplotlib.pyplot as plt

# Draw client points based on their x, y axis values
def draw_initial_state(depot, clients):
  # draw clients
  x_list = []
  y_list = []
  for client in clients:
    x_list.append(client._pos._x)
    y_list.append(client._pos._y)
  plt.scatter(x_list, y_list, s=10)

  # draw depot
  plt.scatter(depot._x, depot._y, s=10)

  # Set chart title.
  plt.title("Initial state", fontsize=19)
  
  # Display the plot in the matplotlib's viewer
  plt.show()
