from giga_web import giga_web
from userapi import UserAPI
from projectapi import ProjectAPI
from campaignapi import CampaignAPI
from leaderboardapi import LeaderboardAPI
from clientapi import ClientAPI
from clientuserapi import ClientUserAPI
from donationapi import DonationAPI
from clientmapapi import ClientMapAPI
from verifymapapi import VerifyMapAPI

app = giga_web


def register_api(view, endpoint, url, pk='id'):
    view_func = view.as_view(endpoint)
    if endpoint in ['client_api', 'user_api']:
        app.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET', ])
    else:
        app.add_url_rule('/<cid>' + url, defaults={pk: None},
                         view_func=view_func, methods=['GET', ])
    if endpoint == 'project_api':
        app.add_url_rule('/<camp_id>/<proj_perma>/', defaults={pk: None},
                         view_func=view_func, methods=['GET'])

    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s>' % (url, pk), view_func=view_func,
                     methods=['GET', 'POST', 'DELETE'])

register_api(UserAPI, 'user_api', '/users/')
register_api(CampaignAPI, 'campaign_api', '/campaigns/', pk='campaign_perma')
register_api(ProjectAPI, 'project_api', '/projects/')
register_api(LeaderboardAPI, 'leaderboard_api', '/leaderboards/',)
register_api(ClientAPI, 'client_api', '/clients/')
register_api(ClientUserAPI, 'client_user_api', '/client_users/')
register_api(DonationAPI, 'donations_api', '/donations/')
register_api(ClientMapAPI, 'client_map_api', '/client_maps/')
register_api(VerifyMapAPI, 'verify_map_api', '/verify_maps/')
