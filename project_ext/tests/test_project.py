# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestProject(TransactionCase):

    def setUp(self):
        super(TestProject, self).setUp()
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.user_model = self.env['res.users']

        # Create a test user
        self.user = self.user_model.create({
            'name': 'Test User',
            'login': 'test_user',
        })

        # Create a test project
        self.project = self.project_model.create({
            'name': 'Test Project',
        })

        # Create test tasks
        self.task1 = self.task_model.create({
            'name': 'Task 1',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user.id])],
        })
        self.task2 = self.task_model.create({
            'name': 'Task 2',
            'project_id': self.project.id,
            'user_ids': [(6, 0, [self.user.id])],
        })

    def test_get_projects_all(self):
        result = self.project.get_projects('all')
        self.assertEqual(result['projects'], ['Test Project'])
        self.assertEqual(result['count'], [2])
        self.assertEqual(len(result['tasks']), 2)
        self.assertEqual(len(result['assignees']), 1)

    def test_get_projects_this_week(self):
        result = self.project.get_projects('this_week')
        self.assertEqual(result['projects'], ['Test Project'])
        self.assertEqual(result['count'], [2])
        self.assertEqual(len(result['tasks']), 2)
        self.assertEqual(len(result['assignees']), 1)

    def test_get_projects_last_week(self):
        result = self.project.get_projects('last_week')
        self.assertEqual(result['projects'], ['Test Project'])
        self.assertEqual(result['count'], [0])
        self.assertEqual(len(result['tasks']), 0)
        self.assertEqual(len(result['assignees']), 0)

    def test_get_projects_this_month(self):
        result = self.project.get_projects('this_month')
        self.assertEqual(result['projects'], ['Test Project'])
        self.assertEqual(result['count'], [2])
        self.assertEqual(len(result['tasks']), 2)
        self.assertEqual(len(result['assignees']), 1)

    def test_get_projects_last_month(self):
        result = self.project.get_projects('last_month')
        self.assertEqual(result['projects'], ['Test Project'])
        self.assertEqual(result['count'], [0])
        self.assertEqual(len(result['tasks']), 0)
        self.assertEqual(len(result['assignees']), 0)