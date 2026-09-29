from django.apps import AppConfig
# AppConfig is a Django class that provides configuration information about an application.


class AccountsConfig(AppConfig): #It inherits from Django's: AppConfig
    name = 'accounts'   # so Your AccountsConfig gets the functionality provided by Django's AppConfig


"""
    Why does Django need this?

    Django needs to know about your application so that it can properly load things such as:

    -Models
    -Signals
    -Application configuration
    -App-specific initialization
    -Migrations
    -Other application-related components

"""