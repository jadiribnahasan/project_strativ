# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectTeam(models.Model):

    _name = 'project.team'
    _description = 'Project Team'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False, index=True, default='New Team')
    description = fields.Text(string='Description', copy=False)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', copy=False)
    member_ids = fields.Many2many('res.users', string='Members', copy=True, domain=[('share', '=', False)]) #Copy true will help to copy the members when we duplicate the team

    project_ids = fields.One2many('project.project', 'team_id', string='Projects', copy=False)


