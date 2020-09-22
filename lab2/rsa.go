package main

import (
	"bufio"
	"crypto/rand"
	"fmt"
	"math/big"
	"os"
	"strings"
)

func getMessage() string {
	fmt.Print("INPUT MESSAGE: ")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	text = strings.Replace(text, "\n", "", -1)
	fmt.Print("THE MESSAGE: ", text, "\n\n")
	return text
}

func main() {
	// generate random primes (1024 bits) for p and q
	p, _ := rand.Prime(rand.Reader, 1024)
	q, _ := rand.Prime(rand.Reader, 1024)

	// calculate n
	n := big.NewInt(0).Mul(p, q)

	// calculate phi (q-1)*(p-1)
	phi := big.NewInt(0).Sub(big.NewInt(0).Set(p), big.NewInt(1))
	phi.Mul(phi, big.NewInt(0).Sub(big.NewInt(0).Set(q), big.NewInt(1)))

	// generate random prime (16 bit) for e
	// check if e is factor of phi, if factor generate a new prime and check
	e, _ := rand.Prime(rand.Reader, 16)
	for {
		gcd := big.NewInt(0).GCD(nil, nil, e, phi)
		if gcd.Int64() == 1 {
			break
		}
		e, _ = rand.Prime(rand.Reader, 32)
	}

	// calulcate d, (de = 1 % phi => d = 1/e % phi)
	d := big.NewInt(0).ModInverse(e, phi)

	// get message to encrypt from input
	textMessage := getMessage()

	// covert message from string to number representation
	message := big.NewInt(int64(textMessage[0]))
	for i := 1; i < len(textMessage); i++ {
		message.Mul(message, big.NewInt(1000))
		message.Add(message, big.NewInt(int64(textMessage[i])))
	}
	fmt.Print("MESSAGE: ", message, "\n\n\n")

	// encrypt with public key (e, n)
	// calculate c = m^e % n
	encryptedMessage := big.NewInt(0).Exp(message, e, n)
	fmt.Print("ENCRYPTED MESSAGE: ", encryptedMessage, "\n\n\n")

	// decrypt with private key (d, n)
	// calculate m = c^d % n
	decryptedMessage := big.NewInt(0).Exp(encryptedMessage, d, n)
	fmt.Print("DECRYPTED MESSAGE: ", decryptedMessage, "\n\n\n")

	// convert message from number to string representation
	var decryptedTextMessage string
	for {
		char := big.NewInt(0)
		char.Mod(decryptedMessage, big.NewInt(1000))
		decryptedTextMessage = string(int(char.Int64())) + decryptedTextMessage

		decryptedMessage.Div(decryptedMessage, big.NewInt(1000))
		if decryptedMessage.Int64() == 0 {
			break
		}
	}
	fmt.Println("OUTPUT MESSAGE: ", decryptedTextMessage)
}
