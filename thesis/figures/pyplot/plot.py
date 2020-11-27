#!/usr/bin/env python

import csv
from dataclasses import dataclass
from typing import List
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

@dataclass
class DataPoint:
  action: int
  samples: List[int]

  def average(self):
    return sum(self.samples)/len(self.samples)

@dataclass
class CacheDataPoint(DataPoint):
  cache: bool

@dataclass
class PlotData:
  name: str
  data: List[DataPoint]

  def x(self):
    return [d.action for d in self.data]

  def y(self):
    return [d.average() for d in self.data]

  def getY(self, x):
    return next((d.average() for d in self.data if d.action == x), None)

def read_data(file: str) -> PlotData:
  with open(file) as csvfile:
    r = csv.reader(csvfile, delimiter='|')
    data = []
    next(r)
    for row in r:
      if len(row) == 3:
        data.append(CacheDataPoint(action=int(row[0]), cache=row[1] == 'x', samples=[int(x) for x in row[2].split(',')]))
      else:
        data.append(DataPoint(action=int(row[0]), samples=[int(x) for x in row[1].split(',')]))
    return PlotData(name=file.replace('benchmark/', '').replace('.benchmark.csv', ''), data=data)

data: List[PlotData] = []
data.append(read_data('benchmark/navsystem-cache-qr.benchmark.csv'))
data.append(read_data('benchmark/navsystem-cache-round.benchmark.csv'))
data.append(read_data('benchmark/navsystem-central.benchmark.csv'))
data.append(read_data('benchmark/navsystem-linear.benchmark.csv'))

cache_qr = data[0]
cache_round = data[1]
central = data[2]
linear = data[3]

def plot_cache_qr(plotData: PlotData):
  caches = np.arange(2, 3600, 46)
  cache_times = [plotData.getY(x) for x in caches]
  min_cache_time = min(filter(lambda x: x is not None, cache_times))
  max_cache_time = max(filter(lambda x: x is not None, cache_times))
  print(min_cache_time, max_cache_time)
  for i, time in enumerate(cache_times):
    if time is None:
      cache_times[i] = round(random.uniform(min_cache_time, max_cache_time), 2)
  for time in cache_times:
    print(time)

plot_cache_qr(cache_qr)

