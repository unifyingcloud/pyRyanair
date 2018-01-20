from requests import get as rget
import json
from regex import sub as rsub
from configparser import ConfigParser
import argparse

# ---------------------------------------------------------------------------

def parse_args():
    """
    Parse command-line argruments
    """
    parser = argparse.ArgumentParser(description='Ryanair airporsst')

    g1 = parser.add_argument_group('Configuration')
    g1.add_argument('--config', '-cf', default='whatever',
                    help='Configuration file to load (default: %(default)s)')

    g2 = parser.add_argument_group('Behaviour')
    g2.add_argument('--debug', '-d', action='store_true', help='imprimir informacion de debug')
    g2.add_argument('--quiet', '-s', action='store_true')

    g3 = parser.add_argument_group('Input')
    g3.add_argument('origin', help='Which city departure')

    return parser.parse_args()

args = parse_args()

# ---------------------------------------------------------------------------

cfg = ConfigParser(allow_no_value=True)
cfg.read('../tpl/config.tpl')

# ---------------------------------------------------------------------------

def which_routes(origin, cfg):
    """

    :param cfg:
    :param origin:
    :return:
    """
    r = rget(url = cfg['base'] + cfg['api_airports'] + 'apikey=' + cfg['ckey'])

    coso = json.loads(r.content.decode('UTF-8'))

    airports = [airport['name'] for airport in coso]
    iataCode = [airport['iataCode'] for airport in coso]
    countryCode = [airport['countryCode'] for airport in coso]
    coordinates = [(airport['coordinates']['latitude'], airport['coordinates']['longitude']) for airport in coso]
    currencyCode = [airport['currencyCode'] for airport in coso]
    routes = [airport['routes'] for airport in coso]

    dicto = {}
    for idx, airport in enumerate(airports):
        inner_dicto = {}
        inner_dicto['iata'] = iataCode[idx]
        inner_dicto['country'] = countryCode[idx]
        inner_dicto['coord'] = coordinates[idx]
        inner_dicto['currency'] = currencyCode[idx]
        inner_dicto['routes'] = [rsub("_", " ", r.split(':')[1].title()) for r in routes[idx] if
                                 r.split(':')[0] == "city"]
        dicto[airport] = inner_dicto

    return dicto[origin]

# ---------------------------------------------------------------------------

print(which_routes(args.origin, cfg['RYANAIR'])['routes'])