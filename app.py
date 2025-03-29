from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import edge_tts
import asyncio
import tempfile
import os
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 支持的语音列表
VOICES = {
    'en-US': [
        {'name': 'en-US-ChristopherNeural', 'gender': 'Male'},
        {'name': 'en-US-EricNeural', 'gender': 'Male'},
        {'name': 'en-US-GuyNeural', 'gender': 'Male'},
        {'name': 'en-US-RogerNeural', 'gender': 'Male'},
        {'name': 'en-US-SteffanNeural', 'gender': 'Male'},
        {'name': 'en-US-JennyNeural', 'gender': 'Female'},
        {'name': 'en-US-AriaNeural', 'gender': 'Female'},
        {'name': 'en-US-EmmaNeural', 'gender': 'Female'},
        {'name': 'en-US-MichelleNeural', 'gender': 'Female'},
        {'name': 'en-US-SaraNeural', 'gender': 'Female'},
    ],
    'es-ES': [
        {'name': 'es-ES-AlvaroNeural', 'gender': 'Male'},
        {'name': 'es-ES-ArnauNeural', 'gender': 'Male'},
        {'name': 'es-ES-DarioNeural', 'gender': 'Male'},
        {'name': 'es-ES-EliasNeural', 'gender': 'Male'},
        {'name': 'es-ES-EstebanNeural', 'gender': 'Male'},
        {'name': 'es-ES-ElviraNeural', 'gender': 'Female'},
        {'name': 'es-ES-AbrilNeural', 'gender': 'Female'},
        {'name': 'es-ES-IreneNeural', 'gender': 'Female'},
        {'name': 'es-ES-LiaNeural', 'gender': 'Female'},
        {'name': 'es-ES-TrianaNeural', 'gender': 'Female'},
    ],
    'pt-PT': [
        {'name': 'pt-PT-DuarteNeural', 'gender': 'Male'},
        {'name': 'pt-PT-RaquelNeural', 'gender': 'Female'},
        {'name': 'pt-BR-AntonioNeural', 'gender': 'Male'},
        {'name': 'pt-BR-BrendaNeural', 'gender': 'Female'},
        {'name': 'pt-BR-FabioNeural', 'gender': 'Male'},
        {'name': 'pt-BR-FranciscaNeural', 'gender': 'Female'},
        {'name': 'pt-BR-GiovannaNeural', 'gender': 'Female'},
        {'name': 'pt-BR-HumbertoNeural', 'gender': 'Male'},
        {'name': 'pt-BR-LeticiaNeural', 'gender': 'Female'},
        {'name': 'pt-BR-ManuelaNeural', 'gender': 'Female'},
    ]
}

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/voices', methods=['GET'])
def get_voices():
    try:
        logger.info("Fetching available voices")
        return jsonify(VOICES)
    except Exception as e:
        logger.error(f"Error fetching voices: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/synthesize', methods=['POST'])
async def synthesize():
    try:
        data = request.json
        text = data.get('text')
        voice = data.get('voice')
        
        if not text or not voice:
            logger.warning("Missing parameters in synthesize request")
            return jsonify({'error': 'Missing text or voice parameter'}), 400

        logger.info(f"Synthesizing text with voice: {voice}")
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()

        try:
            # 合成语音
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(temp_file.name)

            # 返回音频文件
            return send_file(
                temp_file.name,
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name='speech.mp3'
            )

        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}")
            return jsonify({'error': str(e)}), 500

        finally:
            # 清理临时文件
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port) 