#!/usr/bin/env python

import csv
from dataclasses import dataclass
from typing import List
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

pprint(data)

for d in data:
  x = d.x()
  y = d.y()
  fig, ax = plt.subplots()
  ax.plot(x, y, '-o')
  for xy in zip(x, y):
    ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
  ax.set(title=d.name, xlabel='action', ylabel='Time [ms]')
  plt.show()

