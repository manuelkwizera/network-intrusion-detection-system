# Network Intrusion Detection System
A Network Intrusion Detection System (NIDS) is a cybersecurity project designed to monitor and analyze network traffic for signs of malicious activities or security threats. It employs a combination of signature-based detection, which identifies known attack patterns, and anomaly-based detection, which identifies deviations from normal network behavior. The NIDS aims to detect and respond to potential intrusions in real-time, enhancing the overall security posture of a network by identifying and mitigating cyber threats.

# PACKET STRACTURE
Ether / IP / TCP 172.217.166.35:https > 192.168.43.94:33316 A

1. **Ether**: This indicates that the packet is encapsulated within an Ethernet frame, which is a common data link layer protocol used in local area networks (LANs).

2. **IP**: This indicates that the packet is using the Internet Protocol (IP) for network layer addressing and routing.

3. **TCP**: This indicates that the packet is using the Transmission Control Protocol (TCP) for transport layer communication. TCP provides reliable, ordered, and error-checked delivery of data between applications.

4. **172.217.166.35:https**: This is the source address and port number. The source IP address is 172.217.166.35, and it's communicating over the HTTPS (HTTP over TLS/SSL) protocol. The port number for HTTPS is 443.

5. **192.168.43.94:33316**: This is the destination address and port number. The destination IP address is 192.168.43.94, and it's communicating over an unknown protocol using port number 33316. The specific application or protocol associated with this port isn't mentioned here.

The above packet represents a TCP communication where a host with IP address 172.217.166.35 is sending data over HTTPS to a host with IP address 192.168.43.94 on an unknown protocol or application using port 33316.

# SAMPLE SIGNATURE FOR AN SQL INJECTION
Signature Name: SQL Injection Attempt
Description: Detects SQL injection attempts targeting web applications.
Signature Type: Network Traffic
Severity: High
Signature: HTTP URI contains: '; DROP TABLE users; --

Explanation:
This signature detects HTTP requests where the URI contains the string "; DROP TABLE users; --", which is a common payload used in SQL injection attacks. In SQL injection attacks, attackers attempt to execute arbitrary SQL commands by injecting malicious SQL code into input fields or query parameters of web applications.

# SAMPLE OF AN SQL INJECTION
Here's an example of what such an intrusion might look like in network packets:

1. **Normal HTTP Request**:
   - Method: GET
   - URI: /search.php?id=123
   - Host: example.com
   - User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/97.0.4692.71 Safari 537.36
   - Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
   - Accept-Language: en-US,en;q=0.9

2. **SQL Injection Attack**:
   - Method: GET
   - URI: /search.php?id=123'; DROP TABLE users; --
   - Host: example.com
   - User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36
   - Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
   - Accept-Language: en-US,en;q=0.9

In the second example, the attacker has injected malicious SQL code into the `id` parameter of the URI. The injected code `'; DROP TABLE users; --` is designed to manipulate the database by attempting to drop the `users` table. The semicolon (`;`) is used to terminate the legitimate SQL query, followed by the malicious SQL code to drop the table, and then `--` to comment out the rest of the query.
An intrusion detection system (IDS) with a signature-based approach would analyze network packets and detect the second request as a potential SQL injection attack based on the signature matching the SQL injection payload in the URI. It would then generate an alert or take appropriate action to mitigate the threat.
