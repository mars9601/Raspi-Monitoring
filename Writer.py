from collections import deque
from matplotlib import lines
import matplotlib.pyplot as plt
import csv


import pandas as pd
df = pd.read_csv("plot.csv")
saved_column = df.CPU

print(saved_column)

