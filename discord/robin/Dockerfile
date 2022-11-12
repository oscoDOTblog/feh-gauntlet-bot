# Select Docker image
FROM golang:1.19.3-alpine3.16
 
# Create app directory
WORKDIR /app

# Copy Source Code into /app
ADD . /app/
 
# Install app dependencies
RUN go build -o main . 
 
# Run Bot
CMD ["./main"]
