import aiohttp
import asyncio
import logging
from django.conf import settings
from movies.models import Movie
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

OMDB_API_URL = "http://www.omdbapi.com/"

async def fetch_movie_details(movie_title):
    """
    Asynchronously fetch movie details from OMDB API
    """
    try:
        api_key = settings.OMDB_API_KEY
        params = {
            'apikey': api_key,
            't': movie_title,
            'plot': 'short',
            'r': 'json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(OMDB_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('Response') == 'True':
                        return {
                            'title': data.get('Title'),
                            'year': data.get('Year'),
                            'rated': data.get('Rated'),
                            'released': data.get('Released'),
                            'runtime': data.get('Runtime'),
                            'genre': data.get('Genre'),
                            'director': data.get('Director'),
                            'actors': data.get('Actors'),
                            'plot': data.get('Plot'),
                            'poster': data.get('Poster'),
                            'external_id': data.get('imdbID'),
                            'imdb_rating': data.get('imdbRating')
                        }
                    return {'error': 'Movie not found'}
                return {'error': f'API Error: {response.status}'}
    except Exception as e:
        logger.error(f"Error fetching movie details: {str(e)}")
        return {'error': f'Failed to fetch movie details: {str(e)}'}

async def fetch_movie_search(search_term):
    """
    Asynchronously search for movies from OMDB API
    """
    try:
        api_key = settings.OMDB_API_KEY
        params = {
            'apikey': api_key,
            's': search_term,
            'r': 'json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(OMDB_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('Response') == 'True':
                        search_results = []
                        for item in data.get('Search', [])[:5]:  
                            movie_id = item.get('imdbID')
                            movie_details = await fetch_movie_by_id(movie_id, session)
                            if 'error' not in movie_details:
                                search_results.append(movie_details)
                        return search_results
                    return []
                return []
    except Exception as e:
        logger.error(f"Error searching movies: {str(e)}")
        return []

async def fetch_movie_by_id(movie_id, session=None):
    """
    Fetch movie details by IMDB ID
    """
    try:
        close_session = False
        if session is None:
            session = aiohttp.ClientSession()
            close_session = True
            
        api_key = settings.OMDB_API_KEY
        params = {
            'apikey': api_key,
            'i': movie_id,
            'plot': 'short'
        }
        
        async with session.get(OMDB_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('Response') == 'True':
                    return {
                        'title': data.get('Title'),
                        'year': data.get('Year'),
                        'rated': data.get('Rated'),
                        'runtime': data.get('Runtime'),
                        'genre': data.get('Genre'),
                        'director': data.get('Director'),
                        'actors': data.get('Actors'),
                        'plot': data.get('Plot'),
                        'poster': data.get('Poster'),
                        'external_id': data.get('imdbID'),
                        'imdb_rating': data.get('imdbRating')
                    }
            return {'error': 'Movie not found'}
    except Exception as e:
        logger.error(f"Error fetching movie by ID: {str(e)}")
        return {'error': f'Failed to fetch movie details: {str(e)}'}
    finally:
        if close_session and session:
            await session.close()

@sync_to_async
def create_or_update_movie_in_db(movie_data):
    """
    Create or update a movie in the database (sync function)
    """
    try:
        year_value = None
        if movie_data.get('year'):
            try:
                year_str = movie_data.get('year', '').split('–')[0].strip()
                year_value = int(year_str) if year_str.isdigit() else None
            except (ValueError, TypeError):
                year_value = None
        
        imdb_rating = None
        if movie_data.get('imdb_rating'):
            try:
                imdb_rating = float(movie_data.get('imdb_rating'))
            except (ValueError, TypeError):
                imdb_rating = None
        
        movie, created = Movie.objects.update_or_create(
            title=movie_data['title'],
            defaults={
                'external_id': movie_data.get('external_id'),
                'year': year_value,
                'rated': movie_data.get('rated'),
                'runtime': movie_data.get('runtime'),
                'genre': movie_data.get('genre'),
                'director': movie_data.get('director'),
                'actors': movie_data.get('actors'),
                'plot': movie_data.get('plot'),
                'poster': movie_data.get('poster'),
                'imdb_rating': imdb_rating
            }
        )
        return movie
    except Exception as e:
        logger.error(f"Error saving movie: {str(e)}")
        return None

async def save_movie_details(movie_title):
    """
    Fetch movie details and save to database
    """
    movie_data = await fetch_movie_details(movie_title)
    
    if 'error' not in movie_data:
        try:
            movie = await create_or_update_movie_in_db(movie_data)
            return movie
        except Exception as e:
            logger.error(f"Error in save_movie_details: {str(e)}")
            return None
    return None

def get_movie_from_db(movie_title):
    """
    Get movie from database (sync function)
    """
    movie = Movie.objects.filter(title__iexact=movie_title).first()
    
    if movie:
        return movie
    
    return Movie.objects.filter(title__icontains=movie_title).first()

def get_or_create_movie(movie_title):
    """
    Get movie from database or fetch from API if not found
    """
    movie = get_movie_from_db(movie_title)
    if movie:
        return movie
        
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(save_movie_details(movie_title))
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Failed to get or create movie: {str(e)}")
        return None

def search_external_movies(search_term):
    """
    Search for movies from the external API
    Returns a list of movie data dictionaries
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(fetch_movie_search(search_term))
        finally:
            loop.close()
    except Exception as e:
        logger.error(f"Error in search_external_movies: {str(e)}")
        return []