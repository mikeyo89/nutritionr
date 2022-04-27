# Nutritionr

Public Web Application Demo for showcasing uses of Edamam's Nutrition-based APIs.

## Steps to Reproduce

1. Clone this repo using git or github desktop.
2. In a local or virtual environment, ensure to install pip or pip3.
   > This can be done by checking out the documentation on <a href="https://pip.pypa.io/en/stable/installing/">pip</a>.
3. Navigate to the project directory -- 2 folders (scripts and nutritionr) and various other files will be located here.
4. Open a command shell -- such as bash, windows shell, or zsh -- and run the following command:
    >`pip3 install -r requirements.txt`
5. Navigate into the web_app directory (`cd nutritionr/`).
6. In a command shell, run the following command:
    >`python manage.py runserver`
7. There should be a warning about running migrations. Run them by doing:
   >a. Hit `Ctr + C` (to close the server).\
   >b. Run the command `python manage.py migrate` in the terminal to run migrations.
8. Finally, you must setup the cache table by running the following command:
   >`python manage.py createcachetable`

### Congratulations, all dependencies are now installed!
<br><br>

**From here, simply run the web-app by doing the following:**

1. In a command shell, run the following command:
    >`python manage.py runserver`
2. Navigate to <a href="127.0.0.1:35729">127.0.0.1:35729</a> on your preferred browser.
3. You're free to use the application as you wish!

**That is all, folks!**
