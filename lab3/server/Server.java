/* William Uddmyr - wilud321 
   Samuel Larsson - samla949 */

import java.io.*;
import java.net.*;
import javax.net.ssl.*;
import java.security.*;
import java.util.StringTokenizer;
import java.nio.file.*;

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
            sss.setNeedClientAuth(true);
            sss.setEnabledCipherSuites(sss.getSupportedCipherSuites());
			
			System.out.println("\n>>>> Server: active ");
			SSLSocket incoming = (SSLSocket)sss.accept();
            
            DataOutputStream out = new DataOutputStream(incoming.getOutputStream());
            DataInputStream in = new DataInputStream(incoming.getInputStream());

            int optionFromClient;
            int fileNameLength;
            String fileName;
            
            while ((optionFromClient = in.readInt()) != 0) {
                System.out.println(optionFromClient);
                switch (optionFromClient) {
                    case 1: 
                        fileNameLength = in.readInt();
        
                        if(fileNameLength > 0) {
                            byte[] data = new byte[fileNameLength];
                            in.readFully(data, 0, fileNameLength);
                            fileName = new String(data);
                            
                            System.out.println(fileName);
                            File file = new File(fileName);
                            
                            byte[] message = Files.readAllBytes(file.toPath());         
                            System.out.println(message);

                            out.writeInt(message.length);
                            out.write(message);
                            System.out.println("Downloaded!");
                        }

                        break;
                    
                    case 2:
                        fileNameLength = in.readInt();
                        if(fileNameLength > 0) {
                            byte[] data = new byte[fileNameLength];
                            in.readFully(data, 0, fileNameLength);
                            fileName = new String(data);
                        
                            int fileLength = in.readInt();
                            if(fileLength > 0) {
                                byte[] file = new byte[fileLength];
                                in.readFully(file, 0, fileLength); 
                                Files.write(new File(fileName).toPath(), file);
                            }
                        }
                        break;
                    
                    case 3: 
                        fileNameLength = in.readInt();
        
                        if(fileNameLength > 0) {    
                            byte[] data = new byte[fileNameLength];
                            in.readFully(data, 0, fileNameLength);
                            fileName = new String(data);
                            Files.deleteIfExists(Paths.get(fileName));
                        }
                        break;
        
                    default:
                        break;
                }
            }
            incoming.close();
		} catch(Exception x) {
			System.out.println(x);
			x.printStackTrace();
		}
    }

    public static void main(String[] args) {
        Server s = new Server();
        s.start();
    }
}