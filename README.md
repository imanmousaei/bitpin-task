# Django Backend for bitpin task

## How it handles sudden rate changes
It multiplies older rates to LAMBDA(>1) which ensures older rates have more weight than new ones.

## Run on Local

- `make install`
- `make migrate`
- `make admin`
- (optional) run `make test` to run testcases
- `make server`
- go to `http://127.0.0.1:8000/admin/` and use it


## Backup Database
```bash
su - postgres
pg_dump -U postgres bitpindb > dbexport_1403_10_14.pgsql
```
in this way dbexports are saved at : `/var/lib/postgresql`

## Depoly using docker
`docker-compose up --build`

## Deploy using Nginx & Gunicorn
[Django Deployment Document on Ubuntu with Nginx & Gunicorn](./Deploy.md)

## CI 
The file `.gitlab-ci.yml` is configured to run django tests on gitlab when a commit is pushed to `main` branch
