# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):

    _inherit = 'res.users'

    def get_allowed_project_ids(self):
        """
        This method returns the project ids that the user is allowed to view.
        """
        self.ensure_one()

        allowed_project_ids = self.env['project.project'].search([('team_id.member_ids', 'in', [self.id])])

        # Add logics here if still need to filter the projects based on privacy_visibility and follower ids


        return [('id', 'in', allowed_project_ids.ids)]