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


### Setup the environment variable to the server
```
# check env variables
:~printenv
:~export <MY_NAME>=MY_VALUE
cd ~
touch .env
```
Create .env file and copy project all env to server ~/.env file assign the desired and then 
run the below command:
```set -o allexport; source ~/.env; set +o allexport```

If we restart our machine it will remove those env variable so that, we have to put ```set -o allexport; source ~/.env; set +o allexport``` this command to ~/.profile file

#### study
In .profile file ```set -o allexport; source ~/.env; set +o allexport``` some time not running
due to ```.env``` permission. Set its permission to 600 for the user,


#### Connect app from outside. But it need to manually run 
```uvicorn --host 0.0.0.0 app.main:app``` 

##### Host can be unreachable due to port binding or firewall allow
```
uvicorn --host 0.0.0.0 --port 8000 app.main:app
sudo ufw allow 8000/tcp
sudo ufw reload
# checking
sudo ufw status
``` 


##### Need to install
```
pip install gunicorn
pip install httptools
pip install uvtools


gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

# Check all the connection
ps -aef | grep -u gunicorn
```

### Need to run in background and reboot while server reboot

#### services that are run in the system
```cd /etc/systemd/system```

Define service in project directory
#### Creating service
```
sudo nano simple-fastapi.service
```
Now copy the ```gunicorn.service``` file text to ```/etc/systemd/systemsimple-fastapi.service```
```and run sudo start system simple-fastapi.service```

```
sudo systemctl restart simple-fastapi.service
sudo systemctl daemon-reload
sudo systemctl status simple-fastapi.service

# Enable or Disable
sudo systemctl enable simple-fastapi.service
sudo systemctl disable simple-fastapi.service
```


Why nginx is optimized

SSL termination


## Nginx setup
```
sudo apt install nginx -y