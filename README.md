# GateWatch

Simple Port Scanner in Python. Which the sockets tries to create a connection with the host, if the connection is successfull the port is open, otherwise is closed.
Gate Watch also implements threads usage in order to increse the speed of the execution of the various connection tentatives.


The Gate Watch has a menu function:
1. Scan a host with the most used port for most know protocols
2. Scan a host for all the well-known ports (from 0 to 1023)
3. Scan a host for a range of ports specified by the user
4. Export the last scan results to a file text


### Further implementation: 
- GUI interface
- Implementation with a network scanner. Gate Watch takes the result of the network scanner as input to scan each host founded.
- Implementation of Vulnerability Scanner


