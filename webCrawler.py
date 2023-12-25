from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import csv
import json
import random
from urllib.parse import urlparse
import os
import tldextract
from collections import Counter