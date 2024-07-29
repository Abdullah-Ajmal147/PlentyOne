# Plentyone
This should help you get started and understand what how this project is structured.
The Config is our main Project, Anything inside are normal django apps,settings and required folders and files.

### Settings Configuration
- Most of the apps in this project are not included in the settings by default. You will need to make necessary changes in the `settings.py` file before adding them.

### Custom User Model
- The custom user model is designed to modify the default user by adding a phone number field. 
- You may need to remove the `@login_required` decorator from account settings views if you encounter any access errors.

### Templates
- Most errors you might encounter are likely to be found in the templates. Ensure to thoroughly check and debug template files.

### Admin Registration
- Some models have not been registered in the admin interface. Verify and register any missing models in the `admin.py` files of respective apps.

### Static Files
- Static files have been collected in the `staticfiles` directory. Ensure this directory is properly configured in your settings.

### Additional Requirements
- Virtual environment.
- Install all required dependencies using `pip install -r requirements.txt`.
- Ensure the database is set up correctly and run `python manage.py migrate` to apply migrations.


### Additional Resources
- For the latest updates and changes, refer to [GitHub](https://github.com/sudoevans/plentyone).
- If you need further assistance to understand what I did, you can check [sudoevans' GitHub profile](https://github.com/sudoevans).

## Deployment to Railway.app

### Step-by-Step Guide


**Connect to GitHub**: Link your GitHub account and select the repository for this project.

**Django Settings**:
    - Ensure `ALLOWED_HOSTS` includes `railway.app` or set it to `['*']` for testing purposes.
    - Update the `DATABASES` setting in `settings.py` to use the `DATABASE_URL` provided by Railway.
**Static Files**: Configure static files for deployment.
    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'
    ```

**Procfile**:  `Procfile`  Should have the following content:
    ```plaintext
    web: gunicorn Config.wsgi
    ```
**Runtime**:
```
python - 3.12.3 
```