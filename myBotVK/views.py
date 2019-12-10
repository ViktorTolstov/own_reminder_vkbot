from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import vk
import random
import database

session = vk.Session(access_token='bd474e72f9fd5b28da782dbdd5fc1f3b1832bc10566d57ed68a74e9f18cdede0d81ea8335c11f532259c3')
vk_api = vk.API(session)

@csrf_exempt
def admin(request):
	with open('myBotVK/templates/index.html', 'r') as file:
		return HttpResponse(file.read())

@csrf_exempt
def script(request):
	with open('myBotVK/templates/script.js', 'r') as file:
		return HttpResponse(file.read(), content_type="text/javascript")

@csrf_exempt
def client_server(request):
	body = json.loads(request.body)
	res = {}
	if body["type"] == "login":
		if (body["username"] == "admin") and (body["password"] == "admin"):
			res["correct"] = True
			res["val"] = database.get_groups()
			with open('myBotVK/templates/admin.html', 'r') as file:
				res["html"] = file.read()
		else:
			res["correct"] = False
		#print(res)
		return HttpResponse(json.dumps(res))
	elif body["type"] == "postNewMessage":
		users_chat_id = database.get_member(body["group"])
		#print(users_chat_id)
		for i in users_chat_id:
			vk_api.messages.send(user_id=i, message=body['content'],random_id=random.randint(1,50000000000000000000000) ,v=5.103)
		return HttpResponse(json.dumps({"res":"ok"}))

@csrf_exempt
def get_message(request):
	body = json.loads(request.body)
	print(body)
	if body["type"] == 'message_new':
		if "payload" in body["object"]["message"]:
			if body["object"]["message"]["payload"] == '{"command":"start"}':
				start(request)
			elif body["object"]["message"]["payload"] == '{"command":"delete"}':
				user_id = body["object"]["message"]["from_id"]
				database.delete_member(user_id)
				print(database.get_db())
				start(request)
			else:
				user_id = body["object"]["message"]["from_id"]
				group = body["object"]["message"]["payload"]
				database.add_member(group,user_id)
				delete_button(request)
		else:
			talk(request)
	return HttpResponse("ok")

def delete_button(request):
	body = json.loads(request.body)
	user_id = body["object"]["message"]["from_id"]
	message = "Если захочешь изменить группу нажми кнопку Изменить группу"
	keyboard = {
		"one_time": False,
		"buttons": [
			[{
				"action": {
					"type": "text",
					"payload": '{"command":"delete"}',
					"label": "Изменить группу"
				},
				"color": "negative"
			}]
		]
	}
	vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(keyboard), random_id=random.randint(1,50000000000000000000000) ,v=5.103)

def start(request):
	body = json.loads(request.body)
	user_id = body["object"]["message"]["from_id"]
	message = "Чтобы получать от меня уведомления выбери свою группу из предложенных вариантов"
	keyboard = {
		"one_time": True,
		"buttons": [
			[{
					"action": {
						"type": "text",
						"payload": '{"command":"friends"}',
						"label": "Друзья"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command":"classmates"}',
						"label": "Одноклассники"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command":"programmers"}',
						"label": "Программисты"
					},
					"color": "primary"
				}
			]
		]
	}
	vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(keyboard), random_id=random.randint(1,50000000000000000000000) ,v=5.103)

@csrf_exempt
def init(request):
	body = json.loads(request.body)
	if body == { "type": "confirmation", "group_id": 188996934 }:
		return HttpResponse("8806c6d6")

def talk(request):
	body = json.loads(request.body)
	data = database.get_db()
	user_id = body["object"]["message"]["from_id"]
	if body["object"]["message"]["text"].find('/') != -1:
		mes = body["object"]["message"]["text"].split('/')
		database.insert_db(mes[0],mes[1])
		vk_api.messages.send(user_id=user_id, message="Я записал новую фразу", random_id=random.randint(1,50000000000000000000000) ,v=5.103)
	else:
		for i in data:
			if i[1] == body["object"]["message"]["text"]:
				messages = i[2]
				vk_api.messages.send(user_id=user_id, message=messages, random_id=random.randint(1,50000000000000000000000) ,v=5.103)
			elif i == data[-1] and i[1] != body["object"]["message"]["text"]:
				message1 = "Я не понимаю это сообщение"
				message2 = "Напиши мне пару Сообщение/Ответ, если ты хочешь добавить новую фразу. Не забудь разделить их знаком /"
				vk_api.messages.send(user_id=user_id, message=message1, random_id=random.randint(1,50000000000000000000000) ,v=5.103)
				vk_api.messages.send(user_id=user_id, message=message2, random_id=random.randint(1,50000000000000000000000) ,v=5.103)

@csrf_exempt
def empty(request):
	body = json.loads(request.body)
	user_id = body["object"]["message"]["from_id"]
	message = "Чтобы получать от меня уведомления выбери свою группу из предложенных вариантов"
	keyboard = {"buttons":[],"one_time":True}
	vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(keyboard), random_id=random.randint(1,50000000000000000000000) ,v=5.103)
