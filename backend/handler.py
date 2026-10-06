from mangum import Mangum

from app.main import app

# AWS Lambda entry point: set the Lambda handler to "handler.handler"
handler = Mangum(app)
