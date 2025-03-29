from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import edge_tts
import asyncio
import tempfile
import os
import json

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

@app.route('/api/voices', methods=['GET'])
def get_voices():
    return jsonify(VOICES)

@app.route('/api/synthesize', methods=['POST'])
async def synthesize():
    data = request.json
    text = data.get('text')
    voice = data.get('voice')
    
    if not text or not voice:
        return jsonify({'error': 'Missing text or voice parameter'}), 400

    try:
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()

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
        return jsonify({'error': str(e)}), 500

    finally:
        # 清理临时文件
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 