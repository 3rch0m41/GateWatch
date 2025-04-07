import socket
from pyfiglet import figlet_format
import time 
import re
import threading
from queue import Queue

ipAddressPattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
urlPattern = re.compile("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")
portRangePattern = re.compile("([0-9]+)-([0-9]+)")
global minPort, maxPort, target, targetIP
minPort = 0
wellKnownLimit = 1023

maxPort = 65535
portOpen = []
portClosed = []
well_known_ports = [20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 81, 88, 109, 110, 115, 118, 143, 443, 853]
q = Queue()

#Used to prevent duplicates entries from shared variables
print_lock = threading.Lock()

def validateTargetAddress ():
    global target, targetIp
    while True: #Request of user input and check with regex
        target = input("Enter Ip Address or URL to scan:")
        if urlPattern.search(target):
            targetIp = socket.gethostbyname(target)
        else:
            targetIp = target
        if ipAddressPattern.search(targetIp):
            print(f"{target} is a valid address")
            break

def validateTargetPortRange ():
    global minPort, maxPort
    while True:
        print("please enter the range of the ports you want to scan in format: <int>-<int> (i.e. 50-100)")
        portRange = input ("Enter port range: ")
        portRangeValid = portRangePattern.search(portRange)
        if portRangeValid:
            minPort = int(portRangeValid.group(1))
            max = int(portRangeValid.group(2))
            break


def scan (port):
    global targetIp
    try:
        sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.settimeout(0.5)
        res = sock.connect_ex((targetIp, port))
        if res == 0 :
            portOpen.append(port)
            sock.close()
        else:
            portClosed.append(port)
    except:
        pass
   
def threader():
    while True:
        worker = q.get()
        scan(worker)
        q.task_done()

def resultPrint ():
    portOpen.sort()
    portClosed.sort()
    for port in portOpen:
        print(f"Port {port} is open on {targetIp}.")

    for port in portClosed: 
        print(f"Port {port} is closed on {targetIp}.")


def menu ():
    
    print("\n                         Main Menu                              ")
    print("\n****************************************************************")
    print("1. Scan only the most used and common port of the host\n")
    print("2. Scan all the well-known ports of the host\n")
    print("3. Scan a specific port range of the host\n")
    print("9. Exit Gate Watch")

    while True:
        choice = input("Enter your choice (1-3 or 9): ")
        if choice == '1': 
            startTime = time.time()
            validateTargetAddress()

            print ("-"  * 80 )
            print ("                         Please Wait, Scanning the Host -> ", targetIp)
            print ("-" * 80)

            for x in range (99):
                t = threading.Thread(target=threader)
                t.daemon = True
                t.start()

            for worker in well_known_ports:
                q.put(worker)

            q.join()

            print("Time taken: ", time.time()-startTime)
            resultPrint ()

        elif choice == '2': 
            pass
            startTime = time.time()
            validateTargetAddress()

            print ("-"  * 80 )
            print ("                         Please Wait, Scanning the Host -> ", targetIp)
            print ("-" * 80)

            for x in range (99):
                t = threading.Thread(target=threader)
                t.daemon = True
                t.start()

            for worker in range(minPort, wellKnownLimit):
                q.put(worker)

            q.join()

            resultPrint ()
            print("Time taken: ", time.time()-startTime)

        elif choice == '3': 
            pass
            startTime = time.time()
            validateTargetAddress()
            validateTargetPortRange()

            print ("-"  * 80 )
            print ("                         Please Wait, Scanning the Host -> ", targetIp)
            print ("-" * 80)

            for x in range (99):
                t = threading.Thread(target=threader)
                t.daemon = True
                t.start()

            for worker in range(minPort, maxPort):
                q.put(worker)

            q.join()

            resultPrint ()
            print("Time taken: ", time.time()-startTime)

        elif choice == '9': 
            print("Goodbye! See you soon! ")
            break
        else:
            print("Invalid choice! Please try again!")


if __name__ == "__main__":

    print(figlet_format("GateWatch", font='drpepper'))

    print("\n****************************************************************")
    print("\n*           Copyright of Giulio Malini, 2025                   *")
    print("\n****************************************************************")

    menu()
