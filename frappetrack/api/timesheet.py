import frappe
from frappe import _
import base64
from frappe.utils.file_manager import save_file

@frappe.whitelist(allow_guest=False)
def get_timesheet_by_task(task_id: str):
    """
    Fetch Draft Timesheets linked to a specific Task
    """
    try:
        user = frappe.session.user  

        timesheets = frappe.db.get_list(
            "Timesheet",
            fields=["name", "parent_project", "employee", "employee_name", "status"],
            filters={
                "task": task_id,
                "status": "Draft"
            }
        )

        if timesheets:
            return {
                "status": "success",
                "data": timesheets,
                "message": _("{0} draft timesheets found for task {1}.")
                .format(len(timesheets), task_id)
            }
        else:
            return {
                "status": "success",
                "data": [],
                "message": _("No draft timesheets found for this task.")
            }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Timesheet By Task API Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist(allow_guest=False)
def create_timesheet(timesheet_data):
    """
    Create Timesheet with Time Logs
    :param timesheet_data: JSON string or dict
    """

    try:
        user = frappe.session.user
        # If data comes as JSON string (from API call)
        if isinstance(timesheet_data, str):
            timesheet_data = frappe.parse_json(timesheet_data)

        # Create Timesheet document
        ts = frappe.new_doc("Timesheet")

        # ---- Parent Fields ----
        ts.title = timesheet_data.get("title")
        ts.naming_series = timesheet_data.get("naming_series", "TS-.YYYY.-")
        ts.company = timesheet_data.get("company")
        ts.employee = timesheet_data.get("employee")
        ts.employee_name = timesheet_data.get("employee_name")
        ts.parent_project = timesheet_data.get("parent_project")
        ts.start_date = timesheet_data.get("start_date")
        ts.end_date = timesheet_data.get("end_date")

        # ---- Child Table : time_logs ----
        for log in timesheet_data.get("time_logs", []):
            ts.append("time_logs", {
                "activity_type": log.get("activity_type"),
                "from_time": log.get("from_time"),
                "to_time": log.get("to_time"),
                "hours": log.get("hours"),
                "completed": log.get("completed"),
                "project": log.get("project"),
                "task": log.get("task"),
                "is_billable": log.get("is_billable", 0),
                "billing_hours": log.get("billing_hours", 0),
                "billing_rate": log.get("billing_rate", 0),
                "costing_rate": log.get("costing_rate", 0),
            })

        # Insert document
        ts.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "timesheet": ts.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Timesheet API Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(allow_guest=False)
def add_time_log(timesheet, time_log):
    """
    Append a new Time Log row to an existing Timesheet
    and set employee from the JSON payload
    """

    try:
        # Parse JSON if needed
        if isinstance(time_log, str):
            time_log = frappe.parse_json(time_log)

        # If employee is passed in JSON, use it
        employee = time_log.get("employee")
        if not employee:
            # Fallback: derive from session user (optional)
            employee = frappe.get_all(
                "Employee",
                filters={"user_id": frappe.session.user},
                limit=1,
                pluck="name"
            )
            employee = employee[0] if employee else None


        if not employee:
            frappe.throw("Employee must be specified or mapped to session user")

        # Get Timesheet
        ts = frappe.get_doc("Timesheet", timesheet)

        # Set employee
        ts.employee = employee

        # Set parent project
        ts.parent_project = time_log.get("project")
        # Append time log
        ts.append("time_logs", {
            "activity_type": time_log.get("activity_type"),
            "from_time": time_log.get("from_time"),
            "to_time": time_log.get("to_time"),
            "hours": time_log.get("hours"),
            "completed": time_log.get("completed"),
            "project": time_log.get("project"),
            "task": time_log.get("task"),
            "is_billable": time_log.get("is_billable", 0),
            "billing_hours": time_log.get("billing_hours", 0),
            "billing_rate": time_log.get("billing_rate", 0),
            "costing_rate": time_log.get("costing_rate", 0),
            "description": time_log.get("description")
        })

        ts.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "timesheet": ts.name,
            "employee": ts.employee,
            "total_hours": ts.total_hours
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Add Time Log Error")
        return {
            "status": "error",
            "message": str(e)
        }

@frappe.whitelist(allow_guest=True)
def upload_screenshot(file_name: str, file_data: str, timesheet_id: str):
    try:
        # Decode base64 data
        content = base64.b64decode(file_data)

        # Save file in File DocType & attach to Timesheet
        file_doc = save_file(
            fname=file_name,
            content=content,
            dt="Timesheet",
            dn=timesheet_id,
            is_private=0
        )

        return {
            "status": "success",
            "message": "Screenshot uploaded successfully",
            "file_name": file_doc.file_name,
            "file_url": file_doc.file_url,
            "file_id": file_doc.name
        }
    except Exception as e:
        frappe.log_error(
            title="Upload Screenshot Error",
            message=frappe.get_traceback()
        )
        return {
            "status": "error",
            "message": str(e)
        }