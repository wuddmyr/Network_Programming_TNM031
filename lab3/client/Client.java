/* William Uddmyr - wilud321 
   Samuel Larsson - samla949 */

import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.util.StringTokenizer;
import java.nio.file.Files;

public class Client {
    
    static final String HOST = "0.0.0.0";
    static final int PORT = 1337;
    static final String KEYSTORE = "MYkeystore.ks";
    static final String TRUSTSTORE = "MYtruststore.ks";
    static final String KEYSTOREPASS = "123456";
    static final String TRUSTSTOREPASS = "abcdef";

    public void start() {
        try {
            KeyStore ks = KeyStore.getInstance("JCEKS");
            ks.load(new FileInputStream(KEYSTORE), KEYSTOREPASS.toCharArray());
            
            KeyStore ts = KeyStore.getInstance("JCEKS");
            ts.load(new FileInputStream(TRUSTSTORE), TRUSTSTOREPASS.toCharArray());
            
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            kmf.init(ks, KEYSTOREPASS.toCharArray());
            
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            tmf.init(ts);
            
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
            SSLSocketFactory sslFactory = sslContext.getSocketFactory();
            SSLSocket client = (SSLSocket)sslFactory.createSocket(HOST, PORT);
            client.setEnabledCipherSuites(client.getSupportedCipherSuites());
            System.out.println("\n>>>> SSL/TLS handshake completed");
            
			DataInputStream socketIn = new DataInputStream(client.getInputStream());
            DataOutputStream socketOut = new DataOutputStream(client.getOutputStream());

            BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));
            int option;
            
            while (true) {
                
                System.out.println("------ Lab 3: Secure Sockets ------");
                System.out.println("");
                System.out.println("Choose an option: ");
                System.out.println("Click 1 to download files");
                System.out.println("Click 2 to upload files");
                System.out.println("Click 3 to delete files" );
                System.out.println("Click 0 to quit");

                try {
                    option = Integer.parseInt(userInput.readLine());
                } catch (NumberFormatException e) {
                    option = 0;
                }

                socketOut.writeInt(option);
                String fileName;

                switch (option) {

                    case 0:
                        socketOut.writeInt(0);
                        client.close();
                        return;
                           
                    case 1: 
                        System.out.println("Please enter the filename you want to download");
                        fileName = userInput.readLine();

                        socketOut.writeInt(fileName.length());
                        socketOut.write(fileName.getBytes());

                        int fileLength = socketIn.readInt();
                        if(fileLength > 0) {
                            byte[] data = new byte[fileLength];
                            socketIn.readFully(data, 0, fileLength);
                            Files.write(new File(fileName).toPath(), data);
                        }
                        break;
                    
                    case 2:
                        System.out.println("Please enter the filename you want to upload");
            
                        fileName = userInput.readLine();
                        File file = new File(fileName);

                        byte[] message = Files.readAllBytes(file.toPath());
                        System.out.println(message);

                        socketOut.writeInt(fileName.length());
                        socketOut.write(fileName.getBytes());
                        
                        socketOut.writeInt(message.length);
                        socketOut.write(message);
                        
                        break;
                    
                    case 3: 
                        System.out.println("Please enter the filename you want to delete");
                        fileName = userInput.readLine();
                        
                        socketOut.writeInt(fileName.length());
                        socketOut.write(fileName.getBytes());
                        
                        break;
                    
                    default:
                        System.out.println("Error...");
                        break;
                }

            }
        } catch(Exception x) {
            System.out.println(x);
            x.printStackTrace();
        }
    }
        
    public static void main(String[] args) {
        Client c = new Client();
        c.start();
    }
}