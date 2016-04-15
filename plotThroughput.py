import sys
import matplotlib.pyplot as plt
import numpy as np

def getKey(protocol, model, size, type):
  kbSize = int(size) / 1000
  if kbSize < 1000:
    key = protocol.upper() + "_" + model.upper() + "_" + str(kbSize) + "KB_" + type.upper()
  else:
    mbSize = kbSize / 1000
    key = protocol.upper() + "_" + model.upper() + "_" + str(mbSize) + "MB_" + type.upper()
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

  model = sys.argv[1]
  size = sys.argv[2]
  type = sys.argv[3]

  protocol = "amqp"
  amqpkey = getKey(protocol, model, size, type)
  protocol = "mqtt0"
  mqttkey = getKey(protocol, model, size, type)
  protocol = "xmpp"
  xmppkey = getKey(protocol, model, size, type)
  protocol = "coap"
  coapkey = getKey(protocol, model, size, type)
  thruputs = []
  if amqpkey in data:
    thruputs.append(data[amqpkey]["throughputTotal"])
  if mqttkey in data:
    thruputs.append(data[mqttkey]["throughputTotal"])
  if xmppkey in data:
    thruputs.append(data[xmppkey]["throughputTotal"])
  if coapkey in data:
    thruputs.append(data[coapkey]["throughputTotal"])
  index = np.arange(len(thruputs))

  barWidth = .35
  plt.bar(index, thruputs, barWidth)
  plt.xticks(index + (barWidth/2), ('AMQP', 'MQTT QoS=0', 'XMPP', 'CoAP'))
  plt.xlabel('Protocol')
  plt.ylabel('Throughput (MB/s)')

  if model == 'fast':
    modelName = "Bulk Transfer"
  elif model == 'onoff':
    modelName = "ON/OFF Model"
  else:
    modelName = "Telemetry Model"
  kbSize = int(size) / 1000
  if kbSize < 1000:
    plt.title('Throughput for ' + modelName + ' of ' + str(kbSize) + ' KB Messages')
  else:
    mbSize = kbSize / 1000
    plt.title('Throughput for ' + modelName + ' of ' + str(mbSize) + ' MB Messages')

  plt.show()
