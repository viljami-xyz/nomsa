""" Environment settings """

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Environment settings

    Parameters
    ----------
    BaseSettings : BaseSettings
        Base class for environment settings
    """
    testuser:str
    testpass:str
    testdb:str

    port:str
    host:str

    openai_api_key:str
    openai_api_model:str
    
    class Config:
        """
        Configuration for environment settings

        Parameters
        ----------
        Config : Config
            Configuration for environment settings
        """
        env_file = "app/config/.env"
        env_file_encoding = "utf-8"
        case_sensitive = False