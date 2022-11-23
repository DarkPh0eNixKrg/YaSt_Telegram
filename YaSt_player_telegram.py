# -*- coding: utf-8 -*-
import base64
import websocket, ssl
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import telebot
import time

telegram_bot_token = 'TELEGRAM_BOT_TOKEN'
trust_chat_id = [TELEGRAM_CHAT_ID_1, TELEGRAM_CHAT_ID_2]
yast_device_ip = yast_device_port = yast_device_token = ''
yast_oauth_token = 'YANDEX_OAUTH_TOKEN'
yast_headers = {
	'Authorization':'OAUTH ' + yast_oauth_token,
	'Content-Type':'application/json'
}


# YaSt Block
###################################################################################################
def yast_get_devices_name(chat_id):
	yast_devices_name = []
	yast_device_url = 'https://quasar.yandex.net/glagol/device_list'
	yast_devices_json = requests.get(yast_device_url, headers=yast_headers, verify=False).json()
	for device in yast_devices_json['devices']:
# !!! Станции у которых в названии есть Дом или дом выводятся только доверенным пользователям
		if (('Дом' in device['name']) or ('дом' in device['name'])) and (chat_id not in trust_chat_id):
			pass
		else:
			yast_devices_name.append(device['name'])
	
	return yast_devices_name

def yast_get_devices_data(yast_device_name):
	yast_clear_data()
	global yast_device_ip
	global yast_device_port
	global yast_device_token
	
	yast_device_url = 'https://quasar.yandex.net/glagol/device_list'
	yast_devices_json = requests.get(yast_device_url, headers=yast_headers, verify=False).json()
	for yast_device in yast_devices_json['devices']:
		if (yast_device['name'] == yast_device_name):
			yast_device_id = yast_device['id']
			yast_device_ip = yast_device['networkInfo']['ip_addresses'][0]
			yast_device_port = str(yast_device['networkInfo']['external_port'])
			yast_device_platform = yast_device['platform']
			yast_url = 'https://quasar.yandex.net/glagol/token?device_id=' + yast_device_id + '&platform=' + yast_device_platform
			yast_device_token = requests.get(yast_url, headers=yast_headers, verify=False).json()['token']

	if (yast_device_ip == ''):
		return False
	else:
		return True

def yast_clear_data():
	global yast_device_ip
	global yast_device_port
	global yast_device_token
	yast_device_ip = yast_device_port = yast_device_token = ''

def yast_state():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			"command": "ping",
		},
	}
	ws.send(json.dumps(request))
	response = json.loads(ws.recv())
	ws.close()

	if (len(response['extra']['appState']) < 10):
		answer = 'Текущий трек: _ - _\nСтатус: Не воспроизводится'
	else:
		if (response['state']['playing'] == True):
			answer = 'Текущий трек: ' + response['state']['playerState']['subtitle'] + ' - ' + response['state']['playerState']['title'] + '\nСтатус: Воспроизводится'
		else:
			answer = 'Текущий трек: ' + response['state']['playerState']['subtitle'] + ' - ' + response['state']['playerState']['title'] + '\nСтатус: Не воспроизводится'
	return answer


def yast_cmd(command):
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : command
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_prew():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'prev'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_rewind():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Перемотать на 10 секунд назад'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_play():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'play'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_stop():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'stop',
			'text' : 'Стоп'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_forward():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Перемотать вперед на 10 секунд'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_next():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'next'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_like():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Лайк'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_dislike():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Дизлайк'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_shuffle():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Перемешать'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_volume_up():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Увеличить громкость'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_volume_down():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'sendText',
			'text' : 'Уменьшить громкость'
		}
	}
	ws.send(json.dumps(request))
	ws.close()

def yast_volume_mute():
	ws = websocket.WebSocket(sslopt={'cert_reqs':ssl.CERT_NONE})
	ws.connect('wss://' + yast_device_ip + ':' + yast_device_port)
	request = {
		'conversationToken': yast_device_token,
		'payload': {
			'command' : 'setVolume',
			'volume' : 0.0
		}
	}
	ws.send(json.dumps(request))
	ws.close()
###################################################################################################


# Telegram block
###################################################################################################
bot = telebot.TeleBot(telegram_bot_token)

# ⏮⏪▶️⏹⏩⏭❔
# ❤️💔🔀➕➖🔇↩️
player_menu = telebot.types.ReplyKeyboardMarkup(row_width=7, resize_keyboard=True)
button_prev = telebot.types.KeyboardButton('⏮')
button_rewind = telebot.types.KeyboardButton('⏪')
button_play = telebot.types.KeyboardButton('▶️')
button_stop = telebot.types.KeyboardButton('⏹')
button_forward = telebot.types.KeyboardButton('⏩')
button_next = telebot.types.KeyboardButton('⏭')
button_status = telebot.types.KeyboardButton('❔')
player_menu.add(button_prev, button_rewind, button_play, button_stop, button_forward, button_next, button_status)

button_like = telebot.types.KeyboardButton('❤️')
button_dislike = telebot.types.KeyboardButton('💔')
button_shuffle = telebot.types.KeyboardButton('🔀')
button_volume_up = telebot.types.KeyboardButton('➕')
button_volume_down = telebot.types.KeyboardButton('➖')
button_mute = telebot.types.KeyboardButton('🔇')
button_back = telebot.types.KeyboardButton('↩️')
player_menu.add(button_like, button_dislike, button_shuffle, button_volume_up, button_volume_down, button_mute, button_back)

def clear_chat(chat_id, message_id):
	for x in range(0,10):
		try:
			bot.delete_message(chat_id, message_id - x)
		except:
			pass

@bot.message_handler(commands=['start', 'select'])
def cmd_start_select(message):
	yast_clear_data()
	clear_chat(message.chat.id, message.message_id)
	yast_station_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	for yast in yast_get_devices_name(message.chat.id):
		yast_station_menu.add(telebot.types.KeyboardButton(yast))

	select_yast = bot.send_message(message.chat.id, 'Какой станцией вы хотите управлять?', reply_markup=yast_station_menu)
	bot.register_next_step_handler(select_yast, select_yast_handler)


@bot.message_handler(content_types=['text'])
def player_of_YaSt(message):
	if (yast_device_ip == ''):
		cmd_start_select(message)
	else:
		clear_chat(message.chat.id, message.message_id)
		if (message.text == '⏮'):
			yast_prew()
		elif (message.text == '⏪'):
			yast_rewind()
		elif (message.text == '▶️'):
			yast_play()
		elif (message.text == '⏹'):
			yast_stop()
		elif (message.text == '⏩'):
			yast_forward()
		elif (message.text == '⏭'):
			yast_next()
		elif (message.text == '❔'):
			yast_state()
		elif (message.text == '❤️'):
# !!! Лайк только доверенным пользователям
			if (message.chat.id in trust_chat_id):
				yast_like()
		elif (message.text == '💔'):
# !!! Дизлайк только доверенным пользователям
			if (message.chat.id in trust_chat_id):
				yast_dislike()
		elif (message.text == '🔀'):
			yast_shuffle()
		elif (message.text == '➕'):
			yast_volume_up()
		elif (message.text == '➖'):
			yast_volume_down()
		elif (message.text == '🔇'):
			yast_volume_mute()
		elif (message.text == '↩️'):
			cmd_start_select(message)
			return
		else:
			yast_cmd(message.text)

		bot.send_message(message.chat.id, yast_state(), reply_markup=player_menu)

def select_yast_handler(message):
	if (yast_get_devices_data(message.text) == True):
		clear_chat(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, yast_state(), reply_markup=player_menu)
	else:
		cmd_start_select(message)

bot.infinity_polling()
###################################################################################################
