from flask import Flask, request,jsonify
from .service.messageService import MessageService
from .service.redisService import RedisService
from kafka import KafkaProducer
import json
import os
# import jsonpickle



app = Flask(__name__)
app.config.from_pyfile('config.py')



messageService= MessageService();
redisService= RedisService()
kafka_host = os.getenv('KAFKA_HOST', 'localhost')
kafka_port = os.getenv('KAFKA_PORT', '9092')
secret_key= os.getenv('OPENAI_API_KEY');
kafka_bootstrap_servers = f"{kafka_host}:{kafka_port}"
print("Kafka server is "+kafka_bootstrap_servers)
print("\n")
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))




@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    user_id = request.headers.get('x-user-id')
    if not user_id:
        return jsonify({'error': 'x-user-id header is required'}), 400
    
    print("User id ==== "+ user_id);
    message= request.json.get('message')
    result= messageService.process_message(user_id, message)
    
    if result is not None:
        serialized_result= result.serialize();
        serialized_result['user_id'] = user_id
        producer.send('expense_service', serialized_result)
        print("the data", serialized_result);
        return jsonify(serialized_result)
    else:
        return jsonify({'error': 'Invalid message format'}), 400
    
    
@app.route('/api/v1/developer', methods=['GET'])
def handle_get():
    
    cache_key="ds-service:developer"
    cached_response = redisService.get(cache_key)
    if cached_response is not None:
        print("Developer Redis cache HIT")
        return jsonify(cached_response)
    
    print("Developer Redis cache MISS")
    
    response = {
        "developer": "Roshan Jaiswal (CodeCortex)",
        "contact": {
            "linkedin": "https://www.linkedin.com/in/codecortex/",
            "instagram": "https://www.instagram.com/codecortexx/",
            "github": "https://github.com/CodeCortex"
        }
    }
    
    redisService.set(
        cache_key,
        response,
        ttl=3600
    )
    
    return jsonify(response)
 
 
@app.route("/health", methods=['GET'])
def health_check():
    return 'OK'
        
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)