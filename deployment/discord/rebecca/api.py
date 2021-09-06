from fastapi import FastAPI
app = FastAPI()

def send_twitter_update():
    print("Pizza Time")

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}
