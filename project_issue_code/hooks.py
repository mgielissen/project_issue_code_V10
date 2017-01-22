# -*- coding: utf-8 -*-
# © 2016 Michael Viriyananda
# 2017 upgraded it to odoo 10, and add some sql safty guard command, by stella.fredo@gmail.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID
from odoo import api

def pre_init_hook(cr):
    create_code_equal_to_id(cr)

def post_init_hook(cr,registry):
    assign_old_sequences(cr, registry)  

def create_code_equal_to_id(cr):
        """
        With this pre-init-hook we want to avoid error when creating the UNIQUE
        code constraint when the module is installed and before the post-init-hook
        is launched.
        """
        cr.execute('ALTER TABLE project_issue drop column if exists issue_code; '
                   'ALTER TABLE project_issue ADD COLUMN issue_code character varying;')
        cr.execute('UPDATE project_issue SET issue_code = id;')

def assign_old_sequences(cr, registry):
        """
        This post-init-hook will update all existing issue assigning them the
        corresponding sequence code.
        """
        issue_obj = registry['project.issue']
        issue_ids = issue_obj.search(cr, SUPERUSER_ID, [], order="id")
        for issue_id in issue_ids:
            cr.execute('UPDATE project_issue '
                   'SET issue_code = \'%s\' '
                   'WHERE id = %d;' %
                   (self.env['ir.sequence'].next_by_code('project.issue'),
                    issue_id))
