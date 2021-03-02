import os

from fabric.decorators import task
from fabric.api import local

import utils


@task
def setup():
    utils.print_info("Setting up cap-examples")

    if not os.path.exists("settings.py"):
        utils.print_info("Setting up settings.py")
        local("cp config/settings.example.py config/settings.py")

    if not os.path.exists("./data"):
        utils.print_info("Setting up /data directory")
        local("mkdir data")

    utils.print_info("Installing requirements")
    local("pip install -r requirements.txt")

    print("Done.")
    utils.print_info("Register to get an API key => https://case.law/user/register/")
    print("=============================================================")
    utils.print_info("Once finished, copy the API key => https://case.law/user/details and paste it into config/settings.py")


@task
def get_cases_from_bulk(jurisdiction="Illinois", data_format="json"):
    """
    Gets all cases of a requested jurisdiction from /bulk if available
    Saves to /data folder
    """
    utils.get_and_extract_from_bulk(jurisdiction=jurisdiction, data_format=data_format)


@task
def show_api_url():
    url = utils.get_api_url()
    print(url)
    return url


@task
def list_jurisdictions():
    jurisdictions = utils.get_jurisdictions()
    for jurisdiction in jurisdictions:
        print(jurisdiction['name_long'])
    return jurisdictions


@task
def list_whitelisted_jurisdictions():
    jurisdictions = utils.get_jurisdictions()
    utils.print_info("Whitelisted jurisdictions")
    for jurisdiction in jurisdictions:
        if jurisdiction["whitelisted"]:
            print(jurisdiction['name_long'])
    return jurisdictions


@task
def list_blacklisted_jurisdictions():
    utils.print_info("Blacklisted jurisdictions")
    jurisdictions = utils.get_jurisdictions()
    for jurisdiction in jurisdictions:
        if not jurisdiction["whitelisted"]:
            print(jurisdiction['name_long'])
    return jurisdictions
