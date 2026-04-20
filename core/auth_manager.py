token_store = {}

def save_token(name, token):
    token_store[name] = token

def get_token(name):
    return token_store.get(name)