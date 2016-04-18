import yaml

SECRET_KEY = 'some key'

DB_URI = 'sqlite:///ircb.db'

SUBSCRIBER_ENDPOINTS = {
    'stores': 'tcp://127.0.0.1:35000',
}

LOGGING_CONF = yaml.load("""
    version: 1

    formatters:
      simple:
        datefmt: '%Y-%m-%d %H:%M:%S'
        format: '[%(asctime)s][%(name)10s %(levelname)7s] %(message)s'

    handlers:
      console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout

    loggers:
      simpleExample:
        level: DEBUG
        handlers: [console]
        propagate: no

    root:
      level: DEBUG
      handlers: [console]
""")

INTERNAL_HOST = '127.0.0.1'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# A 32 byte string
WEB_SALT = b'c237202ee55411e584f4cc3d8237ff4b'
