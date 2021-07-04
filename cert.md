openssl genrsa -out RootCA.key 4096 
openssl req -new -x509 -days 1826 -key RootCA.key -out RootCA.crt -config config.cnf
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config config.cnf
openssl x509 -req -days 1000 -in server.csr -CA RootCA.crt -CAkey RootCA.key -set_serial 0101 -out server.crt -sha256 -extfile config.cnf
openssl x509 -in server.crt -text -noout 
openssl req -in server.csr -text -noout
