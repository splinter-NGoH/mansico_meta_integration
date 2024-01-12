# Copyright (c) 2023, mansy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
@frappe.whitelist()
def get_credentials():
    return frappe.get_doc("Meta Facebook Settings")

import requests
import json
class Request:
    def __init__(self, url, version, page_id, f_payload=None, params=None):
        self.url = url
        self.version = 'v' + str(version)
        self.page_id = page_id
        self.f_payload = f_payload
        self.params = params
    @property
    def get_url(self):
        return self.url + "/" + self.version + "/" + self.page_id

class RequestPageAccessToken():
    def __init__(self, request):
        self.request = request

    def get_page_access_token(self):
        response = requests.get(self.request.get_url, params=self.request.params, json=self.request.params) 
        
        if frappe._dict(response.json()).get("error"):
            _error_message = ""
            _error_message += "url" + " : " + str(self.request.get_url) + "<br>"
            _error_message += "params" + " : " + str(self.request.params) + "<br>"
            _error_message += "<br>"
            for key in frappe._dict(response.json()).get("error").keys():
                _error_message += key + " : " + str(frappe._dict(response.json()).get("error").get(key)) + "<br>"
            frappe.throw(_error_message, title="Error")
        else:
            self.page_access_token = frappe._dict(response.json()).get("access_token")
            return self.page_access_token

class RequestLeadGenFroms():
    def __init__(self, request):
        self.request = request

    def get_lead_forms(self):
        response = requests.get(self.request.get_url, params=self.request.params, json=self.request.params) 
        if frappe._dict(response.json()).get("error"):
            _error_message = ""
            _error_message += "url" + " : " + str(self.request.get_url) + "<br>"
            _error_message += "params" + " : " + str(self.request.params) + "<br>"
            _error_message += "<br>"
            for key in frappe._dict(response.json()).get("error").keys():
                _error_message += key + " : " + str(frappe._dict(response.json()).get("error").get(key)) + "<br>"
            frappe.throw(_error_message, title="Error")
        else:
            self.lead_forms = frappe._dict(response.json())
            return self.lead_forms

class AppendForms():
    def __init__(self, lead_forms, doc):
        self.lead_forms = lead_forms
        self.doc = doc
    def append_forms(self):
        if self.doc.force_fetch:
            self.doc.set("table_hsya", [])
            for lead_form in self.lead_forms.get("data"):
                self.doc.append("table_hsya", {
                    "form_id": lead_form.get("id"),
                    "form_name": lead_form.get("name"),
                    "created_time": lead_form.get("created_time"),
                    "leads_count": lead_form.get("leads_count"),
                    "page": lead_form.get("page"),
                    "questions": frappe._dict({"questions":lead_form.get("questions")}),
                })
class ServerScript():
    def __init__(self, doc):
        self.doc = doc
    
    def create_server_script(self):
        self.server_script = frappe.get_doc({
            "doctype": "Server Script",
            "name": str(str(self.doc.name).replace("-", "_")).lower(),
            "script_type": "Scheduler Event",
            "event_frequency": self.doc.event_frequency,
            "module": "Meta Facebook Leads",
            "script": self.generate_script()
        })
    def generate_script(self):
        _script = ""
        import os
        _script += """from mansico_meta_integration.mansico_meta_integration.doctype.sync_new_add.sync_new_add import FetchLeads\n"""
        _script += """import frappe\n"""
        _script += """fetch = FetchLeads("{0}")\n""".format(str(str(self.doc.name).replace("-", "_")).lower())
        _script += """fetch.fetch_leads()\n"""
        return _script
    


class RequestSendLead():
    def __init__(self, request):
        self.request = request
    def send_lead(self):
        response = requests.post(self.request.get_url, params=self.request.params, json=self.request.f_payload) 
        if frappe._dict(response.json()).get("error"):
            error_message = ""
            error_message += "url" + " : " + str(self.request.get_url) + "<br>"
            error_message += "params" + " : " + str(self.request.params) + "<br>"
            error_message += "<br>"
            for key in json.dumps(response.json()).get("error").keys():
                error_message += key + " : " + str(json.dumps(response.json()).get("error").get(key)) + "<br>"
            frappe.throw(error_message, title="Error")
        else:
            return json.dumps(response.json())


class FetchLeads():
    def __init__(self, name):
        self.name = name

    @property
    def get_form_ids(self):
        form_ids = []
        for form in self.doc.table_hsya:
            form_ids.append(form.form_id)
        return form_ids
    @frappe.whitelist()
    def fetch_leads(self):
        self.doc = frappe.get_doc("Sync New Add", self.name.upper().replace("_","-"))
        self.form_ids = self.get_form_ids
        for form_id in self.form_ids:
            defaults = get_credentials()
            #  init Request
            request = Request(defaults.api_url, defaults.graph_api_version,
            self.doc.page_id, None, params={"fields": "access_token", "transport": "cors",
                    "access_token": defaults.access_token})
            # init RequestPageAccessToken
            request_page_access_token = RequestPageAccessToken(request)
            # get page access token
            request_page_access_token.get_page_access_token()
            # init Request
            request = Request(defaults.api_url, defaults.graph_api_version,
            form_id + "/leads", None, params={"access_token": request_page_access_token.page_access_token,
            "fields": "ad_id,ad_name,adset_id,adset_name,\
                campaign_id,campaign_name,created_time,custom_disclaimer_responses,\
                    field_data,form_id,id,home_listing,is_organic,partner_name,\
                        platform,post,retailer_item_id,vehicle"
                                              })
            # init RequestLeadGenFroms
            request_lead_gen_forms = RequestLeadGenFroms(request)
            # get lead forms
            request_lead_gen_forms.get_lead_forms()
            if request_lead_gen_forms.lead_forms.get("data"):
                # use self.lead_forms
                # fetch all leads then create them using create_lead
                # filter leads by created_time and id to avoid duplication
                self.paginate_lead_forms(request_lead_gen_forms.lead_forms)

                
            
    def paginate_lead_forms(self, lead_forms):
        if lead_forms.paging.get("next"):
            self.create_lead(lead_forms.get("data"))
            next_page = lead_forms.paging.get("next")
            response = requests.get(next_page)
            lead_forms = frappe._dict(response.json())
            return self.paginate_lead_forms(lead_forms)
        else:
            if lead_forms:
                self.create_lead(lead_forms.get("data"))
            return lead_forms
    def create_lead(self, leads):
        import traceback
        for lead in leads:
            if not frappe.db.exists("Lead", {"email_id": lead.get("field_data")[1].get("values")[0]}):
                new_lead = frappe.get_doc({
                    "doctype": "Lead",
                    "first_name": lead.get("field_data")[0].get("values")[0],
                    "email_id": lead.get("field_data")[1].get("values")[0],
                    "mobile_no": lead.get("field_data")[2].get("values")[0],
                    "job_title" : lead.get("field_data")[3].get("values")[0],
                    "company_name": lead.get("field_data")[4].get("values")[0],
                    "custom_lead_json" : frappe._dict(lead),
                })
                try:
                    new_lead.insert(ignore_permissions=True)
                    # create lead in facebook
                    FetchLeads.create_lead_in_facebook(new_lead)
                except Exception as e:

                    frappe.log_error( "error",str(e))
                    frappe.log_error( "traceback", str(traceback.format_exc()))
                    frappe.log_error( "new_lead", str(new_lead))
    
    @staticmethod
    def create_lead_in_facebook(lead):
        import datetime
        import json
        from mansico_meta_integration.mansico_meta_integration.doctype.sync_new_add.meta_integraion_objects import UserData, CustomData, Payload
        import ast
        now = datetime.datetime.now()
        unixtime = int(now.timestamp())
        if lead.custom_lead_json:
            payload = Payload(
                event_name=lead.status,
                event_time=unixtime ,
                action_source="system_generated",
                user_data=UserData(lead.custom_lead_json.get("id") if not isinstance(lead.custom_lead_json, str) else json.loads(lead.custom_lead_json).get("id")).__dict__,
                custom_data=CustomData("crm", "ERP next").__dict__
            )    
            f_payload = frappe._dict({"data": [payload.__dict__]})
            # send request to facebook
            defaults = get_credentials()
            #  init Request
            request = Request(defaults.api_url, defaults.graph_api_version,
            defaults.pixel_id + "/events", f_payload, params={"access_token": defaults.pixel_access_token})
            # init RequestSendLead
            request_send_lead = RequestSendLead(request)
            # send lead
            response = request_send_lead.send_lead()
            #  insert to note with
            note = frappe.get_doc({
                "doctype": "Note",
                "title": "Lead Created in Facebook Successfully",
                "public": 1,
                "content": "Lead Created in Facebook Successfully <br> Response: " 
                + str(response) + "<br> Payload: " + str(f_payload),
                "custom_reference_name": lead.name,
            })
            note.insert(ignore_permissions=True)

class SyncNewAdd(Document):
    def validate(self):
        defaults = get_credentials()
        #  init Request
        request = Request(defaults.api_url, defaults.graph_api_version,
         self.page_id, None, params={"fields": "access_token", "transport": "cors",
          "access_token": defaults.access_token})
        # init RequestPageAccessToken
        request_page_access_token = RequestPageAccessToken(request)
        # get page access token
        request_page_access_token.get_page_access_token()
        # init Request
        request = Request(defaults.api_url, defaults.graph_api_version,
         self.page_id + f"/leadgen_forms", None, params={"access_token": request_page_access_token.page_access_token,
         "fields": "name,id,created_time,leads_count,page,page_id,\
         questions,leads {\
            ad_id,campaign_id,adset_id,campaign_name,ad_name,form_id,id,\
                adset_name,created_time\
                    }"})
        # init RequestLeadGenFroms
        request_lead_gen_forms = RequestLeadGenFroms(request)
        # get lead forms
        request_lead_gen_forms.get_lead_forms()
        # init AppendForms
        append_forms = AppendForms(request_lead_gen_forms.lead_forms, self)
        # append forms
        append_forms.append_forms()

    def on_submit(self):
        # create Server Script
        server_script = ServerScript(self)
        server_script.create_server_script()
        server_script.server_script.insert(ignore_permissions=True)
        # frappe.db.commit()
        frappe.msgprint("Server Script Created Successfully")

    def on_cancel(self):
        # delete Server Script
        frappe.delete_doc("Server Script", str(self.name).lower().replace("-","_"), ignore_permissions=True)
        frappe.msgprint("Server Script Deleted Successfully")