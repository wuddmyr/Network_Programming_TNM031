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
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	return strings.Replace(text, "\n", "", -1)
}

func main() {

	p, _ := rand.Prime(rand.Reader, 1024)
	q, _ := rand.Prime(rand.Reader, 1024)

	n := big.NewInt(0).Mul(p, q)

	textMessage := getMessage()
	fmt.Println("input message:", textMessage)

	message := big.NewInt(int64(textMessage[0]))
	for i := 1; i < len(textMessage); i++ {
		message.Mul(message, big.NewInt(1000))
		message.Add(message, big.NewInt(int64(textMessage[i])))
	}
	fmt.Println("message:", message)

	// phi
	phi := big.NewInt(0).Sub(big.NewInt(0).Set(p), big.NewInt(1))
	phi.Mul(phi, big.NewInt(0).Sub(big.NewInt(0).Set(q), big.NewInt(1)))

	// check if e is factor of phi
	e, _ := rand.Prime(rand.Reader, 32)
	for {
		gcd := big.NewInt(0).GCD(nil, nil, e, phi)
		if gcd.Int64() == 1 {
			break
		}
		fmt.Print("e is factor of phi")
		e, _ = rand.Prime(rand.Reader, 32)
	}

	// gcd := big.NewInt(0).GCD(nil, nil, e, phi)
	d := big.NewInt(0).ModInverse(e, phi)

	// encrypt
	encryptedMessage := big.NewInt(0).Exp(message, e, n)
	fmt.Println("encryptedMessage:", encryptedMessage)

	// decrypt
	decryptedMessage := big.NewInt(0).Exp(encryptedMessage, d, n)
	fmt.Println("decryptedMessage:", decryptedMessage)

	// decryptMessage to string format
	var decryptedTextMessage string
	for {
		x := big.NewInt(0)
		x.Mod(decryptedMessage, big.NewInt(1000))
		decryptedMessage.Div(decryptedMessage, big.NewInt(1000))

		decryptedTextMessage = string(int(x.Int64())) + decryptedTextMessage

		if decryptedMessage.Int64() == 0 {
			break
		}
	}
	fmt.Println("Descrypted message is:", decryptedTextMessage)
}
