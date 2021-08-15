from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)

@app.route('/shows/most-rated/<page_number>')
def shows_most_rated(page_number):
    page_size = 15
    page_number = int(page_number)
    page_start = (page_number -1) * page_size
    shows = queries.get_most_rated(page_start, page_size)
    count = queries.count_pages()[0]['count']
    number_of_shows = int(count / 15)
    return render_template('most-rated.html', shows=shows, num_of_pages=number_of_shows, page_number=page_number)


def main():
    app.run(debug=False)


if __name__ == '__main__':
    main()
