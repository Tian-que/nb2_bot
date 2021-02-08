from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    plugin_setting: str = "default"

    class Config:
        extra = "ignore"