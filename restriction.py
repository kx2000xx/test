from settings import *
from datetime import datetime, timedelta

usernames = [] 
times = []
time_in_seconds = 604800
def restriction_check(username):
	message = ''
	if username in usernames:
		index = usernames.index(username)
		if times[index]+timedelta(seconds=time_in_seconds) > datetime.now():
			futuretime = datetime.strptime(str(times[index]+timedelta(seconds=time_in_seconds)), '%Y-%m-%d %H:%M:%S.%f')
			currenttime = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
			timeleft = futuretime - currenttime
			timeleft = str(timeleft.days+1)
			timeleft = timeleft.replace("days,", "يوم")
			message = "لا يمكنك إرسال طلب آخر إلا بعد "+ timeleft + " أيام"
		else:
			index = usernames.index(username)
			usernames.remove(username)
			del times[index]
			message = True
	else:
		message = True
	return message

def add_to_restrictor(username):
	if username not in usernames:
		usernames.append(username)
		times.append(datetime.now())