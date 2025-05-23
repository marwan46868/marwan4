from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

VALID_CODE = "cr7"
EXPIRY_DATE = datetime(2025, 9, 19, 22, 0, 59)

@app.route('/code=<code>/check-ban', methods=['GET'])
def check_ban(code):
    if code != VALID_CODE:
        return jsonify({
            'error': 'كود غير صالح، تواصل مع المالك @YU_z2',
            'dev': 'DEV BY : @YU_z2'
        }), 403

    if datetime.now() > EXPIRY_DATE:
        return jsonify({
            'error': 'انتهى الكود، تواصل مع المالك @YU_z2',
            'dev': 'DEV BY : @YU_z2'
        }), 403

    uid = request.args.get('uid')
    if not uid:
        return jsonify({
            'error': 'Missing uid parameter',
            'dev': 'DEV BY : @YU_z2'
        }), 400

    cookies = {
        '_gid': 'GA1.2.86931626.1745074338',
        '_ga_KE3SY7MRSD': 'GS1.1.1745074337.1.1.1745074342.0.0.0',
        '_ga_RF9R6YT614': 'GS1.1.1745074338.1.1.1745074342.0.0.0',
        '_ga': 'GA1.2.1363235624.1745074337',
    }

    headers = {
        'authority': 'ff.garena.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://ff.garena.com/en/support/',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-requested-with': 'B6FksShzIgjfrYImLpTsadjS86sddhFH',
    }

    params = {
        'lang': 'en',
        'uid': uid,
    }

    try:
        response = requests.get('https://ff.garena.com/api/antihack/check_banned',
                                params=params, cookies=cookies, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'banned': result['data']['is_banned'] == 1,
                'uid': uid,
                'dev': 'DEV BY : @YU_z2'
            })
        else:
            return jsonify({
                'error': 'Failed to connect to Garena API',
                'status_code': response.status_code,
                'dev': 'DEV BY : @YU_z2'
            }), 500
    except Exception as e:
        return jsonify({
            'error': 'Exception occurred: ' + str(e),
            'dev': 'DEV BY : @YU_z2'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)