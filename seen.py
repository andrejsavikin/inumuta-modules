# -*- coding: utf8 -*-
"""
seen.py - Willie Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""

import time
import datetime
import pytz
from willie.tools import Ddict, Nick

seen_dict=Ddict(dict)

def get_tz(willie, nick):
    tz = 'asdf'
    if willie.db and nick in willie.db.preferences:
            tz = willie.db.preferences.get(nick, 'tz')
    if tz not in pytz.all_timezones_set:
        tz = 'UTC'
    return tz.strip()

def seen(willie, trigger):
    """Reports when and where the user was last seen."""
    if not trigger.group(2):
        willie.say(".seen <nick> - Reports when <nick> was last seen.")
        return
    nick = Nick(trigger.group(2).strip())
    if seen_dict.has_key(nick):
        timestamp = seen_dict[nick]['timestamp']
        channel = seen_dict[nick]['channel']
        message = seen_dict[nick]['message']

        tz = get_tz(willie, trigger.nick)
        saw = datetime.datetime.fromtimestamp(timestamp, pytz.timezone(tz))
        timestamp = saw.strftime('%Y-%m-%d %H:%M:%S %Z')

        msg = "I last saw %s at %s on %s, saying %s" % (nick, timestamp, channel, message)
        willie.say(str(trigger.nick) + ': ' + msg)
    else:
        willie.say("Sorry, I haven't seen %s around." % nick)
seen.commands = ['seen']

def note(willie, trigger):
    if trigger.sender.startswith('#'):
        nick = Nick(trigger.nick)
        seen_dict[nick]['timestamp'] = time.time()
        seen_dict[nick]['channel'] = trigger.sender
        seen_dict[nick]['message'] = trigger

note.rule = r'(.*)'
note.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
