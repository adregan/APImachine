
import click
import requests
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


@click.group()
def cli():
    ''' Tests the concurrency of the requests to make sure
        we aren't doing anything blocking
    '''
    pass


@cli.command()
@click.argument('url', metavar='URL', required=True)
@click.option('--number', default=10, help='The number of requests to make.')
def get(url, number):
    start = time.time()
    urls = [url for i in range(0, number)]
    pool = ThreadPool(number)
    # Map over the media
    response_times = pool.map(get_request, urls)
    # Close the pool
    pool.close()
    pool.join()

    for resp_time in response_times:
        print(resp_time)

    total_seconds = int(time.time() - start)
    seconds = total_seconds % 60

    print('TOTAL time {seconds} sec'.format(seconds=seconds))

    return


def get_request(url):
    resp = requests.get(url)
    return resp.elapsed

if __name__ == '__main__':
    cli()
