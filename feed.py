import time
from cgi import parse_qs, escape 
import pigpio

mypi = pigpio.pi()
mypi.set_PWM_dutycycle(18, 0)
mypi.set_PWM_frequency(18, 0)

myvars = {}

def application(environ, start_response): 
	status = '200 OK' 
	output = '<html>' 

	d = parse_qs(environ['QUERY_STRING']) 
	dispensed = d.get('dispensed', [''])[0] 

	if dispensed == "1":
		# turn on 
		mypi.write( 17, 1 ) 
		mypi.set_servo_pulsewidth(18,600)
		time.sleep(0.5)
		mypi.set_servo_pulsewidth(18,2200)
		time.sleep(0.5)
		mypi.set_servo_pulsewidth(18,1500)

		count = 0
		if "COUNTER" in myvars:
			count = myvars["COUNTER"]
		myvars["COUNTER"] = count+1
		output += "<h2>Button Pushes: " + str( myvars["COUNTER"] ) + "</h2>"

	output += '<a href="' + environ["SCRIPT_NAME"] + '?dispensed=1"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTxSv8xZZSEI-c8H6LOVBnmlh3KLiCEp5CuqSdMjkc9unkszGThBl0k_s" width="300" /></a>' 
	output += '<img src="/pics/test_image.png"'
	output += '</html>'

	response_headers = [('Content-type', 'text/html'), 
			    ('Content-Length', str(len(output)))] 
	start_response(status, response_headers) 
	return [output]
