How to start Server:

1. go to root directory of project ( same as readme file location ).
2. run : docker build . -t demo-app
3. run : docker run -it -p 8000:8000 demo-app
4. try to open : http://127.0.0.1:8000/siteAdmin/
5. If it opens an django administration page then you can start testing using : http://127.0.0.1:8000/
NOTE :
 --- JWT token will be present in HTTP_AUTHORISATION header in response of successful login request.
 --- Please use Bearer token in postman to use jwt token for transactions.
Routes :

User -------------------------

 - /user/register (POST) : To create a new user account
    params ( x-www-form-urlencoded) : 
        - name    : Min 3 chars  
        - email   : A valid email
        - contact : Just 10 digit mobile no. +91 or 0 is not acceptable as prefix
        - password: Min 8 chars
        - gender  : (M,Male or 1) for male, (F,Female or 2) for female, ( Rest all values) for others


 - /user/updateAccountInfo (PUT) : To update name or password
    params ( x-www-form-urlencoded) : 
        - name       : Min 3 chars  
        - oldPassword: Min 8 chars
        - newPassword: Min 8 chars

 - /user/deleteAccount (DELETE) : To deactivate user's account

 - /user/login (POST) : To fetch a user auth token
        - username   : Email or Contact no.
        - password   : Min 8 chars

 - /user/logout (GET)     

Admin ---------------------------

 - /admin/createAdminAccount (POST) : To create a new admin account
    params ( x-www-form-urlencoded) : 
        - name    : Min 3 chars  
        - email   : A valid email
        - contact : Just 10 digit mobile no. +91 or 0 is not acceptable as prefix
        - password: Min 8 chars
        - gender  : (M,Male or 1) for male, (F,Female or 2) for female, ( Rest all values) for others

 - /admin/getUserActivities/<str:identifier> (GET) : To get a new specific user's activity
    - identifier : An existing email or contact no.

    Ex:  /admin/getUserActivities/prashant.vyala@gmail.com 
        /admin/getUserActivities/8266961869

 - /admin/getAllUsersActivities (GET) : To get all registered users activities

 - /admin/blockUser/<str:identifier> (GET) : To block a user using either email or contact no.

 - /admin/unblockUser/<str:identifier> (GET) : To unblock a blocked user using either email or contact no.
