# -*- coding: utf-8 -*-

from giga_web import giga_web, helpers
from giga_web.models import Project

app = giga_web

@app.route('/homepage/stats/')
def hompage_stats(client_perma, campaign_perma, methods=['GET']):
	all_total_raised = Project.objects.sum('total_raised')
	all_avg = Project.objects.average('total_raised')
	all_projs = len(Projects.objects)
	data = {'data': {'status': 'OK', 'total_raised': all_total_raised,
					 'avg_raised': all_avg, 'total_projs': all_projs}}
	return json.dumps(data)