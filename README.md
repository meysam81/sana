# sana
This app was a question asked at an interview technical test, required to provide a login page for a user, that should be banned after 3 times requesting the login page or entering the wrong password. The ban must be held for 1 hour, and the resulting is the following app.


## Preliminaries
To start the application, first you should install some stuff.
For debian-based linux systems:
```
sudo apt-get install virtualenv virtualenvwrapper
```
Then you need to do some setups in order to be able to run the app.
Some lines must be added to `~/.bashrc`, so :
```
mkdir -p ~/Codes/Python/dev ~/Codes/Python/envs
cat << EOF >> ~/.bashrc
export WORK_HOME=$HOME/Codes/Python/envs
export PROJECT_HOME=$HOME/Codes/Python/dev
. /usr/local/bin/virtualenvwrapper.sh
EOF
```

### Sourcing your bashrc
After adding the lines from previous step, you should re-run your bashrc so that the changes are applied:
```
. ~/.bashrc
````

## Setup the Project
You most probably have the stable python 2.7 version, so no worries there.
After doing the previous steps, the next 2 steps are easy as a peach.
```
cd ~/Codes/Python/dev/
git clone git@github.com:meysam81/sana.git
mkproject sana
```

## Run the Project
Now to run the project, simply run the following command:
```
python manage.py runserver
```

And now you should be able to see the webpage from the following address:
`localhost:5000`

## Stop the project
If you want to stop the app, simply press the following keys on your keyboard:
`Ctrl + C`

And after that, using the following command you can exit the environment:
`deactivate`

And if you ever wanted to comeback to the project, run the following command:
`workon sana`

Thanks for reading, feel free to pull, fork or star.
