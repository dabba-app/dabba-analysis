import math
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np

loc = np.array

# euclidean dist calc
def distance(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return dist

# dist callback
class CreateDistanceCallback(object):

  def __init__(self):
    locations = loc
    size = len(locations)
    self.matrix = {}

    for from_node in xrange(size):
      self.matrix[from_node] = {}
      for to_node in xrange(size):
        if from_node == to_node:
          self.matrix[from_node][to_node] = 0
        else:
          x1 = locations[from_node][0]
          y1 = locations[from_node][1]
          x2 = locations[to_node][0]
          y2 = locations[to_node][1]
          self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

  def Distance(self, from_node, to_node):
    return int(self.matrix[from_node][to_node])

def runTsp(locn):
  link = ""
  locations = locn
  global loc
  loc = locn
  tsp_size = len(locations)
  print(tsp_size)
  num_routes = 1 # 1 for TSP
  # Nodes are indexed from 0 to tsp_size - 1. The depot is the starting node of the route.
  depot = 0
  # Create routing model.
  if tsp_size > 0:
    routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    dist_between_locations = CreateDistanceCallback()
    dist_callback = dist_between_locations.Distance
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve, returns a solution if any.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
      # Solution cost.
      print "Total distance: " + str(assignment.ObjectiveValue()) + "\n"
      # Only 1 route here; else we iterate from 0 to routing.vehicles() - 1.
      route_number = 0
      node = routing.Start(route_number)
      route = ''
      link = "https://www.google.com/maps/dir/?api=1&origin="
      link += str(loc[0][0])
      link += ","
      link += str(loc[0][1])
      link += "&destination="
      link += str(loc[0][0])
      link += ","
      link += str(loc[0][1])
      link += "&waypoints="
      while not routing.IsEnd(node):
        route += str(node) + ' -> '
        link += str(loc[node][0])
        link += ","
        link += str(loc[node][1])
        node = assignment.Value(routing.NextVar(node))
        if not routing.IsEnd(node):
          link += "|"
      print(link)
      route += '0'
      print "Route:\n\n" + route
    else:
      print 'No solution found.'
  else:
    print 'Specify an instance greater than 0.'
  return link