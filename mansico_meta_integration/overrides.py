import ast
import copy
import inspect
import json
import mimetypes
import types
from contextlib import contextmanager
from functools import lru_cache

import RestrictedPython.Guards
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.transformer import RestrictingNodeTransformer

import frappe
import frappe.exceptions
import frappe.integrations.utils
import frappe.utils
import frappe.utils.data
from frappe import _
from frappe.core.utils import html2text
from frappe.frappeclient import FrappeClient
from frappe.handler import execute_cmd
from frappe.model.delete_doc import delete_doc
from frappe.model.mapper import get_mapped_doc
from frappe.model.rename_doc import rename_doc
from frappe.modules import scrub
from frappe.utils.background_jobs import enqueue, get_jobs
from frappe.website.utils import get_next_link, get_toc
from frappe.www.printview import get_visible_columns



from frappe.utils.safe_exec import get_safe_globals, SERVER_SCRIPT_FILE_PREFIX, safe_exec_flags, patched_qb 

def safe_exec(
	script: str,
	_globals: dict | None = None,
	_locals: dict | None = None,
	*,
	restrict_commit_rollback: bool = False,
	script_filename: str | None = None,
):
    # always allow server scripts
	# if not is_safe_exec_enabled():

	# 	msg = _("Server Scripts are disabled. Please enable server scripts from bench configuration.")
	# 	docs_cta = _("Read the documentation to know more")
	# 	msg += f"<br><a href='https://frappeframework.com/docs/user/en/desk/scripting/server-script'>{docs_cta}</a>"
	# 	frappe.throw(msg, ServerScriptNotEnabled, title="Server Scripts Disabled")

	# build globals
	exec_globals = get_safe_globals()
	if _globals:
		exec_globals.update(_globals)

	if restrict_commit_rollback:
		# prevent user from using these in docevents
		exec_globals.frappe.db.pop("commit", None)
		exec_globals.frappe.db.pop("rollback", None)
		exec_globals.frappe.db.pop("add_index", None)

	filename = SERVER_SCRIPT_FILE_PREFIX
	if script_filename:
		filename += f": {frappe.scrub(script_filename)}"

	with safe_exec_flags(), patched_qb():
		# execute script compiled by RestrictedPython
		exec(
			script,
		)

	return exec_globals, _locals
from mansico_meta_integration.mansico_meta_integration.doctype.sync_new_add.meta_integraion_objects import UserData, CustomData, Payload
from mansico_meta_integration.mansico_meta_integration.doctype.sync_new_add.sync_new_add import FetchLeads
def validate_lead(doc, method=None):
    if not doc.is_new():
        
        import datetime
        import json
        now = datetime.datetime.now()
        unixtime = int(now.timestamp())
        if doc.custom_lead_json:
            old_doc = doc.get_doc_before_save()
            if old_doc.status != doc.status:
                lead = frappe.get_doc("Lead", doc.name)
                FetchLeads.create_lead_in_facebook(lead)
            