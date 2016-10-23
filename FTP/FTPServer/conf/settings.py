
import os
BIND_HOST = '127.0.0.1'
BIND_PORT = 9992

BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_HOME = '%s\\var\\users' % BASE_DIR

USER_ACCOUNT = {
    "alex":{
        "password": "81dc9bdb52d04dc20036dbd8313ed055",
        "storage_limit": 2097152
    },
    "yuan":{
        "password": "900150983cd24fb0d6963f7d28e17f72",
        "storage_limit": 2097152
    },

}