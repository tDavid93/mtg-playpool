#Project README
##Overview
This project is a highly Docker-dependent application that consists of a frontend and a backend. It utilizes Docker Compose to orchestrate the deployment of the different services.
Prerequisites
Before running the application, make sure you have the following installed on your machine:
- Docker
- Docker Compose
Getting Started
To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project root directory.
Backend Setup
1. Open a terminal and navigate to the backend directory.
2. Build the backend Docker image by running the following command:
3. Once the image is built, start the backend service by running the following command:
Frontend Setup
1. Open a terminal and navigate to the frontend directory.
2. Build the frontend Docker image by running the following command:
3. Once the image is built, start the frontend service by running the following command:
Nginx Setup
1. Open a terminal and navigate to the nginx directory.
2. Build the Nginx Docker image by running the following command:
3. Once the image is built, start the Nginx service by running the following command:
Usage
Once all the services are up and running, you can access the application by opening your browser and navigating to http://localhost:8050.
Additional Information
For more detailed information about the project and its components, please refer to the following documentation:

- Create React App Documentation
- React Documentation
- Docker Documentation
- Docker Compose Documentation
Troubleshooting
If you encounter any issues while setting up or running the application, please refer to the troubleshooting section in the respective documentation links provided above.
Contributing
If you would like to contribute to this project, please follow the guidelines outlined in the CONTRIBUTING.md file.
License
This project is licensed under the MIT License.# MTG-Playpool

usage:

docker-compose up -d

