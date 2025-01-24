# Photon Museum - Film Archive and Management System
A Django-based content management system for archiving and managing films.

## Features
- Add, view, and manage film types you used.
- Add, view, and manage authors of the films.
- Upload and display images for films (auto-detect the last two digits of the file name of the films and link to their index in the roll)
- Dashboard for tracking user's film shooting activity monthly and yearly.
- List top 3 used film types for this year and last year.
- More features to be developed and added...

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Ensure you have the following installed:

1. **Docker** and **Docker Compose**  
   - [Install Docker](https://docs.docker.com/get-docker/)  
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Git** (optional, if you are cloning the repository)  
   - [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

---

### Setup Instructions

1. **Clone the Repository**  
   Open a terminal and run the following command:
   ```bash
   git clone https://github.com/wangsheng-wu/photon-museum-public.git
   cd photon-museum-public
2. **Environment Variables**
   Create a .env file in the root of the project to configure the environment variables.
   Use this template for the file:
   ```bash
   SECRET_KEY=your-django-secret-key
   ALLOWED_HOSTS=127.0.0.1,localhost
   DATABASE_URL=postgres://film_user:photonmuseum@db:5432/film_archive_db
   ```
   Replace your-django-secret-key with a valid secret key. You can generate one by running:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
3. **Start the Docker Containers**
   Run the following command to build and start the containers:
   ```bash
   docker-compose up --build
   ```
4. **Run Database Migration**
   Once the containers are running, apply the database migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
5. **Create a Superuser**
   To access the Django's default admin panel, create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
7. **Access the Application/System**
   - The application/system will be accessible at: http://localhost:8000/archive/home
   - To access the Django's default admin panel, go to: http://localhost:8000/admin
8. **Stop the Application/System**
   To stop the running containers, use:
   ```bash
   docker-compose down
   ```
## Note:
If you are running the system without Docker, make sure you install all the items/dependencies in the ``requirements.txt`` file.

## Contact
If you encounter any issues or have questions, feel free to contact me.
- My email: ww2674 (at) columbia (dot) edu
- You may also reach out to me on [Instagram](https://www.instagram.com/wu.wangsheng/)
