# Golembane
Golang API for FEH-VG-Bots based on [this tutorial ](https://dev.to/aurelievache/learning-go-by-examples-part-2-create-an-http-rest-api-server-in-go-1cdm)

## Requirements
* Install [Taskfile](https://taskfile.dev/installation/)
* Install [Go-Swagger](https://github.com/go-swagger/go-swagger/blob/master/docs/install.md)

## Commands
* `go run internal/main.go` -> Starts API 
* `go build -o bin/go-rest-api internal/main.go` -> Generates an executable binary with our HTTP server
* `swagger version`
* `task swagger.validate`
* `task swagger.doc`
* `task swagger.gen`