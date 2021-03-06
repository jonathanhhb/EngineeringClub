#!/usr/bin/python 

from cgi import parse_qs, escape 
import pigpio

mypi = pigpio.pi()
mypi.set_PWM_dutycycle(18, 0)
mypi.set_PWM_frequency(18, 0)

def application(environ, start_response): 
	status = '200 OK' 
	output = '<html>' 

	d = parse_qs(environ['QUERY_STRING']) 
	led_val = d.get('led', [''])[0] 
	if led_val == '' or led_val == "off":
		# turn off 
		mypi.write( 17, 0 ) 
		mypi.set_servo_pulsewidth(18, 600)
		output += '<a href="' + environ["SCRIPT_NAME"] + '?led=on"><img src="https://thumbs.dreamstime.com/x/toggle-switch-7382047.jpg"/></a><br>' 
	elif led_val == "on":
		# turn on 
		mypi.write( 17, 1 ) 
		mypi.set_servo_pulsewidth(18, 2500)
		output += '<a href="' + environ["SCRIPT_NAME"] + '?led=off"><img src="https://thumbs.dreamstime.com/x/tumbler-7633745.jpg"/></a>' 
	output += '</html>'

	response_headers = [('Content-type', 'text/html'), 
			    ('Content-Length', str(len(output)))] 
	start_response(status, response_headers) 
	return [output]
