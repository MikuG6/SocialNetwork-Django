# SocialNetwork-Django

## About

This is a pet-project implemented on the Django framework, but on the PEST architecture.
It implements: Logging, Auditing, Testing using PyTest.

Web server - nginx

DataBase - PostgreSQL

Containerizer - Docker


## How to install on a local repository
1) First you need to clone repositories

```bash
git clone git@github.com:MikuG6/SocialNetwork-Django.git
```

2) Using Docker-compose, we build and up containers using the following commands

```bash
docker-compose -f docker-compose.yaml up -d --build
```

## Port

1) Ngnix - 80
2) PostqreSQL - 5432
3) Django - 8000

## Testing

```bash
pytest test/
```

## Deployment Scheme
![Project](https://github.com/MikuG6/SocialNetwork-Django/assets/83876860/5d2029b2-f3d3-43f4-9f82-bfe167765a77)
