/* William Uddmyr - wilud321 
   Samuel Larsson - samla949 */

import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.util.StringTokenizer;

//import java.nio.File;
import java.nio.file.Files;

public class Client {
    
    static final String HOST = "0.0.0.0";
    static final int PORT = 1337;
    static final String KEYSTORE = "LIUkeystore.ks";
    static final String TRUSTSTORE = "LIUtruststore.ks";
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
            
            BufferedReader socketIn;
			socketIn = new BufferedReader(new InputStreamReader(client.getInputStream()));
            
            //PrintWriter socketOut = new PrintWriter(client.getOutputStream(), true);
            DataOutputStream socketOut = new DataOutputStream(client.getOutputStream());

            BufferedReader userInput = new BufferedReader(new InputStreamReader(System.in));
            int option;
            
            while (true) {
                
                System.out.println("------Sammes menu------");
                System.out.println("Click 1: option 1 - download files");
                System.out.println("Click 2: option 2 - upload files");
                System.out.println("Click 3: option 3 - delete files");
            
                try {
                    option = Integer.parseInt(userInput.readLine());
                } catch (NumberFormatException e) {
                    option = 0;
                }

                socketOut.writeInt(option);

                switch (option) {
                           
                    case 1: 
                        System.out.println("Please enter the filename you want to download");

                        break;
                    
                    case 2:
                        System.out.println("Please enter the filename you want to upload");
            
                        String fileName = userInput.readLine();
                        File file = new File(fileName);

                        byte[] message = Files.readAllBytes(file.toPath());
                        System.out.println(message);

                        socketOut.writeInt(fileName.length());
                        socketOut.write(fileName.getBytes());
                        
                        socketOut.writeInt(message.length);
                        socketOut.write(message);
                        
                        System.out.println("Succesfully uploaded file: " + fileName);
                        break;
                    
                    case 3: 
                        System.out.println("Please enter the filename you want to delete");


                        break;
                    
                    default:
                        System.out.println("VÄLJ ETT NUMMER SOM EXISTERAR, PAJAS..");
                        break;
                }

            }



            // }
        //    SSLServerSocket sss = (SSLServerSocket)sslServerFactory.createServerSocket(PORT);
        //    sss.setEnabledCipherSuites(sss.getSupportedCipherSuites());
            
        //    System.out.println("\n>>>> Server: active ");
        //    SSLSocket incoming = (SSLSocket)sss.accept();

        //     BufferedReader in = new BufferedReader(new InputStreamReader(incoming.getInputStream()));
        //    PrintWriter out = new PrintWriter(incoming.getOutputStream(), true);			
            
        //    String str;
        //    while (!(str = in.readLine()).equals("")) {
        //        System.out.println(str);
                
        //        // double result = 0;
        //        // StringTokenizer st = new StringTokenizer( str );
        //        // try {
        //        // 	while( st.hasMoreTokens() ) {
        //        // 		Double d = new Double( st.nextToken() );
        //        // 		result += d.doubleValue();
        //        // 	}
        //        // 	out.println( "The result is " + result );
        //        // }
        //        // catch( NumberFormatException nfe ) {
        //        // 	out.println( "Sorry, your list contains an invalid number" );
        //        // }
        //    }
            
        //    incoming.close();
        } catch(Exception x) {
            System.out.println(x);
            x.printStackTrace();
        }
    }
        
    public static void main(String[] args) {

        Client myserver = new Client();
        myserver.start();

        System.out.println("hata java");
    }
}