# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields

class Project(models.Model):
    """
    This class extends the 'project.project' model to add the 'team_id' field and added functionality to the project.
    """

    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Assigned Team', copy=False)

    def get_projects(self, option):
        """
        This method returns all the top projects.
        """
        all_projects = self.env['project.project'].sudo().search([]) #remove sudo if you want to use the current user's access rights

        total_task = []
        project_name = []
        tasks = []
        assignees = []

        if option == 'all':
            for project in all_projects:
                total_task.append(len(project.tasks))
                project_name.append(project.name)
                tasks += [{'name': task.name, 'project': task.project_id.name, 'create_date': task.create_date, 'due_date': task.date_deadline, 'assignee': ', '.join(task.user_ids.mapped('name'))} for task in project.tasks]
                assignees += [assignee for assignee in list(project.tasks.mapped('user_ids'))]

        elif option == 'this_week':
            for project in all_projects:
                this_week_tasks = project.tasks.filtered(
                    lambda task: task.create_date >= fields.Datetime.now() - timedelta(days=7))
                total_task.append(len(this_week_tasks))
                project_name.append(project.name)
                tasks += [{'name': task.name, 'project': task.project_id.name, 'create_date': task.create_date, 'due_date': task.date_deadline, 'assignee': ', '.join(task.user_ids.mapped('name'))} for task in this_week_tasks]
                assignees += [assignee for assignee in list(this_week_tasks.mapped('user_ids'))]

        elif option == 'last_week':
            for project in all_projects:
                last_week_tasks = project.tasks.filtered(
                    lambda task: task.create_date >= fields.Datetime.now() - timedelta(days=14) and task.create_date < fields.Datetime.now() - timedelta(days=7))
                total_task.append(len(last_week_tasks))
                project_name.append(project.name)
                tasks += [{'name': task.name, 'project': task.project_id.name, 'create_date': task.create_date, 'due_date': task.date_deadline, 'assignee': ', '.join(task.user_ids.mapped('name'))} for task in last_week_tasks]
                assignees += [assignee for assignee in list(last_week_tasks.mapped('user_ids'))]

        elif option == 'this_month':
            for project in all_projects:
                this_month_tasks = project.tasks.filtered(
                    lambda task: task.create_date >= fields.Datetime.now() - timedelta(days=30))
                total_task.append(len(this_month_tasks))
                project_name.append(project.name)
                tasks += [{'name': task.name, 'project': task.project_id.name, 'create_date': task.create_date, 'due_date': task.date_deadline, 'assignee': ', '.join(task.user_ids.mapped('name'))} for task in this_month_tasks]
                assignees += [assignee for assignee in list(this_month_tasks.mapped('user_ids'))]

        elif option == 'last_month':
            for project in all_projects:
                last_month_tasks = project.tasks.filtered(
                    lambda task: task.create_date >= fields.Datetime.now() - timedelta(days=60) and task.create_date < fields.Datetime.now() - timedelta(days=30))
                total_task.append(len(last_month_tasks))
                project_name.append(project.name)
                tasks += [{'name': task.name, 'project': task.project_id.name, 'create_date': task.create_date, 'due_date': task.date_deadline, 'assignee': ', '.join(task.user_ids.mapped('name'))} for task in last_month_tasks]
                assignees += [assignee for assignee in list(last_month_tasks.mapped('user_ids'))]

        value = {'projects': project_name, 'count': total_task, 'tasks': tasks, 'assignees': [{'id': assignee.id, 'name': assignee.name} for assignee in list(set(assignees))]}
        return value


