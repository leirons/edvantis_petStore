# PetStore App

## About Project


### Structure
```
    /docker
        /api -- Storage with all different version of api
            DockerFile -- DockerFile with current version of api
    /src
        /app
        - schemes.py -- Message Scheme for error log
        - server.py -- Init of FastAPI
            /routers
            - pet.py - -- All routers of pet service
            - store.py -- ALl routers of store service
            - users.py -- All routers of users service
            /services
                /pet
                - logic.py -- database logic
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
                /store
                - logic.py -- database logic
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
                /user
                - logic.py -- database logic
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
        /core
            /cache
            - backend.py -- Main backend for caching, use ujson insted of json(much faster)
            - cache.py -- Cache logic(Manager)
            - key_marker.py -- Custom Key Maker for making prefix for caching
            - redis.py -- Import of redis(Aioredis -- asyncio)
            /db
            - session.py -- Init of database
            /excpetions
            - base.py -- Base excpetions for all services
            - pet.py -- Exceptions of pet service
            - server.py -- Exceptions of Server
            - store.py -- Exceptions of store service
            - user.py -- Exceptions of user service
            /middlewares
            - authentication.py -- Authentication middleware for user,
            it takes request and check if user loged if True it returs pydantic scheme of user
            /repository
            - base.py -- Base CRUD for all services
            - auth.py -- AuthHandler for auth user
            - config.py -- Init of config: db_url,test_db,dsn, etc..
            - schemes.py -- Scheme of current user(needs for middlewares)
        /migrations
            /versions
            - alembic_helper.py -- Import all models of database
            - env.py -- Settings of alembic
        /resources
        -  strings.py -- Messages for error
    /tests
        - conftest.py -- Init env for tests
        /performance
        - test_performance.py -- Test of user performance
        /pet
        - test_pet.py -- Tests of pet service
        /store
        - test_store.py --  Tests of store service
        /user
        - test_email.py --  Tests of email
        - test_phone.py --  Tests of phone
        - test_user.py --  Tests of user service
    pre-commig.config.yaml --
    docker-compose.yml -

```

## How to run

### Docker
```
docker-compose up --build
docker container ls
docker exec (name of web service) alembic upgrade head
```


### Another way -

* Create .env file in root directory
```
DATABASE_URL=your
TEST_DB=your
SECRET=Your
REDIS_HOST=your
```

### Windows
```
1 - virtualenv myenv
2 - myenv\Scripts\activate
3 - cd src
4 - pip3 install pipenv
5 -  pipenv install
6 - uvicorn app.server:app
```


### Linux
```
1 - python3 -m venv venv
2 - source venv/bin/activate
3 - cd src
4 - pip3 install pipenv
5 -  pipenv install
6 - uvicorn app.server:app
```
