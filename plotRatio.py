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

def plotLine(data, protocol, model, size):
  lossy5 = data[getKey(protocol, model, size, "lossy5")]
  lossy15 = data[getKey(protocol, model, size, "lossy15")]
  lossy25 = data[getKey(protocol, model, size, "lossy25")]
  xVals = [5, 15, 25]
  yVals = []
  yVals.append(lossy5["ratio"])
  yVals.append(lossy15["ratio"])
  yVals.append(lossy25["ratio"])

  return plt.plot(xVals, yVals, label=protocol)

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Not enough arguments. Quitting..."
    sys.exit()

  try:
    with open('data/bandwidth2.txt') as f:
      content = f.readlines()
  except:
    print "File doesn't exist. Quitting..."
    sys.exit()

  data = {}

  for lineNumber in xrange(0, len(content)):
    line = content[lineNumber]
    if lineNumber % 6 != 0:
      continue
    tokens = line.split()
    key = tokens[0] + "_" + tokens[1] + "_" + tokens[2] + "_" + tokens[3]
    dataSent = int(content[lineNumber + 1])
    throughputTotal = float(content[lineNumber + 2])
    throughput = float(content[lineNumber + 3])
    packetsSent = int(content[lineNumber + 4])
    ratio = float(content[lineNumber + 5])
    networkData = {}
    networkData["dataSent"] = dataSent
    networkData["throughputTotal"] = throughputTotal
    networkData["throughput"] = throughput
    networkData["packetsSent"] = packetsSent
    networkData["ratio"] = ratio
    data[key] = networkData

  model = sys.argv[1]
  size = sys.argv[2]

  amqp, = plotLine(data, "amqp", model, size)
  mqtt2, = plotLine(data, "mqtt2", model, size)
  mqtt1, = plotLine(data, "mqtt1", model, size)
  mqtt0, = plotLine(data, "mqtt0", model, size)
  xmpp, = plotLine(data, "xmpp", model, size)
  coap1, = plotLine(data, "coap1", model, size)
  coap0, = plotLine(data, "coap0", model, size)

  plt.xlabel('Packet Loss Percentage')
  plt.ylabel('Goodput Ratio')
  plt.title('Packet Loss Percentage vs Goodput Ratio')
  plt.axis([0, 30, .5, 1.0])
  plt.legend([amqp, mqtt2, mqtt1, mqtt0, xmpp, coap1, coap0], ['AMQP', 'MQTT QoS = 2', 'MQTT QoS = 1', 'MQTT QoS = 0', 'XMPP', 'CoAP QoS = 1', 'CoAP QoS = 0'])

  plt.show()
