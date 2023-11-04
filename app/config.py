from dataclasses import dataclass


@dataclass
class Config:
    app_name = "upakarana"
    app_desc = "Python based cross platform launcher like app for productivity"
    app_version = "0.0.0"


config = Config()
