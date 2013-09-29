#! /usr/bin/env python

import ConfigParser
import boto.swf.layer2 as swf

cf = ConfigParser.ConfigParser()
cf.read('swf.conf')
domain = cf.get('SWF', 'DOMAIN')

swf.Domain(name=domain).deprecate()
