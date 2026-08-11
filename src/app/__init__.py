from flask import Flask, request,jsonify
from service.messageService import MessageService


app = Flask(__name__)
app.config.from_pyfile('config.py')


messageService= MessageService();



@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message= request.json.get('message')
    result= messageService.process_message(message)
    
    if result is not None:
        serialized_result= result.serialize();
        return jsonify(serialized_result)
    else:
        return jsonify({'error': 'Invalid message format'}), 400
    
    
@app.route('/', methods=['GET'])
def handle_get():
     return jsonify({ "message": "Roshan Jaiswal (CodeCortex) -- ds-service"})
 
 
@app.route("/health", methods=['GET'])
def health_check():
    return 'OK'
        
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)