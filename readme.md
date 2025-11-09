fastapi dev main.py

uvicorn app.main:app --reload

### use alembic for SQLAlchemy

```alembic revision -m 'create user table```
then update the ```upgrade()``` & ```downgrade()``` functions

```
def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
```
### Last version
```alembic head```

### For checking the history
```alembic history```

### Upgrade the changes
```alembic upgrade revision_id```


### Automatically generate from models
```alembic revision --autogenerate -m 'auto votes'```


-----------------------
### Heroku setups
------------------------

#### Ubuntu
```curl https://cli-assets.heroku.com/install-ubuntu.sh | sh```

#### Login
```heroku login```

#### Create heroku app
```heroku create unique_app_name```

#### Deploy to heroku
```
git remote
    heroku
    origin

git push heroku main
```

#### Tell Heroku the main.py file
```
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT: -5000}
```


### Deploy on UBuntu server
Install the server then update packages
```sudo apt update && sudo apt upgrade -y```

#### Install packages for project
```sudo apt install python3-pip```
```
sudo pip3 install virtualenv
sudo apt install python3-virtualenv

sudo apt install postgresql postgresql-contrib -y

# Check postgres user is created or not 
sudo cat /etc/passwd

sudo su
# enter the password

su - postgres
psql -U postgres

# change the password
\password postgres

cd /etc/postgresql/17/main

sudo nano postgresql.conf
# change the `Connection and Authentication` Sections listen_addresses = '*'
# put here the only ip addresses that can connect to the database listen_addresses = '192.168.*.*'

# Then open pg_hba.conf
# change the locals methods to md5 and ip4 address to 0.0.0.0/0
```

We have to create another user for handling our project
#### Create user
```
sudo adduser <username>

# give user the admin privilidge
usermod -aG sudo <username>
```