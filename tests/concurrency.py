''' Tests the concurrency of the requests to make sure we aren't doing anything blocking
'''

import click
import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

@click.command()
@click.option('--url', default=None, help='The url to request.')
@click.option('--number', default=10, help='The number of requests to make.')

def test(url, number):
    urls = [url for i in range(0, number)]
    pool = ThreadPool(number)
    # Map over the media
    response_times = pool.map(get_request, urls)
    # Close the pool
    pool.close()
    pool.join()

    for time in response_times:
        print(time)

def get_request(url):
    resp = requests.get(url)
    return resp.elapsed

if __name__ == '__main__':
    test()
