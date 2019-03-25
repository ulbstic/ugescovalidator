import functools

from google import google


@functools.lru_cache( maxsize=1000 )
def search_google(query, num_page):
    """
    Search Google using the scraper https://github.com/abenassi/Google-Search-API
    Return the titles of the links and their descriptions.
    Other elements can be :
    name # The title of the link
    link # The external link
    google_link # The google link
    description # The description of the link
    cached # A link to the cached version of the page
    page # What page this result was on (When searching more than one page)
    index # What index on this page it was on
    """
    results = google.search( query + " wikipedia", num_page )
    try:
        return [i.link for i in results]
    except TypeError:
        return None


if __name__ == "__main__":
    print( search_google( "hamme escaut Flandre occiendtale", 1 ) )
