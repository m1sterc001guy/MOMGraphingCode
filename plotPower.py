import sys
import matplotlib.pyplot as plt
import math

def plotLine(protocol, model, size, type, data):
  kbSize = int(size) / 1000
  if kbSize < 1000:
    key = protocol.upper() + "_" + model.upper() + "_" + str(kbSize) + "KB_" + type.upper()
  else:
    mbSize = kbSize / 1000
    key = protocol.upper() + "_" + model.upper() + "_" + str(mbSize) + "MB_" + type.upper()

  if key in data:
    axisData = data[key]
    return plt.plot(axisData["x"], axisData["y"], label=protocol.upper())
  else:
    return None

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "Not enough arguments. Quitting..."
    sys.exit()

  try:
    with open('data/sheet.csv') as f:
      content = f.readlines()
  except:
    print "File doesn't exist. Quitting..."
    sys.exit()

  data = {}
  resistence = .15

  for lineNumber in xrange(0, len(content)):
    line = content[lineNumber]
    if lineNumber % 3 != 0:
      continue
    tokens = line.split()
    key = tokens[0] + "_" + tokens[1] + "_" + tokens[2] + "_" + tokens[3]
    xValsString = content[lineNumber + 1].split(', ')
    xVals = [int(numeric_string) for numeric_string in xValsString]
    yValsString = content[lineNumber + 2].split(',')
    yVals = [((math.pow(float(numeric_string), 2) / resistence) * 1000) for numeric_string in yValsString]
    axis = {}
    axis["x"] = xVals
    axis["y"] = yVals
    data[key] = axis

  model = sys.argv[1]
  size = sys.argv[2]
  type = sys.argv[3]
  
  amqp = plotLine("amqp", model, size, type, data)
  mqtt = plotLine("mqtt0", model, size, type, data)
  xmpp = plotLine("xmpp", model, size, type, data)
  coap = plotLine("coap", model, size, type, data)

  if coap != None:
    plt.legend([amqp, mqtt, xmpp, coap], ['AMQP', 'MQTT QoS=0', 'XMPP', 'CoAP'])
  else:
    plt.legend([amqp, mqtt, xmpp], ['AMQP', 'MQTT QoS=0', 'XMPP'])
  plt.xlabel('Time (Seconds)')
  plt.ylabel('Power (mW)')
  plt.show()
