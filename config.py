class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_HOST = '127.0.0.1'
    MYSQL_DATABASE_DB = 'FlaskProject'  # can be any

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    
    MYSQL_DATABASE_USER = 'yourusername'
    MYSQL_DATABASE_PASSWORD = 'yourpassword'
    MYSQL_DATABASE_HOST = 'linktoyourdb' # eg to amazone db :- yourdbname.xxxxxxxxxx.us-east-2.rds.amazonaws.com
    MYSQL_DATABASE_DB = 'yourdbname'

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


#OLD STUFF 
# class Config(object):
#     """
#     Common configurations
#     """

#     # Put any configurations here that are common across all environments


# class DevelopmentConfig(Config):
#     """
#     Development configurations
#     """

#     DEBUG = True
#     SQLALCHEMY_ECHO = True


# class ProductionConfig(Config):
#     """
#     Production configurations
#     """

#     DEBUG = False


# app_config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig
# }