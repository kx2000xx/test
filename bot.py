import telebot
from settings import *
import requests
from restriction import *

bot = telebot.TeleBot(API_KEY, parse_mode=None)
global name
global typex
global totalseasons 
global releaseyear
global option
global Notes
global ticketType

@bot.message_handler(commands=['start'])
def send_welcome(message):
	username = message.from_user.username
	user_id = message.from_user.id
	user_status = bot.get_chat_member(chat_id=public_channel_id, user_id=user_id)
	if user_status.status == "member" or user_status.status == "creator":
		restriction_message = restriction_check(str(username))
		if restriction_message == True:
			bot.reply_to(message, "1. New Request | طلب جديد\n2. Modification | تعديل")
			bot.register_next_step_handler(message, options)
		else:
			bot.reply_to(message, restriction_message)
	else:
		bot.reply_to(message, "أنت لست عضواً في قناتنا\nقم بالإنضمام إلينا\n@VULTURE_TV")
	


def options(message):
	global option
	option = message.text
	global ticketType
	if option == '1':
		ticketType = "[New Request | طلب جديد]"
		bot.reply_to(message, "New Request | طلب جديد\n\n1. Movie | فيلم\n2. TV Series | مسلسل")
		bot.register_next_step_handler(message, new_request)
	elif option == '2':
		ticketType = "[Modification | تعديل]"
		bot.reply_to(message, "Modification | تعديل\n\n1. Movie | فيلم\n\n2. TV Series | مسلسل\n\n3. TV Channel | قناة")
		bot.register_next_step_handler(message, modify)
	else:
		bot.reply_to(message, "There is no option with this number | لا يوجد خيار بهذا الرقم")

def new_request(message):
	global option
	option = message.text
	if option == '1':
		bot.reply_to(message, "Movie Name | أسم الفلم")
		bot.register_next_step_handler(message, title)
	elif option == '2':
		bot.reply_to(message, "TV Series Name | أسم المسلسل")
		bot.register_next_step_handler(message, title)
	else:
		bot.reply_to(message, "There is no option with this number | لا يوجد خيار بهذا الرقم")



def modify(message):
	global option
	option = message.text
	if option == '1':
		bot.reply_to(message, "Movie Name | أسم الفلم")
		bot.register_next_step_handler(message, title)
	elif option == '2':
		bot.reply_to(message, "TV Series Name | أسم المسلسل")
		bot.register_next_step_handler(message, title)
	elif option == '3':
		bot.reply_to(message, "TV Channel Name | أسم القناة")
		bot.register_next_step_handler(message, title)
	else:
		bot.reply_to(message, "There is no option with this number | لا يوجد خيار بهذا الرقم")




def title(message):
	global name
	name = message.text
	if option == '3':
		bot.reply_to(message, "Notes (Type dash if there are no notes) | ملاحظات (ضع شرطة إذا كان لا يوجد أي ملاحظة)")
		bot.register_next_step_handler(message, notes)
	else:
		bot.reply_to(message, "Release Year | سنة الإنتاج")
		bot.register_next_step_handler(message, release_year)



def release_year(message):
	global releaseyear
	releaseyear = message.text
	bot.reply_to(message, "Show Type Subbed/Dubbed | نوع العمل مترجم/مدبلج\n\n1. Subbed | مترجم\n2. Dubbed | مدبلج\n3. other | غير ذلك")
	bot.register_next_step_handler(message, type)




def type(message):
	global typex
	typex = message.text
	if typex == '1':
		typex = "مترجم"
	elif typex == '2':
		typex = "مدبلج"
	elif typex == '3':
		typex = "غير ذلك"
	if option == '1':
		bot.reply_to(message, "Type Notes or Type dash if there are no notes | أكتب ملاحظات أو ضع شرطة إذا كان لا يوجد أي ملاحظة")
		bot.register_next_step_handler(message, notes)
	elif option == '2':
		bot.reply_to(message, "Number of Seasons | عدد المواسم")
		bot.register_next_step_handler(message, seasons)

def notes(message):
	global Notes
	Notes = message.text
	if option == '3':
		send_caption_only(message)
	else:
		bot.reply_to(message, "Send the Show's Poster | قم بإرسال البوستر الخاص بالعمل")
		bot.register_next_step_handler(message, send_photo_with_caption)





def seasons(message):
	global totalseasons
	totalseasons = message.text
	bot.reply_to(message, "Type Notes or Type dash if there are no notes | أكتب ملاحظات أو ضع شرطة إذا كان لا يوجد أي ملاحظة")
	bot.register_next_step_handler(message, notes)


def send_caption_only(message):
	caption = Channel_caption(name, Notes)
	bot.send_message(chat_id=requests_private_channel, text=caption)
	bot.reply_to(message, "Your Request has Been Submitted | تم إرسال طلبك")
	bot.send_message(message.chat.id,"Your Request Will Be fulfilled As Soon As Possible. | سيتم تلبية طلبك في أقرب وقت ممكن")
	add_to_restrictor(message.from_user.username)




def send_photo_with_caption(message):
	photo_id = message.photo[2].file_id
	print(photo_id)
	url = str("https://api.telegram.org/bot"+API_KEY+"/getfile?file_id="+photo_id)
	r = requests.get(url)
	data = r.json()
	photo_path = data['result']['file_path']
	url = str("https://api.telegram.org/file/bot"+API_KEY+"/"+photo_path)
	print(url)
	
	with open('poster.jpg', 'wb') as handle:
		response = requests.get(url, stream=True)
		for block in response.iter_content(1024):
			if not block:
				break
			handle.write(block)
	photo = open('poster.jpg', 'rb')
	if option == '1':
		caption = Movie_caption(name, releaseyear, typex, Notes)
	elif option == '2':
		caption = Series_caption(name, releaseyear, typex, Notes)
	bot.send_photo(requests_private_channel, photo, caption=caption)
	bot.reply_to(message, "Your Request Has Been Submitted | تم إرسال طلبك")
	bot.send_message(message.chat.id,"Your Request Will Be fulfilled As Soon As Possible. | سيتم تلبية طلبك في أقرب وقت ممكن")
	username = message.from_user.username
	add_to_restrictor(username)


def Movie_caption(name, releaseyear, typex, Notes):
	caption = ticketType + "\n\n\n"
	caption += "أسم الفلم: " + name +"\n\n"
	caption += "سنة الإنتاج: " + releaseyear +"\n\n"
	caption += "نوع العمل: " + typex +"\n\n"
	caption += " ملاحظات: " + Notes
	return caption


def Series_caption(name, releaseyear, typex, Notes):
	caption = ticketType + "\n\n\n"
	caption += "أسم المسلسل: " + name +"\n\n"
	caption += "عدد المواسم: " + totalseasons +"\n\n"
	caption += "سنة الإنتاج :" + releaseyear +"\n\n"
	caption += "نوع العمل: " + typex +"\n\n"
	caption += " ملاحظات:" + Notes
	return caption

def Channel_caption(name, Notes):
	caption = ticketType + "\n\n\n"
	caption += "أسم القناة: " + name +"\n\n"
	caption += " ملاحظات: " + Notes
	return caption


bot.infinity_polling()