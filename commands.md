##Commands:

#Shutdown Command (kapat):

Command: kapat
Action: Shuts down the machine running the RAT.
For Windows: Executes shutdown /s /t 0
For Linux/macOS: Executes shutdown -h now
File Creation Command (touch <filename>):

#Command: touch <filename>
Action: Creates an empty file with the specified filename on the system.
Example: touch newfile.txt will create a file named "newfile.txt".
General Command Execution:

#Command: Any valid shell command can be sent and executed by the RAT.
Action: Executes the provided command in the shell and sends back the output.
Error Handling:

#If the RAT cannot execute a command or encounters an error, it will send an error message with details.
Important Notes:

##This script is intended for educational purposes only.
Make sure you understand and comply with all relevant laws and regulations when using or sharing such scripts.
