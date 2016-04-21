import sys
import matplotlib.pyplot as plt
import numpy as np

def getKey(protocol, model, size, traffictype):
  kbSize = int(size) / 1000
  if kbSize < 1000:
    key = protocol.upper() + "_" + model.upper() + "_" + str(kbSize) + "KB_" + traffictype.upper()
  else:
    mbSize = kbSize / 1000
    key = protocol.upper() + "_" + model.upper() + "_" + str(mbSize) + "MB_" + traffictype.upper()
  return key

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "Not enough arguments. Quitting..."
    sys.exit()

  try:
    with open('data/bandwidth.csv') as f:
      content = f.readlines()
  except:
    print "File doesn't exist. Quitting..."
    sys.exit()

  data = {}

  for lineNumber in xrange(0, len(content)):
    line = content[lineNumber]
    if lineNumber % 5 != 0:
      continue
    tokens = line.split()
    key = tokens[0] + "_" + tokens[1] + "_" + tokens[2] + "_" + tokens[3]
    dataSent = int(content[lineNumber + 1])
    throughputTotal = float(content[lineNumber + 2])
    throughput = float(content[lineNumber + 3])
    packetsSent = int(content[lineNumber + 4])
    networkData = {}
    networkData["dataSent"] = dataSent
    networkData["throughputTotal"] = throughputTotal
    networkData["throughput"] = throughput
    networkData["packetsSent"] = packetsSent
    data[key] = networkData

  protocol = sys.argv[1]
  model = sys.argv[2]
  traffictype = sys.argv[3]

  onekbkey = getKey(protocol, model, 1000, traffictype)
  hundredkbkey = getKey(protocol, model, 100000, traffictype)
  onembkey = getKey(protocol, model, 1000000, traffictype)
  thruputs = []
  if onekbkey in data:
    thruputs.append(data[onekbkey]["throughputTotal"])
  if hundredkbkey in data:
    thruputs.append(data[hundredkbkey]["throughputTotal"])
  if onembkey in data:
    thruputs.append(data[onembkey]["throughputTotal"])
  index = np.arange(len(thruputs))

  barWidth = .35
  plt.bar(index, thruputs, barWidth)
  plt.xticks(index + (barWidth/2), ('1KB', '100KB', '1 MB'))
  plt.xlabel('Message Size')
  plt.ylabel('Throughput (MB/s)')

  if model == 'fast':
    modelName = "Bulk Transfer"
  elif model == 'onoff':
    modelName = "ON/OFF Model"
  else:
    modelName = "Telemetry Model"
  plt.title('Throughput for ' + protocol.upper() + ' ' + modelName + ' of Varying Size')
  plt.show()
