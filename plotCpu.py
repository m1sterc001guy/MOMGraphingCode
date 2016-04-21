import sys
import matplotlib.pyplot as plt

def plotLine(protocol, model, size, traffictype):
  filename = protocol + "_cpu_pub_" + model + "_" + size  + "_" + traffictype
  try:
    with open('data/' + filename) as f:
      content = f.readlines()
  except:
    return None

  xVals = []
  yVals = []
  for line in content:
    tokens = line.split()
    xVals.append(int(tokens[0]))
    yVals.append(float(tokens[1]))

  return plt.plot(xVals, yVals, label=protocol)

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "Not enough arguments. Quitting..."
    sys.exit()

  model = sys.argv[1]
  size = sys.argv[2]
  traffictype = sys.argv[3]
  amqp = plotLine("amqp", model, size, traffictype)
  mqtt = plotLine("mqtt0", model, size, traffictype)
  xmpp = plotLine("xmpp", model, size, traffictype)
  coap = plotLine("coap0", model, size, traffictype)
  
  plt.axis([0, 180, 0, 1.0])
  if coap != None:
    plt.legend([amqp, mqtt, xmpp, coap], ['AMQP', 'MQTT QoS=0', 'XMPP', 'CoAP QoS=0'])
  else:
    plt.legend([amqp, mqtt, xmpp], ['AMQP', 'MQTT QoS=0', 'XMPP'])
  plt.xlabel('Time (Seconds)')
  plt.ylabel('CPU Utilization')
  if model == 'fast':
    modelName = "Bulk Transfer"
  elif model == 'onoff':
    modelName = "ON/OFF Model"
  else:
    modelName = "Telemetry Model"
  kbSize = int(size) / 1000
  if kbSize < 1000:
    plt.title('CPU Utilization for ' + modelName + ' of ' + str(kbSize) + ' KB Messages')
  else:
    mbSize = kbSize / 1000
    plt.title('CPU Utilization for ' + modelName + ' of ' + str(mbSize) + ' MB Messages')
  plt.show()
