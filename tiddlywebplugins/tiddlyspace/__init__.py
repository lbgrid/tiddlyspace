"""
TiddlySpace
A discoursive social model for TiddlyWiki

website: http://tiddlyspace.com
repository: http://github.com/TiddlySpace/tiddlyspace
"""

from tiddlyweb.web.extractor import UserExtract
from tiddlyweb.manage import make_command
from tiddlyweb.util import merge_config

from tiddlywebplugins.utils import replace_handler, get_store

from tiddlywebplugins.tiddlyspace.config import config as space_config
from tiddlywebplugins.tiddlyspace.handler import (home,
        friendly_uri, get_identities, ControlView)
from tiddlywebplugins.tiddlyspace.spaces import (
        add_spaces_routes, change_space_member)


__version__ = '0.2.2'


def init(config):
    """
    Establish required plugins and HTTP routes.
    """
    import tiddlywebwiki
    import tiddlywebplugins.logout
    import tiddlywebplugins.virtualhosting # calling init not required
    import tiddlywebplugins.magicuser
    import tiddlywebplugins.socialusers
    import tiddlywebplugins.mselect
    import tiddlywebplugins.cookiedomain
    import tiddlywebplugins.tiddlyspace.validator
    import tiddlywebplugins.prettyerror
    import tiddlywebplugins.form

    @make_command()
    def addmember(args):
        """Add a member to a space. <space name> <user name>"""
        store = get_store(config)
        space_name, username = args
        change_space_member(store, space_name, add=username)
        return True

    @make_command()
    def delmember(args):
        """Delete a member from a space. <space name> <user name>"""
        store = get_store(config)
        space_name, username = args
        change_space_member(store, space_name, remove=username)
        return True

    merge_config(config, space_config)

    tiddlywebwiki.init(config)
    tiddlywebplugins.logout.init(config)
    tiddlywebplugins.magicuser.init(config)
    tiddlywebplugins.socialusers.init(config)
    tiddlywebplugins.mselect.init(config)
    tiddlywebplugins.cookiedomain.init(config)
    tiddlywebplugins.prettyerror.init(config)
    tiddlywebplugins.form.init(config)

    if 'selector' in config: # system plugin
        replace_handler(config['selector'], '/', dict(GET=home))
        add_spaces_routes(config['selector'])
        config['selector'].add('/{tiddler_name:segment', GET=friendly_uri)
        config['selector'].add('/users/{username}/identities',
                GET=get_identities)
        if ControlView not in config['server_request_filters']:
            config['server_request_filters'].insert(
                    config['server_request_filters'].
                    index(UserExtract) + 1, ControlView)
