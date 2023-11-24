import spotify

from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voting')
def voting():
    return render_template('voting.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    songs = spotify.search_song("BQD9x6uHPDMs6QolRfpRqZR_NKgr7RySjg-b8byVFIpjH-6a_qDX5YVb9KzFIPDMvvjkEMSLZtJFiCr-uTecdnHdV-wZLEuUteQzScZTISSEms4OEGM",query)
    search_results_template = """
        <h2>Search Results</h2>
        <ul>
            {% for song in songs %}
            <li>
                <h3>{{ song['name'] }}</h3>
                <p>Artist: {{ song['artist'] }}</p>
                <p>Album: {{ song['album'] }}</p>
                <audio controls>
                    <source src="{{ song['preview_url'] }}" type="audio/mpeg">
                </audio>
            </li>
            {% endfor %}
        </ul>
    """
    rendered_results = render_template_string(search_results_template, songs=songs)

    return rendered_results

if __name__ == '__main__':
    app.run(debug=True)