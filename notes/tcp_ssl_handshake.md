## 1. TCP Handshake - Setup (3 way: SYN - SYNACK - ACK)
![tcp_handshake_setup](https://media.geeksforgeeks.org/wp-content/uploads/TCP-connection-1.png)

1. (SYN): In the first step, the client wants to establish a connection with a server, so it sends a segment with SYN(Synchronize Sequence Number) which informs the server that the client is likely to start communication and with what sequence number it starts segments with
2. (SYN + ACK): Server responds to the client request with SYN-ACK signal bits set. Acknowledgement(ACK) signifies the response of the segment it received and SYN signifies with what sequence number it is likely to start the segments with
3. (ACK): In the final part client acknowledges the response of the server and they both establish a reliable connection with which they will start the actual data transfer

### 1.1 (TLS) TCP Handshake - Setup
![tls_handshake](https://media.geeksforgeeks.org/wp-content/uploads/20200713225340/Diagram.png)

1. With a TLS enabled service, a sender sends a ClientHello (as referred in protocol). This includes information about Client.
2. Then server responds with ServerHello message (selecting highest version of TLS supported by Client) and then chooses a cipher suite from list in ClientHello message. The server also transmits its Digital certificate and a final ServerHelloDone message.
3. Client validates certificate. Client then sends ClientKeyExchange message. Here client chooses a key exchange mechanism to securely establish a shared secret with server. Client also needs to send ChangeCipherSpec indicating that it is switching to secure communication now, which is finally followed by Finished message for indicating a successful handshake.
4. Server replies with ChangeCipherSpec and an encrypted Finished message once shared secret is received.

Session key is Shared Symmetric Encryption Key used in TLS sessions to encrypt data being sent back and forth.

## 2. TCP Handshake - Termination (4 way- FIN - ACK - FIN - ACK)

![tcp_handshake_termination](https://media.geeksforgeeks.org/wp-content/uploads/20220406111342/TheFourWayHandshakeProcess.jpg)

1. Host A → Host B: FIN flag set.
2. Host B → Host A: ACK flag set.
3. Host B → Host A: FIN flag set.
4. Host A → Host B: ACK flag set.
