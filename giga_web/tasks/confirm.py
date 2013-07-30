# -*- coding: utf-8 -*-
from giga_web import celery, crud_url, helpers, celery_logger
from wsgiref.handlers import format_date_time
from datetime import datetime, timedelta
from time import mktime
from celery.utils.log import get_task_logger
import requests

logger = celery_logger

@celery.task
def confirm_donation(data):
    logger.info('task confirm_donation called. args: %s', str(data))
    for proj in data['proj_list']:
        up = update_project_post(proj)
        if 'error' in up:
            return up
    # update campaign
    camp, leader_id = update_campaign_post(data)
    if 'error' in camp:
        return camp
    # update leaderboard
    lead = update_leaderboard_post(data, leader_id)
    if 'error' in lead:
        return lead


@celery.task
def update_project_post(data):
    logger.info('task update_project_post. args: %s', str(data))
    p = helpers.generic_get('/projects/', data['proj_id'])
    pj = p.json()
    pj['raised'] += data['donated']
    if (pj['raised'] >= pj['goal']) and ('completed' not in pj):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        pj['completed'] = format_date_time(stamp)
    upd_p = helpers.generic_patch('/projects/', pj, pj['etag'])
    return upd_p


@celery.task
def update_campaign_post(data):
    logger.info('task update_campaign_post called. args: %s', str(data))
    camp = helpers.generic_get('/campaigns/', data['camp_id'])
    camp_j = camp.json()
    lead_id = camp_j['leaderboard_id']
    camp_j['total_raised'] += data['total_donated']
    for projs in data['proj_list']:
        activelist_proj = helpers.get_index(camp_j['active_list'], 'p_id', projs['proj_id'])
        if activelist_proj is not None:
            camp_j['active_list'][activelist_proj]['raised'] += projs['donated']
    upd_camp = helpers.generic_patch('/campaigns/', camp_j, camp_j['etag'])
    return upd_camp, lead_id


@celery.task
def update_leaderboard_post(data, lead_id):
    logger.info('task update_leaderboard_post called. args: %s %s', str(data), lead_id)
    lead = helpers.generic_get('/leaderboards/', lead_id)
    lead_j = lead.json()
    lead_j['raised'] += data['total_donated']
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
                                 'combined': data['total_donated']})

    upd_lead = helpers.generic_patch('/leaderboards/', lead_j, lead_j['etag'])
    return upd_lead
