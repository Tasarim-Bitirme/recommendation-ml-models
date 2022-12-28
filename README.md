
# The model interface API is runned on docker.
## To run the model all you need to do is:
### 1. Clone the source code
### 2. Navigate the interface forder 
### 3. Run the docker by the following:
#### 3-a. Build the docker image by this command:
`docker build -t image-name .`
#### 3-b. Create a container for the image and run it:
`docker run -d -p 80:80 --name container-name image-name`
