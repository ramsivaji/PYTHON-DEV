# Railway Deployment Guide for Python DEV (Django)

Your Django application is now fully configured for production deployment on Railway. All necessary files (`Procfile`, `runtime.txt`, `requirements.txt`) have been created, and the `settings.py` file has been properly configured for PostgreSQL, WhiteNoise (static files), and environment variables.

## Step-by-Step Deployment Setup

### 1. Push your code to GitHub
If you haven't already, push your updated code to your GitHub repository:
```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

### 2. Create a Railway Account & Connect GitHub
1. Go to [Railway.app](https://railway.app/) and sign in.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository (`ramsivaji/PYTHON-DEV`).
4. Railway will analyze your repository and detect the `Procfile` and `requirements.txt`. It will automatically start creating the web service, but it will likely fail on the first run because we haven't configured the database and environment variables yet. That is normal.

### 3. Add PostgreSQL Service
1. In your Railway project, click **New** (or right-click an empty area) -> **Database** -> **Add PostgreSQL**.
2. Wait a few seconds for the database to provision.

### 4. Link the Database and Set Environment Variables
1. Click on your previously created GitHub repository service (the web app) in Railway.
2. Navigate to the **Variables** tab.
3. Click **New Variable** and add the following:
   
   - **DATABASE_URL**: (Railway automatically provides this when you link the Postgres service, or you can copy it from the PostgreSQL service's Variables tab and add it here. Actually, it is best to click **Variable Reference** and select the Postgres service's `DATABASE_URL`).
   - **SECRET_KEY**: `your-very-secret-long-random-string` (Create a new secure random string).
   - **DEBUG**: `False` (This is crucial for production).
   - **ALLOWED_HOSTS**: `*` (Or you can use your specific Railway `up.railway.app` URL).
   - **CSRF_TRUSTED_ORIGINS**: `https://your-app-name.up.railway.app` (Replace with the exact public domain Railway gives you for your app).

### 5. Generate a Public URL
1. Click on your web app service.
2. Navigate to the **Settings** tab.
3. Under **Networking**, click **Generate Domain** (or set up a custom domain). This will give you a public URL like `https://something.up.railway.app`.

### 6. Run Migrations & Collect Static Files
Railway will automatically detect your `release` command in the Procfile and run migrations for you:
`python manage.py migrate`

Static files are automatically handled via WhiteNoise, which hook into `python manage.py collectstatic` during the build phase. You do not need to run `collectstatic` manually on Railway.

### 7. Create Superuser (Admin)
Since your app uses a production database, you need to create a new admin user on the Railway database.
1. In Railway, click on your web app service, go to the **Command** palette or **Deployments** tab, and click the **Terminal** icon (shell access).
2. Run the following command:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow the prompts to set up your username, email, and password.

---

## Common Deployment Fixes

- **Static Files Not Loading (404 Not Found)**: 
  This issue is solved! We have already configured `WhiteNoise` in `settings.py`. Ensure that `STATIC_ROOT` is pointing to the correct directory (`staticfiles`) as we configured.
- **CSRF Verification Failed**: 
  If you get a 403 CSRF error on form submissions or admin login, ensure `CSRF_TRUSTED_ORIGINS` contains your HTTPS Railway domain. (e.g., `https://python-dev-production.up.railway.app`).
- **Database Connection Error**: 
  Make sure your Web service has the `DATABASE_URL` variable properly injected. In `settings.py`, `dj_database_url` takes care of parsing the URL and overriding SQLite automatically. If `DATABASE_URL` is omitted, the app will safely fall back to the local `db.sqlite3`.
- **Application Error (H10 / 500)**:
  Check the Railway deployment logs. Ensure that `DEBUG=False` is set and that your `ALLOWED_HOSTS` accepts requests (e.g. `*` or the generated domain).

Your project is now 100% production-ready!
