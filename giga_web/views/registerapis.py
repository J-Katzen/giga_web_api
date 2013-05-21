from giga_web import giga_web
from userapi import UserAPI
from projectapi import ProjectAPI
from campaignapi import CampaignAPI

app = giga_web


def register_api(view, endpoint, url, pk='id'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule('%s<%s>' % (url, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(UserAPI, 'user_api', '/users/', pk='id')
register_api(CampaignAPI, 'campaign_api', '/campaigns/', pk='campaign_perma')
register_api(ProjectAPI, 'project_api', '/projects/', pk='proj_id')
register_api(LeaderboardAPI,'leaderboard_api','/leaderboards/',pk='id')
