import pandas as pd

num_locations = 20
tabu_tenure = 6
tabu_list_size = 6
# num_neighbours = (num_locations)*(num_locations - 1)//2 # arithmetic progression formula
optimal = 1285
flows = pd.read_csv(r'./Flow.csv', header = None).values
distances = pd.read_csv(r'./Distance.csv', header = None).values