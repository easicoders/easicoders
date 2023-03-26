# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal


class EasiTimesheetCustomerPortal(TimesheetCustomerPortal):

    @http.route(['/my/timesheet/<model("account.analytic.line"):timesheet>/remove'], type='http', auth="public", website=True,
                methods=['POST'], csrf=False)
    def remove_timesheet(self, timesheet, **post):
        timesheet.unlink()
        return request.redirect('/my/timesheets')

    @http.route(['/my/timesheet/<model("account.analytic.line"):timesheet>/edit'], type='http', auth="public",
                website=True, methods=['POST'], csrf=False)
    def edit_timesheet(self, timesheet, **post):
        new_values = {}
        if post.get('date'):
            new_values.update({'date': post.get('date')})
        if post.get('name'):
            new_values.update({'name': post.get('name')})
        if post.get('unit_amount'):
            new_values.update({'unit_amount': float(post.get('unit_amount'))})

        if new_values:
            timesheet.write(new_values)
        return request.redirect('/my/timesheets')

    @http.route(['/my/timesheet/create'], type='http', auth="public",
                website=True, methods=['POST'], csrf=False)
    def create_timesheet(self, **post):
        new_values = {'project_id': int(post.get('project_id') or
                                        request.env['project.task'].browse(int(post.get('task_id'))).project_id.id),
                      'task_id': int(post.get('task_id'))}
        if post.get('c_date'):
            new_values.update({'date': post.get('c_date')})
        if post.get('c_name'):
            new_values.update({'name': post.get('c_name')})
        if post.get('c_unit_amount'):
            new_values.update({'unit_amount': float(post.get('c_unit_amount'))})

        if new_values:
            request.env['account.analytic.line'].create(new_values)
        return request.redirect('/my/timesheets')

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none',
                             **kw):
        res = super(EasiTimesheetCustomerPortal, self).portal_my_timesheets(page=page, sortby=sortby, filterby=filterby,
                                                                            search=search, search_in=search_in,
                                                                            groupby=groupby, **kw)

        partner_id = request.env.user.partner_id
        all_projects = []
        followed_projects = []
        followed_tasks = []
        projects = request.env['project.project'].sudo().search([])
        for project in projects:
            if partner_id in project.message_partner_ids:
                followed_projects.append(project)
        tasks = request.env['project.task'].sudo().search([])
        for task in tasks:
            if (partner_id in task.message_partner_ids or (followed_projects and task.project_id in followed_projects)
                    and task not in followed_tasks):
                followed_tasks.append(task)
                all_projects.append(task.project_id)

        res.qcontext.update({
            'all_projects': all_projects,
            'all_tasks': followed_tasks
        })

        return res
