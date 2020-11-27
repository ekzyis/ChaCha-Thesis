#!/usr/bin/env python

import csv
from dataclasses import dataclass
from typing import List
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

def avg(n):
  return sum(n)/len(n)

@dataclass
class DataPoint:
  action: int
  samples: List[int]
  interpolated: bool

  def average(self):
    return avg(self.samples)

@dataclass
class CacheDataPoint(DataPoint):
  cache: bool

@dataclass
class PlotData:
  name: str
  data: List[DataPoint]

  def x(self):
    return [d.action for d in sorted(self.data, key=lambda d: d.action)]

  def y(self):
    return [d.average() for d in sorted(self.data, key=lambda d: d.action)]

  def getY(self, x):
    return next((d.average() for d in self.data if d.action == x), None)

def read_data(file: str) -> PlotData:
  with open(file) as csvfile:
    r = csv.reader(csvfile, delimiter='|')
    data = []
    next(r)
    for row in r:
      if len(row) == 3:
        data.append(
          CacheDataPoint(
            action=int(row[0]), cache=row[1] == 'x', samples=[int(x) for x in row[2].split(',')], interpolated=False
          )
        )
      else:
        data.append(
          DataPoint(
            action=int(row[0]), samples=[int(x) for x in row[1].split(',')], interpolated=False
          )
        )
    return PlotData(name=file.replace('benchmark/', '').replace('.benchmark.csv', ''), data=data)

data: List[PlotData] = []
data.append(read_data('benchmark/navsystem-cache-qr.benchmark.csv'))
data.append(read_data('benchmark/navsystem-cache-round.benchmark.csv'))
data.append(read_data('benchmark/navsystem-central.benchmark.csv'))
data.append(read_data('benchmark/navsystem-linear.benchmark.csv'))

def insert_interpolation(plotData: PlotData, cache_step: int):
  first_cache = 2
  max_actions = 3600
  # Interpolate data for cached action which are missing in the benchmark data
  caches = np.arange(first_cache, max_actions, cache_step)
  cache_times = [plotData.getY(x) for x in caches]
  avg_cache_time = round(avg(list(filter(lambda y: y is not None, cache_times))), 2)
  pprint(plotData)
  for (x,t) in zip(caches, cache_times):
    if t is None:
      plotData.data.append(CacheDataPoint(action=x, samples=[avg_cache_time], cache=True, interpolated=True))

  # Interpolate data for actions between caches which are missing in the benchmark data
  mid_caches = np.arange(first_cache + (cache_step / 2), max_actions, cache_step)
  mid_cache_times = [plotData.getY(x) for x in mid_caches]
  avg_mid_cache_time = round(avg(list(filter(lambda y: y is not None, mid_cache_times))), 2)
  for (x, t) in zip(mid_caches, mid_cache_times):
    if t is None:
      plotData.data.append(CacheDataPoint(action=x, samples=[avg_mid_cache_time], cache=False, interpolated=True))

def plot_cache(plotData: PlotData, title):
  fig, ax = plt.subplots(figsize=(20, 5))
  x, y = plotData.x(), plotData.y()

  cache_data = list(map(lambda d: (d.action, d.average()), filter(lambda d: d.cache == True and d.interpolated == False, sorted(plotData.data, key=lambda d: d.action))))
  cache_x, cache_y = [d[0] for d in cache_data], [d[1] for d in cache_data]

  cache_data_int = list(map(lambda d: (d.action, d.average()), filter(lambda d: d.cache == True and d.interpolated == True, sorted(plotData.data, key=lambda d: d.action))))
  cache_x_int, cache_y_int = [d[0] for d in cache_data_int], [d[1] for d in cache_data_int]

  non_cache_data_int = list(map(lambda d: (d.action, d.average()), filter(lambda d: d.cache == False and d.interpolated == True, sorted(plotData.data, key=lambda d: d.action))))
  non_cache_x_int, non_cache_y_int = [d[0] for d in non_cache_data_int], [d[1] for d in non_cache_data_int]

  ax.plot(x, y, '-o', zorder=1)
  ax.scatter(non_cache_x_int, non_cache_y_int, marker='s', zorder=2, label='interpolated')
  ax.scatter(cache_x, cache_y, c='g', zorder=3, label='cached actions')
  ax.scatter(cache_x_int, cache_y_int, marker='s', c='g', zorder=4, label='cached actions (interpolated)')

  ax.legend()
  ax.set(title=title, xlabel='action', ylabel='time [ms]')
  plt.ylim(0, max(y)+10)
  plt.show()

def plot_cache_qr(plotData: PlotData):
  """
  Create the plot for the navigation system with caches at every quarterround.
  """
  insert_interpolation(plotData, 46)
  plot_cache(plotData, title='Performance of navigation system with caches for every quarterround')

plot_cache_qr(data[0])

def plot_cache_round(plotData: PlotData):
  """
  Create the plot for the navigation system with caches at every round.
  """
  insert_interpolation(plotData, 184)
  plot_cache(plotData, title='Performance of navigation system with caches for every round')
  
plot_cache_round(data[1])

def plot_linear(plotData: PlotData):
  fig, ax = plt.subplots(figsize=(20, 5))
  x, y = plotData.x(), plotData.y()

  ax.plot(x, y, '-o')
  ax.set(title='Performance of linear navigation system', xlabel='action', ylabel='time [ms]')
  plt.ylim(0, max(y) + 10)
  plt.show()

plot_linear(data[3])

def plot_central(plotData: PlotData):
  fig, ax = plt.subplots(figsize=(20, 5))
  x, y = plotData.x(), plotData.y()

  ax.plot(x, y, '-o')
  ax.set(title='Performance of centralized navigation system', xlabel='action', ylabel='time [ms]')
  plt.ylim(0, max(y) + 10)
  plt.show()

plot_central(data[2])