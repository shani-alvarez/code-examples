// ASK 2020 York Online Masters
// ---------UDPServer ---------
//  Socket communications UDP

//Based on the code provided in 2.4.1 Lesson & Activity: Socket Programming with UDP, CAMN module

// Imports required packages
import java.util.ArrayList;
import java.util.List;
import java.io.*;
import java.net.*;

class UDPClient {
	
	// Applies a sliding window of size 5 protocol to send UDP datagram packets
	public static void main(String[] args)  throws Exception {
		// Arguments of the main construct: (host name or address, port number)
		// Declares and instantiates the objects
		String host = null; // IP address or host name
		Integer portNumber = 0; // Port number
		Boolean status = true; // Status of the client socket
		int windowSize = 5; // Window size
		int originalWindowSize = 5; //Original window size
		int seqNumber = -1; // Sequence number
		
		// Retrieve the IP address or host name from the arguments. 
		// If none were found, the local host and port 9876 will be used.
		if (args.length > 0) {
		    try {
		    	host = args[0];
		    } catch (NumberFormatException e) {
		        System.err.println("Argument" + args[0] + " must be an IP address or a host name.");
		        System.exit(1);
		    }
		    try {
		    	portNumber = Integer.parseInt(args[1]);
		    } catch (NumberFormatException e) {
		        System.err.println("Argument" + args[1] + " must be a port number.");
		        System.exit(1);
		    }
		}
		else {
	    	host = "localhost";
	    	portNumber = 9876;
	    }

		// Instantiate the client socket and IP address variable with the input argument
		DatagramSocket clientSocket = new DatagramSocket();
		InetAddress ipAddress = InetAddress.getByName(host);
		
		// Read the file test.txt  
		String fileText = "";
		try {
			// file reader
	        FileReader file = new FileReader("./test.txt");
	        BufferedReader br = new BufferedReader(file);
	        fileText = br.readLine();
	        System.out.println("File contents: " + fileText + "\n");
	        br.close();
		    } 
		catch (FileNotFoundException e) {
		      System.out.println("File cannot be read.");
		      e.printStackTrace();
		}
        
		// Add characters in the file content to a list
		List<Character> chars = new ArrayList<>(); 
        for (char ch : fileText.toCharArray()) {
            chars.add(ch);
        }
		
     	//The sliding window protocol starts here
		while (status) {
			for (int i=0; i<windowSize; i++) {
				seqNumber += 1;
				// Convert the contents of the file to bytes
				String data = String.valueOf(chars.get(seqNumber));
				byte [] fileBytes = data.getBytes();
				// Print in the console the data being sent and its sequence number.
				System.out.println("Sending datagram with character " + data + "... \n");
				// Include the file's content and sequence number in the payload
				ByteArrayOutputStream os = new ByteArrayOutputStream( );
		        DataOutputStream dos = new DataOutputStream(os);
		        dos.writeInt(seqNumber);
		        dos.write(fileBytes);
		    	// Send the data packet to the server
				byte[] sendData = os.toByteArray();
				DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, ipAddress, portNumber);
				clientSocket.send(sendPacket);
				}
						
			// Receive the confirmation message from the server
			byte[] receiveData = new byte[7];
			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
			clientSocket.receive(receivePacket);
			String data = new String(receivePacket.getData());
			ByteArrayInputStream is = new ByteArrayInputStream(receivePacket.getData());
	        DataInputStream dis = new DataInputStream(is);
	        int confirmationSeqNumber = dis.readInt();
	        String confirmationChar1 = Character.toString(data.charAt(4));
	        String confirmationChar2 = Character.toString(data.charAt(5));
	        String confirmationChar3 = Character.toString(data.charAt(6));
	        String confirmation = confirmationChar1 + confirmationChar2 + confirmationChar3;
			// Conditional to check if the server acknowledgement and print the results
			if (confirmation.contentEquals("ACK") && confirmationSeqNumber < fileText.length()-originalWindowSize) {
					windowSize = 1;
					status=true;
					System.out.println("FROM SERVER: " + confirmation + " for datagram with sequence number " + confirmationSeqNumber);
			}
			else if (confirmation.contentEquals("ACK") && confirmationSeqNumber >= fileText.length()-originalWindowSize) {				
				// Receive the last confirmation message from the server
				status=false;
				System.out.println("FROM SERVER: " + confirmation + " for datagram with sequence number " + confirmationSeqNumber);
				for (int j=0; j<fileText.length()-originalWindowSize+1; j++) {
					// Receive the confirmation message from the server
					byte[] lastReceiveData = new byte[7];
					DatagramPacket lastReceivePacket = new DatagramPacket(lastReceiveData, lastReceiveData.length);
					clientSocket.receive(lastReceivePacket);
					// Include the file's content and sequence number in the payload
					String lastData = new String(lastReceivePacket.getData());
					ByteArrayInputStream lis = new ByteArrayInputStream(lastReceivePacket.getData());
			        DataInputStream ldis = new DataInputStream(lis);
			        int lastConfirmationSeqNumber = ldis.readInt();
			        String lastConfirmationChar1 = Character.toString(lastData.charAt(4));
			        String lastConfirmationChar2 = Character.toString(lastData.charAt(5));
			        String lastConfirmationChar3 = Character.toString(lastData.charAt(6));
			        String lastConfirmation = lastConfirmationChar1 + lastConfirmationChar2 + lastConfirmationChar3;
			        // Conditional to check the last acknowledged for the last sequence number
					if (lastConfirmation.contentEquals("ACK") && lastConfirmationSeqNumber != fileText.length()-1) {
							System.out.println("FROM SERVER: " + confirmation + " for datagram with sequence number " + lastConfirmationSeqNumber);
							
					}
					else if (lastConfirmation.contentEquals("ACK") && lastConfirmationSeqNumber == fileText.length()-1) {
						status=false;
						System.out.println("FROM SERVER: " + confirmation + " for datagram with sequence number " + lastConfirmationSeqNumber);
						System.out.println("All acknowledgements have been sent from the server.");
						// Client socket closes once all the content of the file and acknowledgements have been received
						System.out.println("Client socket will close now.");
						clientSocket.close();
					}
					else {
						status=false;
						System.out.println("Error, retransmission required.");
					}		
				}
			}  
			else {
				status=false;
				System.out.println("Error, retransmission required."); 
			}
		}
			
	}	
	
}