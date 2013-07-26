# -*- coding: utf-8 -*-
from giga_web import celery
from wsgiref.handlers import format_date_time
from datetime import datetime, timedelta
from time import mktime


@celery.task
def confirm_donation(self, data):
    active_ids = dict()
    aidx = 0
    for proj in data['proj_list']:
        up, project_id = self.update_project_post(proj)
        if 'error' in up:
            return up
        if project_id is not None:
            active_ids[aidx] = project_id
            aidx += 1
    # update campaign
    camp, leader_id = self.update_campaign_post(data, active_ids)
    if 'error' in camp:
        return camp
    # update leaderboard
    lead = self.update_leaderboard_post(data, leader_id)
    if 'error' in lead:
        return lead


def update_project_post(self, data):
    p = helpers.generic_get('/projects/', data['proj_id'])
    pj = p.json()
    pop_proj_id = None
    pj['raised'] += data['donated']
    if pj['raised'] >= pj['goal']:
        now = datetime.now()
        stamp = mktime(now.timetuple())
        pj['completed'] = format_date_time(stamp)
        if pj['type'] == 'rolling':
            pj['active'] = False
            # find popular voted on projects
            parm = dict()
            parm['where'] = '{"camp_id": "%s","active": false, "type": { "$in": ["rolling", "uncapped"]}}' % pj['camp_id']
            parm['max_results'] = 1
            popular_req = requests.get(crud_url + '/projects/', params=parm)
            pop_req_j = popular_req.json()
            if len(pop_req_j['_items']) > 0:
                pop_proj = pop_req_j['_items'][0]
                pop_proj['active'] = True
                pop_proj_id = pop_proj['_id']
                upd_pop = helpers.generic_patch('/projects/', pop_proj, pop_proj['etag'])
                if 'error' not in upd_pop:
                    upd_p = helpers.generic_patch('/projects/', pj, pj['etag'])
                else:
                    upd_p = {'error': 'Could not set new active project'}
    else:
        upd_p = helpers.generic_patch('/projects/', pj, pj['etag'])
    return upd_p, pop_proj_id


def update_campaign_post(self, data, active_ids):
    camp = helpers.generic_get('/campaigns/', data['camp_id'])
    camp_j = camp.json()
    lead_id = camp_j['leaderboard_id']
    camp_j['total_raised'] += data['total_donated']
    for projs in data['proj_list']:
        activelist_proj = next((d for d in camp_j['active_list'] if
                                d['p_id'] == projs['proj_id']), None)
        if activelist_proj is not None:
            activelist_proj['raised'] += projs['donated']
            camp_j['active_list'][:] = [d for d in camp_j['active_list']
                                        if d['p_id'] != projs['proj_id']]
            camp_j['active_list'].append(activelist_proj)
    if len(active_ids) > 0:
        for projs in data['proj_list']:
            camp_j['active_list'][:] = [d for d in camp_j['active_list']
                                        if d['p_id'] != projs['proj_id']]
        for active_id in active_ids:
            active_p = helpers.generic_get('/projects/', active_id)
            active_pj = active_p.json()
            now = datetime.now()
            stamp = mktime(now.timetuple())
            d_start = format_date_time(stamp)
            if 'sumnmary' not in active_pj:
                summary = active_pj['description'][0:254]
                active_pj['summary'] = summary[:summary.rfind('.') + 1]
            if 'thumbnail' not in active_pj:
                active_pj['thumbnail'] = 'https://s3.amazonaws.com/media.gigawatt.co/img/add.png'
            new_active_proj = {'p_id': active_pj['_id'],
                               'proj_name': active_pj['name'],
                               'perma_name': active_pj['perma_name'],
                               'type': active_pj['type'],
                               'raised': active_pj['raised'],
                               'description': active_pj['summary'],
                               'goal': active_pj['goal'],
                               'proj_thumb': active_pj['thumbnail'],
                               'date_start': d_start}

            if active_pj['type'] != 'uncapped':
                c_start = datetime.strptime(d_start, '%a, %d %b %Y %H:%M:%S GMT')
                d_end = (c_start + timedelta(active_pj['length'])).strftime('%a, %d %b %Y %H:%M:%S GMT')
                camp_end = datetime.strptime(camp_j['date_end'], '%a, %d %b %Y %H:%M:%S GMT')
                dc_end = datetime.strptime(d_end, '%a, %d %b %Y %H:%M:%S GMT')
                if dc_end > camp_end:
                    new_active_proj['date_end'] = camp_j['date_end']
                else:
                    new_active_proj['date_end'] = d_end
            else:
                new_active_proj['date_end'] = camp_j['date_end']
            camp_j['total_goal'] += new_active_proj['goal']
            camp_j['active_list'].append(new_active_proj)
    upd_camp = helpers.generic_patch('/campaigns/', camp_j, camp_j['etag'])
    return upd_camp, lead_id


def update_leaderboard_post(self, data, lead_id):
    lead = helpers.generic_get('/leaderboards/', lead_id)
    lead_j = lead.json()
    lead_j['raised'] += data['total_donated']
    if 'ref' in data:
        lead_j['referred'] += data['total_donated']
        # find out if the referral id is in the leaderboard list
        user = next((d for d in lead_j['donors'] if
                     d['user_id'] == data['ref']), None)
        # if so, update the stats!
        if user is not None:
            lead_j['donors'][:] = [d for d in lead_j['donors']
                                   if d['user_id'] != data['ref']]
            user['ref'] += data['total_donated']
            user['combined'] += data['total_donated']
            lead_j['donors'].append(user)
    # check if user donating is already in leaderboard
    if 'user_id' not in data:
        data['user_id'] = "51e3b7ac855d9179965bda38"
    user2 = next((d for d in lead_j['donors'] if
                  d['user_id'] == data['user_id']), None)
    if user2 is not None:
        lead_j['donors'][:] = [d for d in lead_j['donors']
                               if d['user_id'] != data['user_id']]
        user2['donated'] += data['total_donated']
        user2['combined'] += data['total_donated']
        lead_j['donors'].append(user2)
    else:
        n_user = helpers.generic_get('/users/', data['user_id'])
        n_user = n_user.json()
        if ('first_name' in data) and ('last_name' in data):
            data['name'] = data['first_name'] + ' ' + data['last_name']
        elif ('firstname' in n_user) and ('lastname' in n_user):
            data['name'] = n_user['firstname'] + ' ' + n_user['lastname']
        else:
            data['name'] = data['email']

        if 'avatar_url' in n_user:
            data['avatar'] = n_user['avatar_url']
        else:
            data['avatar'] = "https://s3.amazonaws.com/media.gigawatt.co/img/johnsmith.jpg"
        lead_j['donors'].append({'name': data['name'],
                                 'user_id': data['user_id'],
                                 'donated': data['total_donated'],
                                 'avatar': data['avatar'],
                                 'ref': 0,
                                 'combined': data['total_donated']})

    upd_lead = helpers.generic_patch('/leaderboards/', lead_j, lead_j['etag'])
    return upd_lead
