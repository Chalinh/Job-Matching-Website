# Render Deployment Setup Guide

## CRITICAL: You MUST set DATABASE_URL before the app will work!

### Step 1: Set DATABASE_URL Environment Variable

**This is the MOST IMPORTANT step!**

1. Go to your **Render Dashboard**: https://dashboard.render.com
2. Click on your **PostgreSQL database** (should be named something like `job-matching-db`)
3. Copy the **"Internal Database URL"** - it looks like:
   ```
   postgresql://username:password@dpg-xxxxx.oregon-postgres.render.com/dbname
   ```

4. Go to your **Web Service** (`job-matching-website`)
5. Click **"Environment"** in the left sidebar
6. Click **"Add Environment Variable"**
7. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the database URL you copied
8. Click **"Save Changes"**

**The service will automatically redeploy!**

---

### Step 2: Verify the Build Logs

After the service redeploys, check the **Logs** tab. You should see:

```
==> Checking DATABASE_URL...
DATABASE_URL is set
==> Testing database connection...
System check identified no issues (0 silenced).
==> Running database migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, jobs, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying jobs.0001_initial... OK
  Applying sessions.0001_initial... OK
==> Checking if jobs table was created...
Jobs table exists: True
==> Loading job data...
Loading jobs from: data/normalized_data/camhr_normalized_20251227_014140.json
Loaded 100 jobs...
Loaded 200 jobs...
...
Successfully loaded 1777 jobs
Total jobs in database: 1777
==> Build completed successfully!
```

---

### Step 3: Test the Website

Visit: https://job-matching-website.onrender.com

You should see the search form with no errors!

---

## Troubleshooting

### Error: "DATABASE_URL is not set"
- You forgot to add the `DATABASE_URL` environment variable
- Go back to Step 1 and add it

### Error: "relation 'jobs' does not exist"
- The migrations didn't run
- Check if `DATABASE_URL` is set correctly
- Try manually redeploying: Dashboard → Manual Deploy → Deploy latest commit

### Error: "Connection refused"
- The `DATABASE_URL` is wrong or pointing to localhost
- Make sure you copied the **Internal Database URL** from your Render PostgreSQL database
- The URL should start with `postgresql://` and contain `.render.com`

---

## Manual Fix (If Build Fails)

If the automatic build doesn't work, you can manually run migrations using Render Shell:

1. Go to your **Web Service**
2. Click **"Shell"** tab
3. Run these commands:
   ```bash
   python manage.py migrate
   python manage.py load_jobs
   ```

---

## Current Status Checklist

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL environment variable added to web service
- [ ] Service redeployed successfully
- [ ] Build logs show "Jobs table exists: True"
- [ ] Build logs show "Successfully loaded XXXX jobs"
- [ ] Website loads without errors

---

**If you're still stuck, share the BUILD LOGS from Render!**
