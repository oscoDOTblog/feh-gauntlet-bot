from fastapi import FastAPI
app = FastAPI()

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}