# What is Django file Drive ?
It is an API allowing you to manage your own file drive in the cloud. You can see it as a Google Drive API clone.
Here is a list of the main features of the API:
- Mangage users
- Manage files & folders
- Manage who you share your file and folders with
- Search among your files and folders

![App Screenshot](https://i.ibb.co/yySBLmm/apidoc.png)  

🔗 Check the [full documentation of the API on Postman.](https://documenter.getpostman.com/view/11214441/UVyvvE6f) for more information on all the endpoints.

🚀 If you want a [live demo](#) of the API, you can check the [front-end repo](https://github.com/Virgin75/file-drive-front) that I created with React.
This API was built with Python and Django Rest Framework.

# How to deploy the project locally?
The easiest way to test the API locally is to run it on your computer with Docker compose.

1. Clone this repo locally
2. `cd` to the directory of the downloaded repo on your device
3. Optionnaly: You can edit `.env` file in the root directory, with the db password of your choice as well as django secret key.
4. Use `docker-compose` command to start the server with all the associated services (django app, db, nginx, celery & redis) : `sudo docker-compose up --build`
5. Try to access this URL[http://127.0.0.1/admin/login/](http://127.0.0.1/admin/login/). If you see the Django admin login : the server is up and running 🎉
6. Create the django superuser in the db to access the admin view:
  - Access the shell of the django container with : `sudo docker exec -it <insert_here_django_container_name> sh`
  - Then `# python manage.py createsupersuer` will prompt you to input your email & password.
