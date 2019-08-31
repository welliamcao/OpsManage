#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import time
from celery import task
from utils import base
from asset.models import Assets
from django.contrib.auth.models import User 
