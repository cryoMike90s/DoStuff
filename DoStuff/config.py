import os


class Config:
    SECRET_KEY = '36efc808e2e7127d66370ba4548af728'
    SQLALCHEMY_DATABASE_URI = "sqlite:///dostuff.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
