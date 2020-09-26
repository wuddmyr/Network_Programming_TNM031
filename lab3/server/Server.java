/* William Uddmyr - wilud321 
   Samuel Larsson - samla949 */

import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.util.StringTokenizer;

import java.nio.file.Files;

public class Server {
    
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
			SSLServerSocketFactory sslServerFactory = sslContext.getServerSocketFactory();
			SSLServerSocket sss = (SSLServerSocket)sslServerFactory.createServerSocket(PORT);
			sss.setEnabledCipherSuites(sss.getSupportedCipherSuites());
			
			System.out.println("\n>>>> Server: active ");
			SSLSocket incoming = (SSLSocket)sss.accept();

      	    // BufferedReader in = new BufferedReader(new InputStreamReader(incoming.getInputStream()));
			PrintWriter out = new PrintWriter(incoming.getOutputStream(), true);			
            DataInputStream in = new DataInputStream(incoming.getInputStream());

            int optionFromClient = in.readInt();
            System.out.println("OptionClient==" + optionFromClient);

            switch (optionFromClient) {
                           
                case 1: 
         

                    break;
                
                case 2:
                    int fileNameLength = in.readInt();
                    String fileName = "haha.txt";
					if(fileNameLength > 0) {
                        byte[] data = new byte[fileNameLength];
                        in.readFully(data, 0, fileNameLength);
                        fileName = new String(data);
                        fileName = "test_" + fileName;
                    }
                
                    int fileLength = in.readInt();
                    if(fileLength > 0) {
                        byte[] file = new byte[fileLength];
                        in.readFully(file, 0, fileLength); //read message
                        Files.write(new File(fileName).toPath(), file);
                    }
                    break;
                
                case 3: 
                   


                    break;
                
                default:
                    System.out.println("CLIENTEN ÄR EN DISCGOLFARE, VAFAN..");
                    break;
            }

            // int l = in.readInt();
            // System.out.println(l);
			// if(l > 0) {
			// 	byte[] message = new byte[l];
            //     in.readFully(message, 0, l); //read message ?
                
            //     System.out.println(new String(message));
			// }
				
            
            incoming.close();
		} catch(Exception x) {
			System.out.println(x);
			x.printStackTrace();
		}
    }


	// download files



	// upload files



	// delte files





	
    
    public static void main(String[] args) {

        Server myserver = new Server();
        myserver.start();

        System.out.println("hata java");
    }
}