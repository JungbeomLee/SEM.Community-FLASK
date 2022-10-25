from flask import (request, redirect, make_response, url_for, flash)
from functools import wraps
from .env_var import jwt_secret_key, jwt_access_token_expires, jwt_refresh_token_expires
import jwt
import datetime

class CHECK_TOKEN() :
    def check_for_token(func):
        @wraps(func)
        def wrapped(*args, **kwargs):

            access_token = request.cookies.get('access_token')
            refresh_token = request.cookies.get('refresh_token')

            # 쿠키에 토큰이 둘 다 없을 경우
            if(not(access_token or refresh_token)) : 
                flash('You have to login first!')
                return redirect(url_for('flask_login.login'))
            try : 
                # access token이 만료되지 않은경우
                decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']
                try : 
                    # refresh token이 만료되지 않은 경우
                    decode_refresh_token_user_email = jwt.decode(refresh_token, jwt_secret_key, algorithms='HS256')['user_email']
                except : 
                    # refresh token이 만료된 경우
                    # refresh 토큰 생성
                    refresh_token = jwt.encode({
                    'user_email' : decode_access_token_emil,
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_refresh_token_expires)
                    }, jwt_secret_key, algorithm='HS256')

                    reps = make_response(func(*args, **kwargs))
                    reps.set_cookie('refresh_token', refresh_token)
                    return reps 
            except : 
                #access token이 만료된 경우
                try :  
                    # refresh token이 만료되지 않은 경우
                    decode_refresh_token_user_email = jwt.decode(refresh_token, jwt_secret_key, algorithms='HS256')['user_email']

                    # access token 생성
                    access_token = jwt.encode({
                    'user_email' : decode_refresh_token_user_email,
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_access_token_expires)
                    }, jwt_secret_key, algorithm='HS256')

                    reps = make_response(func(*args, **kwargs))
                    reps.set_cookie('access_token', access_token)
                    return reps
                except : 
                    # refresh token이 만료된 경우
                    flash('Your login has expired!')
                    return redirect(url_for('flask_login.login'))

            return func(*args, **kwargs)

        return wrapped