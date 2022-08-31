// ASK 2020 York Online Masters
// ---------UDPServer ---------
//  Socket communications UDP

//Based on the code provided in 2.4.1 Lesson & Activity: Socket Programming with UDP, CAMN module

// Imports required packages
import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.List;


class UDPServer {
	
	// Applies a sliding window of size 5 protocol to send UDP datagram packets
	public static void main(String args[]) throws Exception	{
		// Declares and instantiates the objects
		DatagramSocket serverSocket = new DatagramSocket(9876); // Datagram socket for the server
		byte[] receiveData = new byte[5]; // Byte object to receive data
		byte[] sendData = new byte[3]; // Byte object to send data
		int windowSize = 5; // Window size
		Boolean status = true; // Status of the server socket
		int seqNumber = 0; // Sequence number
		InetAddress IPAddress = null; // IP address
		int port = 0; // Port number
		String confirmation = ""; // Acknowledgement confirmation
		int firstSeqNumber =  0; // First sequence number in the sliding window
		List<Integer> seqNumberList = new ArrayList<>(); // Sequence number list (sliding window)
		
		// Prints the status of the server
		System.out.println("Server running..." + "\n");
		
		//The sliding window protocol starts here
		while(status)	{	
	        int lastSeqNumber = 0; // Last sequence number in the sliding window
			for (int i=0; i<windowSize; i++) {
				// Receives packet form the client program
				DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
				serverSocket.receive(receivePacket); 
				String data = new String(receivePacket.getData());
				IPAddress = receivePacket.getAddress();
				port = receivePacket.getPort();
				ByteArrayInputStream is = new ByteArrayInputStream(receivePacket.getData());
		        DataInputStream dis = new DataInputStream(is);
		        seqNumber = dis.readInt();
		        seqNumberList.add(seqNumber);
		        System.out.println("Sequence number that arrived: " + seqNumber);
		        String content = Character.toString(data.charAt(4));
				System.out.println("FROM CLIENT: " + content);	
				System.out.println("Current sequence number list: " + seqNumberList + "\n");
				lastSeqNumber = seqNumber;
			}
			// Conditional for different sizes of the sequence number list
			if (seqNumberList.size() > 1) {
				if (seqNumberList.get(0) == seqNumberList.get(1)-1) {
					confirmation = "ACK";
					firstSeqNumber =  seqNumberList.get(0);
				}
					else {
						confirmation = "NAK";
					}
				}
			else if (seqNumberList.size()==1 && seqNumberList.get(0) == lastSeqNumber) {
				confirmation = "ACK";
			}
			else {
				confirmation = "NAK";
			}
			// Conditional for different sequence numbers and confirmations, either ACK or NAK
			if (confirmation == "ACK" && lastSeqNumber < 7) {
				// Send packet with ACK or NAK confirmation
				status = true;
				byte [] confirmationBytes = confirmation.getBytes();
				ByteArrayOutputStream os = new ByteArrayOutputStream( );
		        DataOutputStream dos = new DataOutputStream(os);
		        System.out.println("Sending ACK for datagram with sequence number: " + firstSeqNumber + "\n");
		        dos.writeInt(firstSeqNumber);
		        dos.write(confirmationBytes);
		        byte[] sendConfirmation = os.toByteArray();
				DatagramPacket sendPacket = new DatagramPacket(sendConfirmation, sendConfirmation.length, IPAddress, port);
				serverSocket.send(sendPacket);
				windowSize = 1;
				seqNumberList.remove(0);
			}
			else if(confirmation == "ACK" && lastSeqNumber==7) {
				for (int j=0; j<seqNumberList.size()+2; j++) {
					if (seqNumberList.get(0) == seqNumberList.get(1)-1) {
						// Send packet with ACK or NAK confirmation
						confirmation = "ACK";
						firstSeqNumber =  seqNumberList.get(0);
						System.out.println("Current sequence number list: " + seqNumberList);
						byte [] confirmationBytes = confirmation.getBytes();
						ByteArrayOutputStream os = new ByteArrayOutputStream( );
				        DataOutputStream dos = new DataOutputStream(os);
				        System.out.println("Sending ACK for datagram with sequence number: " + firstSeqNumber + "\n");
				        dos.writeInt(firstSeqNumber);
				        dos.write(confirmationBytes);
				        byte[] sendConfirmation = os.toByteArray();
						DatagramPacket sendPacket = new DatagramPacket(sendConfirmation, sendConfirmation.length, IPAddress, port);
						serverSocket.send(sendPacket);
						seqNumberList.remove(0);
					}
					else {
						status = false;
						confirmation = "NAK";
						sendData = confirmation.getBytes();
						DatagramPacket sendPacketError = new DatagramPacket(sendData, sendData.length, IPAddress, port);
						serverSocket.send(sendPacketError);
					}
				}
				// Last confirmation for the last sequence number
				System.out.println("Current sequence number list: " + seqNumberList);
				status = false;
				confirmation = "ACK";
				byte [] lastConfirmationBytes = confirmation.getBytes();
				ByteArrayOutputStream los = new ByteArrayOutputStream( );
		        DataOutputStream ldos = new DataOutputStream(los);
		        System.out.println("Sending ACK for datagram with sequence number: " + lastSeqNumber);
		        ldos.writeInt(lastSeqNumber);
		        ldos.write(lastConfirmationBytes);
		        byte[] lastSendConfirmation = los.toByteArray();
				DatagramPacket lastSendPacket = new DatagramPacket(lastSendConfirmation, lastSendConfirmation.length, IPAddress, port);
				serverSocket.send(lastSendPacket);
				
				System.out.println("All datagrams have been acknowledged.");
				System.out.println("Server socket will close now.");
					
			}
			else {
				status = false;
				confirmation = "NAK";
				sendData = confirmation.getBytes();
				DatagramPacket sendPacketError2 = new DatagramPacket(sendData, sendData.length, IPAddress, port);
				serverSocket.send(sendPacketError2);
			}
		}
		// Server socket is closed
		serverSocket.close();
	}
	
}
	
