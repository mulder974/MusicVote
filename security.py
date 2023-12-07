import qrcode
from io import BytesIO
import random
import string
import psycopg2
import jwt
import datetime



def generate_token(length):
    # choose from all lowercase letter
    letters = string.ascii_letters + string.digits + string.hexdigits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def generate_qr():
    token = generate_token(16)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img.save("voting_qr_code.png")   
    return token

def generate_jwt(qr_code):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': qr_code
        }
        return jwt.encode(
            payload,
            'your_secret_key',  # Replace with your secret key
            algorithm='HS256'
        )
    except Exception as e:
        return e


def is_qr_valid(token):
    # Connect to the database
    conn = psycopg2.connect("postgresql://mulder974:nghtIMk7xrP3@ep-autumn-cake-33374612.eu-central-1.aws.neon.tech/PubSong?sslmode=require")
    cursor = conn.cursor()

    # Query to check if the token exists in the database
    query = "SELECT EXISTS(SELECT 1 FROM tokens WHERE token = %s);"
    cursor.execute(query, (token,))

    # Fetch the result
    result = cursor.fetchone()[0]

    # Close the connection
    cursor.close()
    conn.close()
    print(result)
    return result

def is_jwt_valid(token):
    try:
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

