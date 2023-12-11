from flask import Flask, render_template
from datetime import datetime
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start Flask app in a separate thread
    threading.Thread(target=app.run, kwargs={'port': 5000, 'host': 'localhost'}, daemon=True).start()

    # Start Hypercorn server with HTTP/2 support
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config.from_mapping(
        bind="localhost:8000",
        http2=True,
    )

    # Start the server
    asyncio.run(serve(app, config))
