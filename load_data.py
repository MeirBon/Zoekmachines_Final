#!/usr/bin/env python3

from src.es_init import load_data, get_connection

if __name__ == '__main__':
    load_data(get_connection())
