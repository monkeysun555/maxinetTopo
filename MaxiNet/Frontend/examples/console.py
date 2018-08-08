

def console_platform(mode, num_path):
	while True:
		ops = raw_input("Please Enter Command Here: ")
		if ops == 'maxinet':
			print("<=====================>")	
			print("Enter Maxinet Environment")	
			exp.CLI('./', './')
			print("Exit Maxinet Environment")
			print("<=====================>")		
		elif ops == 'show mode':
			print("<=====================>")
			print("Current mode is %s" % mode)
			print("<=====================>")

		elif ops == 'show status':
			
			print("<=====================>")
			print("%s paths are available!")
			print("<=====================>")
		elif ops == 'exit':
			print("<=====================>")
			print("Going to Exit Simulation")
			print("<=====================>")

			break
		else:
			print("<=====================>")
			print("Unrecognized Command!")
			print("<=====================>")
