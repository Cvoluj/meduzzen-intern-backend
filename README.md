# Instalation
Clone project to your local machine using Git. You can use the following command to clone the repository:
```
git clone --branch BE-2-init_application https://github.com/Cvoluj/meduzzen-intern-backend.git
```
Create your image
```
docker build . -t fastapi_app_test:latest -f Dockerfile.test
```
Run container
```
docker run -p 8000:8000 <image_name>
```
Use localhost:8000 to visit site

Create test image
```
docker build . -t fastapi_app_test:latest -f Dockerfile.test
```
Run container
```
docker run --rm fastapi_app_test
```