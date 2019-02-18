import paho.mqtt.client as mqtt
import datetime
import time
#from pymongo import MongoClient
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Karu.settings')
django.setup()

from cebolla.models import *

def createItem(message, msg):	
	
	correctFormat = False
	try:
		data = str(message).strip('{}').split(', ')
		rfid = data[0].split(' ')[1]
		peso = int(data[1].split(' ')[1])
		correctFormat = True
	except:
		print("couldnt properly gather the data")

	if correctFormat:
		#print(str(receiveTime) + ": " + msg.topic + " " + str(peso)+" "+ rfid)
		#post={"time":receiveTime,"topic":msg.topic,"value":val}
		
		#Se verifica si existe o no la rfID actual, si no, se crea en la base de datos7

		if not rfID.objects.filter(hex_id = rfid).exists():
			rfid_object = rfID.objects.create(hex_id = rfid)
		else:	
			rfid_object = rfID.objects.get(hex_id = rfid)
			
		# Se obtiene la orden asociada a la rfid. Si no existe, se crea.
		if not Order.objects.filter(rfID = rfid_object).exists():
			order_object = Order.objects.create(rfID = rfid_object)
		else:
			order_object = Order.objects.get(rfID = rfid_object)
		
		pesa = int(msg.topic.split('_')[1])
		#print(pesa)
		#print(msg.topic)
		
		if Ingredient.objects.filter(scale = pesa).exists():
			#print('aca muere')
			ingredient_object = Ingredient.objects.get(scale = pesa)
			#print("ingrediente encontrado")
	
			if not Item.objects.filter(ingredient = ingredient_object, order = order_object).exists():
				item = Item.objects.create(ingredient = ingredient_object,
									order = order_object,
									amount = peso, itemPrice = ingredient_object.price)
				
			else:
				item = Item.objects.get(ingredient = ingredient_object, order = order_object)
				item.amount += peso
				item.save()
				
			#print('aca')
			order_object.orderPrice += peso * item.itemPrice
			#print(order_object.orderPrice)
			order_object.save()
			print("recibido y guardado peso: "+str(peso))
			
		print("error")

		
def selectOrder(message,msg):
	correctFormat = False
	try:
		#rfid = int(message)
		rfid = message
		correctFormat = True
	except:
		print('no se recibieron los datos correctamente')
		
	print(rfid)
	if rfid == "-1":
		orders = Order.objects.filter()
		for order in orders:
			order.ongoing = False
			order.save()
	else:
		orders = Order.objects.filter()
		for order in orders:
			order.ongoing = False
			order.save()
			
		if Order.objects.filter(rfID__hex_id = rfid).exists():
			order_object = Order.objects.get(rfID__hex_id = rfid)
			order_object.ongoing = True
			order_object.save()
			print("orden guardada")
		else:
			print("la rfid no tiene una orden asociada")

def setReceivingOrder(message,msg):
	correctFormat = False
	try:
		#rfid = int(message)
		rfid = message
		tid = int(msg.topic.split('_')[-1])
		correctFormat = True
	except:
		print('no se recibieron los datos correctamente')
		
	print(rfid)
	if rfid == "0":
		orders = Order.objects.filter(receiving = tid)
		for order in orders:
			order.receiving = 0
			order.save()
	else:
		orders = Order.objects.filter(receiving = tid)
		for order in orders:
			order.receiving = 0
			order.save()
			
		if Order.objects.filter(rfID__hex_id = rfid).exists():
			order_object = Order.objects.get(rfID__hex_id = rfid)
			order_object.receiving = tid
			order_object.save()
			print("orden recepcionando ingredientes especiales")
		else:
			if not rfID.objects.filter(hex_id = rfid).exists():
				rfid_object = rfID.objects.create(hex_id = rfid)
			else:	
				rfid_object = rfID.objects.get(hex_id = rfid)
			order_object = Order.objects.create(rfID = rfid_object)
			order_object.receiving = tid
			order_object.save()
			print("orden creada y recepcionando ingredientes especiales")

			
def sendPrices(message,msg):
	rfid = message
	pesa = int(msg.topic.split('_')[-1])
	#print(rfid)
	#print(pesa)
	if Ingredient.objects.filter(scale = pesa).exists() and pesa != 0:
		ingredientPrice = Ingredient.objects.get(scale = pesa).price
		
		if Order.objects.filter(rfID__hex_id = rfid).exists():
			orderPrice = Order.objects.get(rfID__hex_id = rfid).orderPrice
		else:
			orderPrice = 0
		#client.publish("cumprice_ingrediente_"+str(pesa),orderPrice)
		print("enviado: "+str(ingredientPrice))
		client.publish("precio_ingrediente_"+str(pesa),ingredientPrice) 
		client.publish("acumulado_ingrediente_"+str(pesa),orderPrice)
			

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([
	("id_ingrediente_1",0), ("id_ingrediente_2",0),
	("ingrediente_1",0), ("ingrediente_4",0),
    ("ingrediente_2",0), ("ingrediente_5",0),
    ("ingrediente_3",0), ("ingrediente_6",0),
	("caja",0), ("tablet_1",0)
    ])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic)
	receiveTime=datetime.datetime.now()
	message=msg.payload.decode("utf-8")
	correctFormat = False
	print("aca")
	request = msg.topic.split('_')[0]
	print(request)
	if request == "caja":
		selectOrder(message,msg)
	elif request == "ingrediente":
		createItem(message, msg)
	elif request == "id":
		sendPrices(message, msg)
	elif request == "tablet":
		setReceivingOrder(message, msg)
		
	
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
    client.loop_forever()
