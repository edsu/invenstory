import os
import json
import fondz
import logging
from os.path import join, isdir, abspath

from fondz.topics import topics
from fondz.convert import convert
from fondz.identify import identify, summarize
from fondz.utils import render_to, write_json, read_json


def create(fondz_dir, *bags, **kwargs):
    """
    create will initialize initialize a new fondz directory add one or more
    bags to it, convert what it can to web accessible formats, run topic 
    modeling, and format identification, and write out a HTML description
    """

    init(fondz_dir)

    # add all the bags
    for bag in bags:
        add_bag(fondz_dir, bag)
   
    fondz.convert(fondz_dir)
    fondz.identify(fondz_dir)
    fondz.topics(fondz_dir)
    write(fondz_dir)


def init(fondz_dir):
    mkdir(fondz_dir, "css")
    mkdir(fondz_dir, "images")
    mkdir(fondz_dir, "js")
    mkdir(fondz_dir, "originals")
    mkdir(fondz_dir, "derivatives")


def add_bag(fondz_dir, bag_dir):
    """
    add a particular bagit directory to the fondz description
    """
    # TODO: make sure bag_dir is actually a valid bag
    current_bags = os.listdir(join(fondz_dir, "originals"))
    next_orig = str(len(current_bags) + 1)
    link_name = join(fondz_dir, "originals", next_orig)
    bag_dir = os.path.abspath(bag_dir)
    logging.info("symlinking %s to %s", bag_dir, link_name)
    os.symlink(bag_dir, link_name)


def write(fondz_dir):
    index_file = join(fondz_dir, "index.html")
    topics = read_json(join(fondz_dir, "js", "topics.json"))
    formats = read_json(join(fondz_dir, "js", "formats.json"))
    format_summary = summarize(formats)

    render_to('index.html', index_file, 
              topics=topics,
              format_summary=format_summary)


def mkdir(*parts):
    path = join(*parts)
    if not isdir(path):
        os.makedirs(path)
