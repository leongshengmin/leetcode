BINARY_NAME=onearc

## tidy: tidy modfiles and format .go files
.PHONY: tidy
tidy:
	go mod tidy
	go fmt

## build: build the application
.PHONY: build
build:
	go build -o bin/${BINARY_NAME} . && chmod +x bin/${BINARY_NAME}

## run: run the  application
.PHONY: run
run: build
	bin/${BINARY_NAME}
