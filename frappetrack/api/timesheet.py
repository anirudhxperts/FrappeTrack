import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_timesheet(timesheet_data):
    """
    Create Timesheet with Time Logs
    :param timesheet_data: JSON string or dict
    """

    try:
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


@frappe.whitelist(allow_guest=True)
def add_time_log(timesheet, time_log):
    """
    Append a new Time Log row to an existing Timesheet
    """

    try:
        # Parse JSON if needed
        if isinstance(time_log, str):
            time_log = frappe.parse_json(time_log)

        ts = frappe.get_doc("Timesheet", timesheet)

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
        })

        ts.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "timesheet": ts.name,
            "total_hours": ts.total_hours
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Add Time Log Error")
        return {
            "status": "error",
            "message": str(e)
        }
