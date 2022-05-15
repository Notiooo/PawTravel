@echo off
cls
set /p txt=Give me facebook secret key: 
echo SOCIAL_AUTH_FACEBOOK_SECRET=%txt% > "..\PawTravel\.env"
set /p txt=Give me google secret key:
echo SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=%txt% >> "..\PawTravel\.env"
exit