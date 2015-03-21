''' Tests the concurrency of the requests to make sure we aren't doing anything blocking
'''

import click
import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

@click.group()
def cli():
    ''' An upload tool to test media uploads. Encodes your images, just tell it where to find them
    \b
        media_upload.py post URL -t dropbox_token -f file_path
    '''
    pass


@cli.command()
@click.argument('url', metavar='URL', required=True)
@click.option('--number', default=10, help='The number of requests to make.')
def get(url, number):
    urls = [url for i in range(0, number)]
    pool = ThreadPool(number)
    # Map over the media
    response_times = pool.map(get_request, urls)
    # Close the pool
    pool.close()
    pool.join()

    for time in response_times:
        print(time)

    return

def get_request(url):
    resp = requests.get(url)
    return resp.elapsed


if __name__=='__main__':
    cli()
