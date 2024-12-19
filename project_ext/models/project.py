# -*- coding: utf-8 -*-

from odoo import models, fields

class Project(models.Model):
    """
    This class extends the 'project.project' model to add the 'team_id' field and added functionality to the project.
    """

    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string='Assigned Team', copy=False)