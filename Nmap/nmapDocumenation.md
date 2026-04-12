# NMap (Network Mapper)

- It is a recconiaossance (foot printing) tool, used to find information on the traget. 

- eg - IP, Open ports, website

- very noicy scanner -> easily detectable by firewalls, servers etc

- ***MAKE SURE TO DO IT ANONYMOUSLY***

- **nmap basically deals with `TCP` and `UDP` ports**

---

One IP can have many ports.

1 IP can have :
- 65535 TCP ports
- 65535 UDP ports
	
so one IP can have :
- A port 22 
- A port 80 
- A port 443 
- etc etc  -> in all a servcie (applicaiton) might be running
	
Important ports to look for -> `SSH`, `HTTP`, `HTTPS`, `echo`, `mySQL` etc

**Use -F to access the most commonly targeted ports** (100 ports by default)
	
Example:
> nmap -F scanme.nmap.org
- `-F` -> fast

---

## SCANNING

- Scanning is typically conducted after extensive passive reconnaissance is completed.

- ### **Objective** - identify active target and potential access vector in form of ports and services.
	    
- no exploitation or gaining of access | focus on building the profile of the target.
    - Info like OS version, service version, stack misconfiguration


### Tpye of Scanning:

1. **Network scanning :**

	- process of identifying active host on a target network.
    
    - goal is to create detailed schema of network infrastructue.	
		
	- *example* 
        - how host are connected with eachother.
        - connected to resource like a file server, email server etc
		 
2. **Port Scanning :**

	- probing the traget with a specific TCP flags.

    - Goal - enumerating the running services and their ports.


## TCP Flags:

- found in TCP header.

- responsible for transmission and flow of packet accross the network

- **port scanning** use these TCP flags (especially crafted).

- Used to determine:
    - the OS in use.
    - service versions
    - check for firewall etc.

### Flags :


Flags | Usage 
----|----
URG (urgent)| packet to be proccessed immediatly 
PSH (push) | transmit data immediatly 
FIN (finish) | no further tranmission
ACK (acknowledgement) | ack recieved packets
SYN (synchonization) | inititalize a connection btn host and targets
RST (reset) | reset the connection (cuts the connection)

---
#### <u>TCP 3 way handshake</u> :

`SYN` ---- `SYN-ACK` ---- `ACK`

- In **full scan** :
    - TCP 3-way handshake is established 
    - and response by the targets tell the versions details

- In **stealth scan** :  
    - SYN and `SYN-ACK` is send.
    - and then the nmap sends a `RST` to end the handshake process. 
---

### <u>TCP CONNECT SCAN</u>  `-sT`:

> host sends SYN ---> target respond with SYN-ACK ---> host send ACK ---> connection is then reset (RST)

- A 3-way connection is established 

- used for more accurate results related to OS and service version information (enumaration)

- disadavantages:
    - very slow scan -> connect to every port individually -> TCP - connection with every port 
    - very noicey scan- very easy to detect as it is a full scan 
    - firewall can prevert 
    
- **RARELY USED**

- example:
    >  nmap -sT 192.168.10.1

### <u>Stealth Scan</u> (or) <u>half open scan</u> `-sS` :

> SYN by host ---> SYN-ACK by target ---> RST by host
	
- reduce the scan time

- nmap waits for the response from the target -> response will conclude if the port is open/closed, service running etc etc
	
- example:  
	> sudo nmap -sS 192.169.10.2					

### Verbose `-v` :

> nmap -v -A scanme.nmap.org

- `-v` : versbose mode -> shows real time detials
	- version number
	- address name
	- which host is being scanned 
	- timings etc.

- `-v` -> verbose
- `-vv` -> more verbose
- `-vvv` -> maximum verbose 

### Agressive scan `-A` :
- enable Scans for:
 	- OS
	- version detection
	- script scanning, traceroute

### Range IP scan :

> nmap -v -sn 192.168.0.0/24 10.0.0.0/8 

### Ping Scan `-sn` :

- ping scan 

- Scan No port 

- only scan ping 

- ping sweep 

- **host discovery** 			

- best used for knowing the **host details** running on the network

 - Nmap will:
	- Send ICMP Echo Request (ping)
	- Send ARP request (if local network)
	- Send TCP SYN to port 443 or 80 (if ICMP blocked)
	- But it will **NOT** check open/closed ports.
	
- More reliable than pinging the broadcast address because many hosts do not reply to broadcast queries.
	
- windown servers have **firewall** config setup -> can block incoming ICMP echo request -> **can't discover host** 
			
### No Ping `-Pn` : 

- disabling host discovery

- no ping

- **only port scan**

- asumes the target is live and start the port scan directly | no pinging 
	       
- by default nmap only perform heavy probing (like - port scan, version detection, OS detection) on ports that are up.
	       
- but with this option it will perform heavy scan on the all `IPs specifed 
	       
- why used?
	- some network block ICMP ping / drop echo reply
	       
- when to use?
	- scanning firewall enabled servers
	- cloud server
	- ICMP blocked 
	- many host appear down on normal scan 
	- when doing PT (stealth)
	       
- downside?
	- slow (scan even dead host)
	- generate more traffic
	- less accurate in large netwok
	
- host discovery is skipped by `-sL` and `-Pn`
	
- why skip ping scan ?
	- sometimes up, but highly protected / firewalled.
	- port does not reply to the ping request.
	
---

by default nmap scan upto 1000 ports
max 6500 ports 

as a hacker you dont need that -> waste of time -> port scan must be specific 

---

open ports -> it is a port that is having a service/app running on it and it is listening for requests -> reply with SYN/ACK

close ports -> it is a port that has no service/app running on it (nothing is listening on that port) -> reply with RST (reset)

filtered ports -> prots then send no reply as they are blocked using firewall (no response - icmp blocked)

---------------------------------------------------------------------------------------------------------------------------------------
SAVE THE OUTPUT IN A PRINT PREETY WAY:

	GRAPPABLE OUTPUT (-oG) -> an output that can be easily searched and filtered by tools like grep, awk, sed etc

		eg-> nmap -vv -oG ./Desktop/gnmapscan 192.168.1.0-255 -> how this command is working?
	
			nmap will scan 1000 ports one by one and check for any open ports	

GRAPPABLE IS DEPLETE NOW. USE XML OUTPUT

	XML output: (-oX)

		eg-> nmap -vv -oX ./Desktop/gnmapscan 192.168.1.0-255 

Format		Command		Notes

XML		-oX		Best replacement for greppable
JSON		-oJ		Modern automation-friendly
Normal		-oN		Human-readable
All formats	-oA		Generates everything

---------------------------------------------------------------------------------------------------------------------------------------- 
AGGRESSIVE SCAN (-A) :
	
	enable OS detection, version detection, script scanning. traceroute
	
	eg-> nmap -A -v scanme.nmap.org  
	
------------------------------------------------------------------------------------------------------------------------------------------------------------------
service version (-sV):
	tells not just what port is open, but also 
	what services and its version running on it.

how is it helpful?
	While attacking you need the specific details of the services running on the open port and its version

-------------------------------------------------------------------------------------------------------------------------------------------------------------------
only see open ports:
	(--open)
	
	eg -> nmap --open nmap.scanme.org 
	
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
ZENMAP: 
	created by NMAP team | GUI version of nmap
	
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
timing and performation:
	
	Timing		Name		Speed		Usage
	
	T0		Paranoid	Very slow	Avoid detection / IDS evasion
	T1		Sneaky		Slow		IDS evasion
	T2		Polite		Moderate	Reduces network load
	T3		Normal		Default		Balanced
	T4		Aggressive	Fast		Good for local networks / reliable connections
	T5		Insane		Very fast	Risky, may miss results

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
operating System detection (fingerprinting):
	
	-O (capital O)
	
	how nmap id a OS?
		TCP/IP stack behaviour
		packet response 
		TTL values
		window size
		protocols 
		
	fails when?
		host has a firewall
		too many ports filtered
		target drop unusal packets
		
	example:
		nmap -O 192.168.1.1
		nmap -O -p- 192.168.1.1 	->	this will scan all 65535 ports
		nmap -O -p 80 192.168.1.1	->	this will scan OS detials of port 80

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
UDP scanning:	
	
	UDP - connectionless
	no SYN-ACK flags involved 
	
	ICMP echo is used 	
	
	eg - DNS, SNMP, TFTP
	
	very dificult protocol to analyse 
	
	port is open - no response from the target system
	port closed - 'icmp destination/port unreachable' response
	
	-sU 
	    -> for UDP scan. 
	    -> keep in mind to use sudo (root privilage) to run this scan 
	    -> why ?
	    -> coz UDP scan send a custom emtpy UDP packet which only root access user can create 
	    -> and UPD scan result depend on ICMP reply (port unreachable in case of port is closed) and ICMP reply can be heard only by root user  
	example -> sudo nmap -sU 192.168.10.2
	
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

HOST DISCOVERY:

	1. -sn -> scan No port 
		  it does a ping scan - used for descovering hosts in network - nothing more than that.
		  
		  1.1. nmap -sn 172.16.38.129 -> this give give host details of this IP only
		  
		  
		  1.2. if check host details for range of IP:
		  	
		  	nmap -sn 172.16.38.0/24   ---> this is going to scan all the IP from 172.16.38.0 to 255
		  	
		  	nmap -sn 172.16.38.1-100  ---> this is going to scan all the IP from 172.16.38.1 to 100
		  	
		  	nmap -sn 172.16.38.0/24 --exclude 172.16.38.2 ---> this is going to scan all IP except 172.16.38.2
		  	
		  	
		  	nmap -sn -iL fileWithListOfIP.txt   
		  				---->  this will ping scan for host details all the IP that are present in the file list
		
		  				-iL <inputFileName> -> input from the list of Host and Network 
		  				
		  				using a '-' after the -iL option will enable you to enter standard Input. no file name needed
		  						exmaple -> echo 192.168.1.10 | nmap -iL -
									   cat ips.txt | grep "192.168" | nmap -iL -
									   seq 1 10 | sed 's/^/192.168.1./' | nmap -iL -

		  		
		  	nmap -sn 172.16.38.0/24 --excludefile fileIPexcludeList.txt 
		  				----> this will ping scan all the IP in the specifed domain but exclude the Ip present in the file
		  				
		  				--excludefile <exclude_file> -> exclude the list from the file
		  				
	
	allowed IP ranges:
		nmap -sn 172.16.38.0/24
			 172.16.38.31/24   -> this will also scan all the IP from 172.16.38.0-255
			 172.16.38.0-255 
			 172.16.38.-       -> this '-' itself means start is 0 and end is 255
			 172.16.38.2-      -> this means range is from 2 to 255 
			 172.16.38.-100    -> this means range is from 0 to 100
			 172.16.1-20.15-40 
			 172.16,17,19-20.199.24 -> octate 2nd me 16,17,19 to 20 tak ke IP will be scanned  tec
			 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Host discovery technique:
			
	before, finding an host online against Ip address was easy -> send an ICMP echo request and wait for the response -> firewall rarely blocked these requests
		reason - every host had an ICMP echo server function -> received and sent response
		
	now, not the case -> ICMP ping messages are blocked by firewall
	
		hosts can no longer be assumed unavailable based on failure to reply to ICMP ping probes.
		
		example -> nmap -sn -PE -R -v microsoft.com ebay.com citibank.com google.com \slashdot.org yahoo.com
		
				-PE -> ICMP-only(Echo) Ping scan (no other function of -sn is used)
	
				
	1. TCP SYN Ping (-PS<port list>) ------>
						sents an empty TCP packet with SYN flag set.
						default destination - port 80
						alternate port as parameter
						
						ex -> -PS22-25,80,113,1050,35000
							
						----> nmap -sn -PS80 -R -v microsoft.com ebay.com citibank.com google.com
						
						how it works:
							nmap try to establish a connection with target system
							if closed -> target port sent - RST flag set packet
							if open -> TCP 3 way handshake will take place by target sending SYN/ACK TCP packet
								   and host will send a RST to terminate the connection before full 3 way handshake
							
							in unix/linux -> only root(priviliged user) can send TCP raw packet 
							
							when you run Nmap without root, it cannot craft low-level packets like SYN pings.
							So it uses a workaround:
								It uses the connect() system call
									this sends a normal TCP SYN packet created by OS (not raw packet)
							
							eg ->	nmap -sn 192.168.1.10
								
								nmap calls - connect(192.168.1.10:80)	-> OS sents a syn packet
								
								1. if, target reply -> RST (conneciton refused)
									OS report to nmap -> connect: ECONNREFUSED
								   	nmap read this as host is alive.
								   	
								2. if, target reply -> SYN/ACK
									OS report to nmap -> connect : success
									nmap read this as host is alive
									
								3. if, target reply -> no reply till timeout
									OS report to nmap -> connection : timeout
									nmap reas this as host if offline
									
						this fails when router/firewall are configued with a rule where incoming SYN packet is blocked
						in such a case, the target can send SYN packets but not recieve one. 
						therefore not establishing any TPC connection from outside 
						
						this is where TCP ACK ping does the job;
		
	2. TCP ACK ping (-PA<port list>) ------>
						TCP ack flag is send when the packet is sent from NMAP host to target ports.	
						
						the ACK packet is purporting to acknowledge data over an established TCP connection, that does not exist
						hence RST packet is sent by the target proving it(host) is indeed online 	
						
						rest all the rules are same as TCP SYN ping		
						
						ACK probe fails when a firewall is configued with stateful rules. 
							if an packet ACK comes unexpectedly, it will be dropped 
							need to first estblish a connection then only ACK is acceptable 
							no first ack is acceptable 
	
	3. UDP ping (-PU<port list>) ---------->
						sends UDP packet to given ports
						
						default ports are 40, 125
							A highly uncommon port is used by default because sending to open ports 
							is often undesirable for this particular scan type.
						
						if port closed -> ICMP port unreachable packet is sent in return. -> machine is up and running
						if host/network unreachable or TTL exceeded -> machine is offline.
						if port is open -> mostly UPD request wont get any response from the ports 
								   even if some port is open and services reply, nmap will know the machine is open
						
						by pass firewal and filter that only screen TCP
						
						ex -> nmap -PU53 172.16.38.129 ------> this is bad scan as 53 is a DNS port number and this ping wont 
										       return any response. nmap wont know the host is up or not 
										       better do it on uncommon ports
						
	
	4. ICMP ping types (-PE, -PP, -PM) ----->
						-PE -> ICMP Echo request | ICMP-only packet sent (code8) | reply -> code14
						-PP -> ICMP timestamp request -> code13 | reply -> code14
						-PM -> ICMP subnetmask request -> code17 | reply -> code18
						
						 These two queries can be valuable when administrators specifically block echo request packets, 
						 but forget that other 	ICMP queries can be used for the same purpose.
						 
	5. IP Protocol Ping (-PO<protocol list>) ->
						 sends IP packet with the specified protocol number on its IP header
						 if no protocol list is specified it will send IP packet to ICMP (protocol 1), IGMP (protocol 2), IP-in-IP (protocol 4)		
	
	6. ARP ping  (-PR) ------------------------> 	
						  scan an ethernet LAN
						  
						  work on local network | assume you are in the targets network, thn this scan is used
						
						  -----> nmap -n -sn --send-ip 192.168.33.37
						
							-> --send-ip  = send IP level packet (not ethernet level)
							-> 3 ARP packet will be set to elicit a response, before giving up the host
						  		ARP packet is sent because IP packet need to know the destination MAC of the machine/port
						  		
						  	why this way (sending raw IP packet) is bad?
						  		1. linux OS sents 3 ARP packet to know the MAC. 1sec apart.
						  		   nmap send ARP request to 16 million IPs for ip range 10.0.0.0/8 -> delay increased max 
						  		
						  		2. when destination host is unresponsive, the source host generally adds an incomplete entry for that
						  		   destination IP in the kernel ARP table -> ARP table fill up - problem starts 
						  		
						  		ARP scanning resolves both problems by putting Nmap in control.
						  			nmap issue raw ARP request | handles retransmission and timeout periods
						  			system ARP cache is bypassed
						  			
						  -----> nmap -n -sn -PR --packet-trace --send-eth 192.168.33.37            -> better to use this
						  
						  		-> neither the -PR or --send-eth options have any effect. 
						  		This is because ARP is the default scan type when scanning 
						  		ethernet hosts that Nmap detects are on a local ethernet network.
						  
						  ARP scan is much efficient and accurate -> host can block IP biased ping but not ARP request

	Default combination:
	
		If none of these host discovery techniques are chosen, 
			for Windows or privileged (root) Unix users 	
				if host/attacker out the network -> -PE -PS443 -PA80 -PP arguments
				if host/attacker is inside the network -> ARP scan is used.
			
			for unprivileged Unix shell users -> -PS80,443 
			
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
host discovery stratigies:
	
	different option flag related to ping scanning:
	
		-v -> --verbose
			default nmap -> print only active/resposive hosts
			verbose -> print more info 
			
			
		-g -> --source-port <port number>  
			force nmap to use a specific source port number when sending packets
			
			why this helps in finding the host?
				many firewall allow trusted source ports
				some IDS/IPS dont detect traffic of trusted source
				network admin - Testing firewall rule accuracy
			
			-----> nmap --source-port 53 -sS 192.168.1.10		// source port will be 53 
		
		
		-n -> DNS resolution for none of the target host
		
		
		-R -> DNS resolution for all the host, even the down ones
		
		
		--dns-server <server1>[,<server2>] -> 
			By default Nmap will try to determine your DNS servers (for rDNS resolution) from your resolv.conf file (Unix) or the Registry (Win32). 
			this option dont work with 
					--system-dns option 
					IPv6 scan.
			using mutliple DNS server -> stealth , fast
			
		
		--data-length <length> -> add <length> byte to packet to every packet
					  work on -> TCP, UDP, ICMP scan (privileged user + IPv4 scan only)
					  make packet look more legit -> some IDS (like snort) block zero byte ping packets
					  <length> -> 32 -> best for echo packet from window
					  	      56 -> best for ping packet from unix
				
		
		--ttl <value> ->
				for privileged users doing IPv4 scans only
				used for safty -> scan to not propogate beyond local network 
				prevent from routing loops - reduce router CPU load.
		
		
		canned timing options (-T4, -T3, -T5 etc) ->
							    higher the T value - speedy the scan is.
		
		
		--max-parallelism, --min-parallelism <value> ->
							       default - 2 ping probe at same time.
							       number of machine being scanned in parallel
							       
							    
		--min-rtt-timeout, --max-rtt-timeout, --initial-rtt-timeout <time> ->
		 									how long will nmap wait for ping response
		 									round trip timing 
		 
		 
		--randomize-hosts ->  
					suffling the host scan order - makes the scan less conspicuous.
					scan output - difficult to follow
		
		
		--reason ->
				normal Nmap output indicates whether a host is up or not, 
				but does not describe which discovery test(s) the host responded to.
				
				
		--packet-tracer ->
				  more detaited output than --reason provides
				  show every packet sent and received + sequence numbers + TTl value + TCP flags 
				  the most effective way to explore Nmap's behavior 
				  
				  
		--D <decoy1,decoy2,..> ->
					for privileged IPv4 scan
					camouflaging the true attacker
					
					
		-6 ->
			TCP connect-based ping scan (-PS) support IPv6 protocol
			
		
		-S <source IP address> , -e <sending device name> ->
								    as with other function of nmap, the source address and sending device 
								    can be specified with these options.
				
								    
LIST OF BEST HOST DISCOVERY PROBES:	
				    
			Hostsfound	   	Probe
			62.47%			-PE
			44.17%			-PS443
			43.28%			-PA80
			43.01%			-PA443
			42.47%			-PS80
			40.65%			-PA110
			40.42%			-PA3389
			40.41%			-PS110
			39.89%			-PA22
			39.62%			-PS21
			39.62%			-PA21
			38.75%			-PS22
			37.50%			-PS3389
			36.66%			-PP
			31.17%			-PU40125 --source-port 53 --data-length 24
			29.96%			-PU31338 --source-port 53 --data-length 24
			29.05%			-PU631 --source-port 53 --data-length 24
			26.38%			-PU40125
			26.09%			-PS25
			25.69%			-PA25
			25.35%			-PU31338
			24.71%			-PU631
			24.15%			-PU53 --source-port 53 --data-length 24
			22.20%			-PU53
			9.09%			-PO2
			9.03%			-PO150
			7.20%			-PO4
			4.21%			-PM
			

Best host discovery probe combinations ->
 
					Hosts found		Probe combination
			1 		probe			62.47%	-PE
			2		probes			77.61%	-PE -PA80
			3 		probes			83.83%	-PE -PA80 -PS443
			4 		probes			88.64%	-PE -PA80 -PS443 -PP
			5 		probes			91.12%	-PE -PA80 -PS443 -PP -PU40125 --source-port 53
			6 		probes			92.42%	-PE -PS80 -PS443 -PP -PU40125 -PA3389 --source-port 53
			7 		probes			93.10%	-PE -PS80 -PS443 -PP -PU40125 -PS3389 -PA21 --source-port 53
			8 		probes			93.69%	-PE -PS80 -PS443 -PP -PU40125 -PS3389 -PA21 -PU161 --source-port 53
	
	
	
ping option that will catch vast majortiy of host   ->  -PE -PP -PS21,22,23,25,80,113,443,31339 -PA80,113,443,10042 --source-port 53


default ping scan  -->  icmp echo request, tcp syn to port 443, tcp ack to port 80, icmp timestamp request   


in secuirty audit  -->  start with TCP analysis with port scab against most common 1000 ports with comprehensive ping scan options
			also launch -Pn (ping disabled) scans against all 65K TCP ports in the background 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------			
	-iR <num_of_random_hosts> ---> input random Host/IPs | useful for research and secuity study, internetwide scanning, collecting data
	
					⚠️ Warning (Important):
						Random scanning can:
						Trigger intrusion detection systems		
						Hit protected networks
						Be considered hostile activity
					
			ex -> nmap -iR 5   --> this will scan random 5 IP from the internet 
			      nmap -iR 0   --> this will scan random unlimited IP from the internet	
	
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	Nmap offers a dry run using the list scan (-sL option). 
	print out the target hosts and exit prior to even sending ping probes 
	
	Simply execute
	 
		nmap -sL -n <targets> 			| -n -> no DNS resolution -> by default, DNS resoultion enabled 
	
	to see which IPs would be scanned before you actually do it.
	
	Whether to scan corporate parents, siblings, service providers, and subsidiaries is an important issue that should be worked out with the customer in advance.
	
----------------------------------------------------------------------------------------------------------------------------------------------------------------------		
IPv6 scan:	
	 
	 nmap -6 2001:800:40:2a03::3  ---> Scans the IPv6 host at address 2001:800:40:2a03::3
	 
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Finding an Organization's IP Addresses:

	ALWAYS DOUBLE CHECK THE LIST OF IP ADDRESSES YOU HAVE RECEIVED TO SCAN ON.
	
	
	step1 - query the DNS record:
			host -t ns target.com    | -t -> type of DNS     | ns -> name server record
			host -t a target.com	 | a -> A record (ipv4)
			host -t aaaa target.com  | aaaa -> AAAA record (ipv6)
			host -t mx target.com	 | mx -> mail server record
			host -t SOA target.com   | Start of authority
			host -t CNAME target.com | Canonical names
			host -t txt target.com   | text record 
	
	step2 - resolve the IP of NS server
			host ns1.target.com
			host ns2.target.com
	
	step3 - check common subdomain
			host www.target.com
			host ftp.target.com
			host mail.target.com
			host smtp.target.com
			host dev.target.com
			host test.target.com	
			host vpn.target.com
			
			host smtp01.target.com
			host smtp02.target.com
			host ns3.target.com
			
	step4 - try zone transfer 
			-> DNS server sends a complete copy of its DNS record to another server
			-> it exists for a legitimate reason: to synchronize DNS data between primary and secondary DNS servers - DNS redundency 
			
			-> A zone file contains every DNS record for the domain, such as:
				A, AAAA
				MX
				NS
				TXT
				CNAME
				SRV
				SOA
				ALL subdomains (public + hidden/internal)
			
			=> dig AXFR target.com @ns1.target.com   | Ask ns1.target.com to give me the full zone for target.com.
			
	step5 - check which IP is part of source and which is not
			traceroute
			DNS reverse-resolution 
			whois
			
			=> nmap -Pn -T4 --traceroute www.target.com
			
			=> whois 207.171.166.49
			
			can use website as well for this task - netcraft DNS search - http://searchdns.netcraft.com/?host

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
DNS Resoultion:

	a great source of information of online host is DNS.
	
	organization - asign name which discloses the function of DNS.
			wireless access point - WAP
			firewall - fw, fw-1
			development webserver - dev, staging, www-int, beta	
			
	by default - nmap perform reverse DNS resolution 
		   - -Pn -> will skip host discovery - resoultion is performed on all IPs
		   
	parallel stub reslover -> for sleeping up DNS resolution
		   
		   
	Nmap and DNS:
		
		-n -> (no DNS resoultion) 
		
		-R -> dns resolution for all the target ip (online or offline)
		
		--system-dns -> by default nmap uses its built-in dns resolver - fast and predictable
					Sends DNS queries directly to the configured DNS server
					minimal traffic
			     ->	uses system(os) DNS resolver
			     		used for IPv6 scans 
			        	very slow
			        		coz DNS resolution now go es through:
							/etc/resolv.conf
							systemd-resolved
							NetworkManager
							mDNS / LLMNR
							DNS cache
							VPN DNS
							DoH (if enabled)
			     -> why use system dns?
			     		to match real system behaviour (system might use mDNS, corporate DNS rules, VPN DNS etc)
			     		avoid firewall detection - some firewall allow DNS via system service | block raw DNS queries
			     		scan internal domain - only system reslover knows about the internal network
			        	
			
		--dns-servers <ser1> <ser2> ... -> serves to use for DNS resolution 	
						-> By default, Nmap determines your DNS servers (for rDNS resolution) 
						   from your resolv.conf file (Unix) or the Registry (Win32).
						-> improve stealth -> as request can bounce off like any other recursive DNS server on the internet.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
nmap by default first perform ping scan, 
	then all other, like port scan, os detection, NSE, version detection on online found machines,

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
port scanning:				refer "scan technique" in nmap documentation 

	state - 
		open
		closed
		filtered
		unfiltered
		open|filtered
		closed|filtered
		
	ports - are software abstraction used to distingush btn communication channel. | 16 bits | 65535 ports allowed
										| port 0 - invalid - used as a wildcard (use any port) - eg-> source port is set of 0 
	
	nmap uses protocol -> TCP and UDP which uses port 
	
	nmap comes with 'namp-servcie' file - contains 
		-> well known ports and thier services
		-> some unregistred ports (not reg with IANA) and thier services 
		-> trojan backdoors ports 	
		
	port 0 -> invalid -> in theory, no service can run on it.
			  -> raw packet can be crafted using port 0 in the header
			  -> malicious trojan backdoors listen on and respond to port 0(destination port) packets
	
	by default, nmap dont allow port 0 scan 
	but explicity one can scan it 
		
		eg -> nmap -p0 nmap.scanme.org		// this will scan port 0 
							
			What happens if something responds on port 0? 	 ->	That’s a huge red flag 🚩
											Malicious backdoor
											Broken firewall / kernel bug
											Malformed packet handling issue		
											
	Well-known port -> 0-1023 (0 is excluded from scan) -> nmap, in unix (not windown), require root privilage to run this scan
							       (other application need root access as well to listen to or send packrts on these ports)
			   
	check range of port in ur linux OS:
					> cat /proc/sys/net/ipv4/ip_local_port_range
	change the range:
			> echo "10000 65000" > /proc/sys/net/ipv4/ip_local_port_range 
	



