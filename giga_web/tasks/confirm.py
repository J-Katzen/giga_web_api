# -*- coding: utf-8 -*-
from giga_web import celery, helpers, celery_logger
from giga_web import Lock, LockTimeout
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

logger = celery_logger


@celery.task
def confirm_donation(data):
    logger.info('task confirm_donation called. args: %s', str(data))
    # update user
    update_user_post.delay(data)
    # update referring user if available
    if 'ref' in data:
        if data['ref'] == data['user_id']:
            data.pop('ref', None)
        else:
            data['ref'] = helpers.baseconvert(data['ref'], helpers.BASE62, helpers.BASE16)
            # update the referring user with donation data :D
    for proj in data['proj_list']:
        update_project_post.delay(proj)
    # update campaign
    update_campaign_post.delay(data)
    # update leaderboard
    update_leaderboard_post.delay(data)
    return


@celery.task
def update_user_post(data):
    try:
        with Lock('u_' + data['user_id']):
            logger.info('task update_user_post. args: %s', str(data))
            p = helpers.generic_get('/users/', data['user_id'])
            pj = p.json()
            new_donated = {}
            new_donated['client_id'] = data['client_id']
            new_donated['camp_id'] = data['camp_id']
            new_donated['amt'] = data['total_donated']
            new_donated['amt_ref'] = 0
            new_donated['people_ref_ct'] = 0
            new_donated['people_ref_names'] = []
            if 'class_year' in data:
                new_donated['class_year'] = data['class_year']
            if 'donated' not in pj:
                pj['donated'] = [new_donated]
            else:
                client_list_idx = helpers.get_index(pj['donated'], 'camp_id', data['camp_id'])
                if client_list_idx is None:
                    pj['donated'].append(new_donated)
                else:
                    pj['donated'][client_list_idx]['amt'] += data['total_donated']
            try:
                upd_p = helpers.generic_patch('/users/', pj, pj['etag'])
            except:
                update_user_post.delay(data)
                return
            if 'error' in upd_p:
                update_user_post.delay(data)
                return
            return
    except:
        update_user_post.delay(data)


@celery.task
def update_project_post(data):
    try:
        with Lock('p_' + data['proj_id']):
            logger.info('task update_project_post. args: %s', str(data))
            p = helpers.generic_get('/projects/', data['proj_id'])
            pj = p.json()
            pj['raised'] += data['donated']
            if ('second_class_year' in data) and ('second_fullname' in data):
                pj['donor_count'] += 1
            pj['donor_count'] += 1
            if (pj['raised'] >= pj['goal']) and ('completed' not in pj):
                now = datetime.now()
                stamp = mktime(now.timetuple())
                pj['completed'] = format_date_time(stamp)
            try:
                upd_p = helpers.generic_patch('/projects/', pj, pj['etag'])
            except:
                update_project_post.delay(data)
                return
            if 'error' in upd_p:
                update_project_post.delay(data)
                return
            return
    except:
        update_project_post.delay(data)


@celery.task
def update_campaign_post(data):
    try:
        with Lock('c_' + data['camp_id']):
            logger.info('task update_campaign_post called. args: %s', str(data))
            camp = helpers.generic_get('/campaigns/', data['camp_id'])
            camp_j = camp.json()
            camp_j['total_raised'] += data['total_donated']
            if ('second_class_year' in data) and ('second_fullname' in data):
                camp_j['total_donor_count'] += 1
            camp_j['total_donor_ct'] += 1
            for projs in data['proj_list']:
                activelist_proj = helpers.get_index(camp_j['active_list'], 'p_id', projs['proj_id'])
                if activelist_proj is not None:
                    camp_j['active_list'][activelist_proj]['raised'] += projs['donated']
                    camp_j['active_list'][activelist_proj]['donor_count'] += 1
            try:
                upd_camp = helpers.generic_patch('/campaigns/', camp_j, camp_j['etag'])
            except:
                update_campaign_post.delay(data)
                return
            if 'error' in upd_camp:
                update_campaign_post.delay(data)
                return
            return
    except:
        update_project_post.delay(data)


@celery.task
def update_leaderboard_post(data):
    try:
        camp = helpers.generic_get('/campaigns/', data['camp_id'])
        camp_j = camp.json()
        lead_id = camp_j['leaderboard_id']
        with Lock('l_' + lead_id):
            logger.info('task update_leaderboard_post called. args: %s', str(data))
            lead = helpers.generic_get('/leaderboards/', lead_id)
            lead_j = lead.json()
            lead_j['raised'] += data['total_donated']
            if 'class_year' in data:
                if 'class_yr_totals' in lead_j:
                    class_yr_idx = helpers.get_index(lead_j['class_yr_totals'], 'year', data['class_year'])
                    if class_yr_idx is not None:
                        lead_j['class_yr_totals'][class_yr_idx]['amount'] += data['total_donated']
                    else:
                        lead_j['class_yr_totals'].append({'year': data['class_year'],
                                                          'amount': data['total_donated']})
                else:
                    lead_j['class_yr_totals'] = [{'year': data['class_year'],
                                                  'amount': data['total_donated']}]
            if 'ref' in data:
                lead_j['referred'] += data['total_donated']
                # find out if the referral id is in the leaderboard list
                user_idx = helpers.get_index(lead_j['donors'], 'user_id', data['ref'])
                # if so, update the stats!
                if user_idx is not None:
                    lead_j['donors'][user_idx]['ref'] += data['total_donated']
                    lead_j['donors'][user_idx]['combined'] += data['total_donated']
            # check if user donating is already in leaderboard
            user2_idx = helpers.get_index(lead_j['donors'], 'user_id', data['user_id'])
            if user2_idx is not None:
                lead_j['donors'][user2_idx]['donated'] += data['total_donated']
                lead_j['donors'][user2_idx]['combined'] += data['total_donated']
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
                                         'people_ref': 0,
                                         'combined': data['total_donated']})
            try:
                upd_lead = helpers.generic_patch('/leaderboards/', lead_j, lead_j['etag'])
            except:
                update_leaderboard_post.delay(data)
                return
            if 'error' in upd_lead:
                update_leaderboard_post.delay(data)
                return
            return
    except:
        update_leaderboard_post.delay(data)
