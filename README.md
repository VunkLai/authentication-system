# Authentication System

A authentication system using JWT

## API

### Register

```
POST /auth/register
Content-Type: application/json

{"username": "username", "password": "password"}
```

### Login

```
POST /auth/login
Content-Type: application/json

{"username": "username", "password": "password"}
```

### JWT verify

```
# example
>>> user = User.objects.last()

>>> user.get_all_permissions()
{'cost_center.add_costcenter',
 'cost_center.change_costcenter',
 'cost_center.view_costcenter'}

>>> user.is_active
True
```

## TODO

- [ ] Generate API Document by Swagger
