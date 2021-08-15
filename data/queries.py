from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def count_pages():
    return data_manager.execute_select('SELECT COUNT(id) from shows;')


def get_genres():
    query = """
        select distinct  id, name from genres
        order by name
        """

    return data_manager.execute_select(query)


def get_seasons(show_id):
    query = """
    SELECT shows.id, season_number, seasons.title, seasons.overview from shows
    JOIN seasons on shows.id = seasons.show_id
    WHERE shows.id = %(s_id)s
    ORDER BY season_number;
    """
    return data_manager.execute_select(query, {'s_id': show_id})


def get_show_by_season(letter):
    query = """
    SELECT shows.title from shows
    left join seasons s on shows.id = s.show_id
    WHERE s.title = 'Specials' AND shows.title ILIKE %(letter)s
    """
    return data_manager.execute_select(query, {'letter': '%' + letter + '%'})


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


def get_episodes(genre_id, page_size, min_episodes):
    query = """
    select shows.title, g.id, count(distinct s.show_id) as season_count, count(distinct e.season_id) as episode_count from shows
    left join show_genres sg on shows.id = sg.show_id
    left join genres g on g.id = sg.genre_id
    left join seasons s on shows.id = s.show_id
    left join episodes e on s.id = e.season_id
    where g.id = %(genre_id)s
    group by g.id, shows.title
    having count(distinct e.season_id) >= %(min_episodes)s
    order by episode_count desc
    limit %(page_size)s
    """
    return data_manager.execute_select(query,{'genre_id':genre_id, 'page_size':page_size, 'min_episodes':min_episodes})
