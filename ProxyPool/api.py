from flask import Flask,g
from ProxyPool.db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client

@app.route('/')
def index():
    return '<html>欢迎使用我的代理池</html>'

@app.route('/get/')
def get_proxy():
    return str(get_conn().pop())

@app.route('/count/')
def get_count():
    return str(get_conn().count())

if __name__ == '__main__':
    app.run(debug=True)