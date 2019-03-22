import paho.mqtt.client as mqtt
import datetime
import time
#from pymongo import MongoClient
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Karu.settings')
django.setup()

from cebolla.models import *


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([
    ("ingrediente_1",0), ("ingrediente4",0),
    ("ingrediente2",0), ("ingrediente5",0),
    ("ingrediente3",0), ("ingrediente6",0),
	("rfid_caja",0)
    ])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	receiveTime=datetime.datetime.now()
	message=msg.payload.decode("utf-8")
	correctFormat = False
	if msg.topic == "rfid_caja":
		print("aca")
		
	else:
		try:
			data = str(message).strip('{}').split(', ')
			rfid = data[0].split(' ')[1]
			peso = int(data[1].split(' ')[1])
			print(rfid)
			print(peso)
			correctFormat = True
		except:
			print("couldnt properly gather the data")

		if correctFormat:
			#print(str(receiveTime) + ": " + msg.topic + " " + str(peso)+" "+ rfid)
			#post={"time":receiveTime,"topic":msg.topic,"value":val}
			
			#Se verifica si existe o no la rfID actual, si no, se crea en la base de datos
			try:
				rfid_object = rfID.objects.get(hex_id = rfid)
			except:
				print("no existe")
				rfid_object = rfID.objects.create(hex_id = rfid)	
			# Se obtiene la orden asociada a la rfid. Si no existe, se crea.
			print(rfid_object.hex_id)
			print(Order.objects.filter())
			try:
				order_object = Order.objects.get(rfID = rfid_object)
			except:
				print("creando el sandwich bitch")
				order_object = Order.objects.create(rfID = rfid_object)
			
			pesa = int(msg.topic[-1])
			#print(pesa)
			print(msg.topic)
			try:
				ingredient_object = Ingredient.objects.get(id = pesa)
				print('se logro')
			except:
				print("no hay ingrediente asociado a la pesa")
				return 
				
			Item.objects.create(ingredient = ingredient_object,
								order = order_object,
								amount = peso)
			print("creado con exito")
			
		else:
			print("couldnt store the data")
			#print(str(receiveTime) + ": " + msg.topic + " " + message)
			#post={"time":receiveTime,"topic":msg.topic,"value":message}
    #collection.insert_one(post).inserted_id

# Set up client for MongoDB
#mongoClient = MongoClient()
#db = mongoClient.SensorData
#collection = db.home_data

# Initialize the client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.210", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
while True:
	#client.publish("ingrediente_2", '{"rfid": "asdasd2", "peso": 240}')
	#client.publish("caja", '"asdasd2"')
	client.publish("tablet_5", '"asdasd2"')
	#client.publish("tablet_1", '0')
	time.sleep(5)