# Project installation steps

1. Pull the repository: `git clone <repo_url>`
2. Navigate into the project's root level directory (on the same level with Dockerfile, docker-compose.yml etc.)
3. Copy the following files: `db.env`, `.env`. Paste the contents from respective `.example` files.
4. Build the project's Docker image: `docker compose build --no-cache`
5. Run the containers: `docker compose up`
6. List the containers and locate the ID for `api` container: `docker ps`.
7. Copy `api` container ID and get in its interactive terminal: `docker exec -it <api_container_id> sh`
8. Run the migrations: `python manage.py migrate`
9. Create your superuser: `python manage.py createsuperuser`
10. Install fixtures for Notes (initial 5 records to bootstrap the project): `python manage.py loaddata notes/fixtures/notes.json`
11. Open Swagger doc page in your browser: `localhost:8000/api/docs`
12. Locate `/login` and authenticate with the creds of your superuser you've created in step 8; copy `access` token from the response.
13. Locate `Authorize` bar in the upper section of the Swagger docs page, and provide the access token in the format: `Bearer {token}`.
14. Test any other endpoints you wish!
15. <OPTIONAL> if you want to run tests, open interactive shell for `api` container (covered in steps 6-7), and run `pytest`.
