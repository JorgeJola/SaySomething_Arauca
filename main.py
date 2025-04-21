from flask import Blueprint, Flask, render_template,request,jsonify
import psycopg2
main=Blueprint('main',__name__)

# First Interface
@main.route('/')
def first_interface():
    return render_template('first_interface.html')

@main.route('/SpatialComments')

def spcomments():
    return render_template('SpatialComments.html')

DB_CONFIG={
    'host':'dpg-cvr7f2vgi27c738n24q0-a',
    'dbname':'user_spatial_comments',
    'user':'jorgeandresjola',
    'password':'VI2TORlvj8WPUzxqeQwsdCOfIzkj2t10',
    'port': 5432 
}
# Generate the connection to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@main.route('/submit_comment', methods=['POST'])
def submit_comment():
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    year = request.form.get('year')

    if not all([name, email, comment, lat, lng,year]):
        return jsonify({'error': 'Missing data'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_comments (name, email, comment, latitude, longitude, year)
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (name, email, comment, lat, lng, int(year)))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Comment saved'}), 200
    except Exception as e:
        print("DB Error:", e)
        return jsonify({'error': 'Database error'}), 500