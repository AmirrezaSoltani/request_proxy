from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import requests
import logging
import os
from datetime import datetime

# Configure logging
# logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.environ.get('PORT', 80))

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'paystar-proxy'
    })

@app.route('/proxy', methods=['POST'])
def proxy_request():
    """Main proxy endpoint that forwards requests to Paystar API"""
    try:
        # Get the config from request body
        data = request.get_json()
        
        if not data or 'config' not in data:
        
            return jsonify({'err': "send data"}), 400
        
        config = data['config']
        
        # Log basic request info
  
        # Make the request with streaming enabled
        proxied_response = requests.request(
            method=config.get('method', 'GET'),
            url=config.get('url'),
            headers=config.get('headers', {}),
            data=config.get('data'),
            json=config.get('json'),
            params=config.get('params'),
            stream=True,  # Enable streaming for large responses
            timeout=config.get('timeout', 30)
        )
        
        # Log response status
     

        # Get headers to forward, excluding those that can cause issues
        headers_to_forward = {
            key: value for key, value in proxied_response.headers.items()
            if key.lower() not in ['content-encoding', 'transfer-encoding', 'connection']
        }

        # Create a generator to stream the content chunk by chunk
        def generate():
            for chunk in proxied_response.iter_content(chunk_size=8192):
                yield chunk
        
        # Return a streaming response to the client
        return Response(stream_with_context(generate()), status=proxied_response.status_code, headers=headers_to_forward)
        
    except requests.exceptions.RequestException as e:
     
        return jsonify({
            'err': "err",
            'details': str(e)
        }), 500
        
    except Exception as e:
      
        return jsonify({
            'err': "err",
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'err': "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
 
    return jsonify({'err': "Internal server error"}), 500

if __name__ == '__main__':

    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False
    ) 