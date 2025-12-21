# Streamlit Deployment Guide - Supabase Email Configuration

## 🚨 Issue: Confirmation Emails Not Working After Deployment

When deploying to Streamlit Cloud, Supabase confirmation emails may stop working because the redirect URLs are configured for localhost.

## ✅ Complete Solution

### Step 1: Configure Supabase Dashboard Settings

1. **Go to Supabase Dashboard:**
   - Visit: https://app.supabase.com/project/hqdrdatcbwhunswiiuuw/auth/url-configuration

2. **Update Site URL:**
   - Navigate to: **Authentication** → **URL Configuration**
   - Set **Site URL** to your Streamlit app URL:
     ```
     https://your-app-name.streamlit.app
     ```
   - Replace `your-app-name` with your actual Streamlit app name

3. **Add Redirect URLs:**
   - In **Redirect URLs** section, add:
     ```
     https://your-app-name.streamlit.app/**
     http://localhost:8501/**
     ```
   - The `**` wildcard allows any path on your domain
   - Keep localhost for local development

4. **Save Changes**

### Step 2: Verify Email Templates

1. **Check Email Templates:**
   - Go to: **Authentication** → **Email Templates**
   - Click on **Confirm signup** template
   
2. **Verify Template Uses Dynamic URL:**
   - Ensure the confirmation link uses: `{{ .SiteURL }}`
   - Default template should look like:
     ```html
     <a href="{{ .ConfirmationURL }}">Confirm your email</a>
     ```
   - This automatically uses the correct site URL

3. **Check Other Templates:**
   - Verify **Reset Password** and **Magic Link** templates also use `{{ .SiteURL }}`

### Step 3: Configure Streamlit Secrets

1. **After deploying to Streamlit Cloud:**
   - Go to your app settings on Streamlit Cloud
   - Navigate to **Secrets**

2. **Add the following secrets:**
   ```toml
   SUPABASE_URL = "https://hqdrdatcbwhunswiiuuw.supabase.co"
   SUPABASE_ANON_KEY = "sb_publishable_kZLyTV9kEBwk3jZJtzqryA_agEnY11Y"
   GOOGLE_API_KEY = "AIzaSyAwnU5k8AWnyZI_IgFHkPzzjhXygHdiQb0"
   STREAMLIT_APP_URL = "https://your-app-name.streamlit.app"
   ```

3. **Replace `your-app-name` with your actual Streamlit app name**

### Step 4: Update .env File for Local Development

After deployment, update your local `.env` file:

```env
STREAMLIT_APP_URL=https://your-app-name.streamlit.app
```

This ensures local development also works with the deployed URL.

### Step 5: Disable Email Confirmation (Optional)

If you want users to login immediately without email confirmation:

1. **Go to Supabase Dashboard:**
   - Navigate to: **Authentication** → **Settings**

2. **Disable Email Confirmation:**
   - Find **Enable email confirmations**
   - Toggle it OFF

3. **Save Changes**

⚠️ **Note:** This is less secure but allows immediate access.

## 🔍 Troubleshooting

### Problem: Still Not Receiving Emails

**Check Supabase Email Provider:**
1. Go to: **Authentication** → **Settings** → **SMTP Settings**
2. Verify email provider is configured:
   - **Default (Supabase):** Limited to 3 emails/hour
   - **Custom SMTP:** Unlimited, recommended for production

**Test Email Delivery:**
1. Check your spam/junk folder
2. Verify email address is correct
3. Try with different email provider (Gmail, Outlook, etc.)

### Problem: Redirect After Email Confirmation Fails

**Check Redirect URLs:**
1. Ensure wildcard `/**` is added to redirect URL
2. Verify Site URL matches exactly (no trailing slash)
3. Check for typos in domain name

### Problem: CORS Errors

**Update Supabase CORS Settings:**
1. Go to: **Settings** → **API**
2. Add your Streamlit app URL to allowed origins:
   ```
   https://your-app-name.streamlit.app
   ```

## 📝 Deployment Checklist

- [ ] Update Supabase Site URL
- [ ] Add redirect URLs (deployed + localhost)
- [ ] Verify email templates use `{{ .SiteURL }}`
- [ ] Add secrets to Streamlit Cloud
- [ ] Update local `.env` with deployed URL
- [ ] Test signup on deployed app
- [ ] Verify confirmation email received
- [ ] Test email confirmation link works
- [ ] Verify redirect after confirmation

## 🎯 Quick Verification Test

After deployment:

1. **Create a new account** on your deployed app
2. **Check email** - you should receive confirmation within 1-2 minutes
3. **Click confirmation link** - should redirect to your app
4. **Login** - should work immediately

## 📚 Additional Resources

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Supabase Email Configuration](https://supabase.com/docs/guides/auth/auth-email)

## 🆘 Still Having Issues?

1. Check Supabase logs: **Authentication** → **Logs**
2. Check Streamlit logs in your app dashboard
3. Verify all environment variables are set correctly
4. Try disabling email confirmation temporarily to isolate the issue
