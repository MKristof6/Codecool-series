from flask import Flask, render_template, url_for, jsonify
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('Codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/shows/most-rated/<page_number>')
def shows_most_rated(page_number):
    page_size = 15
    page_number = int(page_number)
    page_start = (page_number - 1) * page_size
    shows = queries.get_most_rated(page_start, page_size)
    count = queries.count_pages()[0]['count']
    number_of_shows = int(count / 15)
    return render_template('most-rated.html', shows=shows, num_of_pages=number_of_shows, page_number=page_number)


@app.route('/show/<show_id>')
def shows_page(show_id):
    show_data = queries.show_data_by_id(show_id)
    actors_num = len(show_data)
    video_id = show_data[0]['trailer'][27:]
    season_data = queries.get_seasons(show_id)
    hour = 0
    while show_data[0]['runtime'] > 60:
        show_data[0]['runtime'] -= 60
        hour += 1
    minute = show_data[0]['runtime']
    if hour != 0:
        runtime = f'{hour}h{minute}m'
    else:
        runtime = f'{minute}m'
    return render_template('shows-page.html', show=show_data, seasons=season_data, video_id=video_id,
                           actors_num=actors_num, runtime=runtime)


@app.route('/shows')
def seasons():
    return render_template('search-for-show.html')


@app.route('/get-shows/<letter>')
def get_seasons(letter):
    data = queries.get_show_by_season(letter)
    return jsonify(data)


@app.route('/shows-by-genre')
def genres():
    data = queries.get_genres()
    return render_template('shows_by_genre.html', genres=data)


@app.route('/get-shows-by-genre/<genre_id>')
def get_shows(genre_id):
    page_size = 50
    min_episodes = 20
    shows = queries.get_episodes(genre_id, page_size, min_episodes)
    return jsonify(shows)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
