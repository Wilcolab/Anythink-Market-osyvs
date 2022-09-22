# Welcome to the Anythink Market repo

To start the app use Docker. It will start both frontend and backend, including all the relevant dependencies, and the db.

Please find more info about each part in the relevant Readme file ([frontend](frontend/readme.md) and [backend](backend/README.md)).

## Development

When implementing a new feature or fixing a bug, please create a new pull request against `main` from a feature/bug branch and add `@vanessa-cooper` as reviewer.

## First setup

Verify that docker is ready by running the following commands in your terminal:
docker -v and docker-compose -v
Both commands will return version information if docker is installed. Navigate your terminal to the project root directory and run the following command:
docker-compose up
Allow docker to prepare both the backend and frontend. If Docker is working correctly, the backend should be running and able to connect to your local database.
You can test this by opening http://localhost:300/api/ping in your browser.
You can check the frontend and ensure it's connected to the backend by creating a new user on http://localhost:3001/register