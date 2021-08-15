from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def count_pages():
    return data_manager.execute_select('SELECT COUNT(id) from shows;')


def get_seasons(show_id):
    query="""
    SELECT shows.id, season_number, seasons.title, seasons.overview from shows
    JOIN seasons on shows.id = seasons.show_id
    WHERE shows.id = %(s_id)s
    ORDER BY season_number;
    """
    return data_manager.execute_select(query, {'s_id': show_id})


def get_most_rated(page_start, page_size):
    query = """
        SELECT title, shows.id as id, year, runtime, trailer, homepage, round(rating, 1) as rating, 
        string_agg(genres.name, ', ' order by name) as names FROM shows 
        JOIN show_genres on shows.id = show_genres.show_id 
        JOIN genres on show_genres.genre_id = genres.id 
        GROUP BY shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, shows.rating, shows.id 
        ORDER BY rating DESC
        LIMIT %(page_size)s OFFSET %(p_s)s;
        """
    return data_manager.execute_select(query, {'p_s': page_start, 'page_size': page_size})


def show_data_by_id(show_id):
    query = """
    SELECT title, runtime as runtime, ROUND(rating, 1) as rating, year, coalesce(trailer, 'no url') as trailer,
    string_agg(genres.name, ', ') as genre_names, overview, actors.name as actor_name FROM shows
    JOIN show_genres on shows.id = show_genres.show_id
    JOIN genres on show_genres.genre_id = genres.id
    JOIN show_characters on shows.id = show_characters.show_id
    JOIN actors on actors.id = show_characters.actor_id
    WHERE shows.id = %(s_id)s
    GROUP BY shows.id, shows.title, shows.year, shows.runtime, shows.trailer, shows.homepage, shows.rating, actors.name;
    """
    return data_manager.execute_select(query, {'s_id': show_id})
