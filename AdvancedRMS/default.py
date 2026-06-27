from  Database import model
from Hashing.hashing import Hash


default_risks = [
    {
        "risk_title": "Admin Panel Unauthorized Access Attempt",
        "risk_description": "Multiple failed login attempts detected on admin dashboard.",
        "risk_priority": "High",
        "risk_status": "Open",
        "risk_type": "Security",
        "risk_category": "Authentication",
        "assigned_to": 1,   # Employee
        "created_by": 5,    # Admin
        "risk_allocation": 2,  # Manager (Mohit Solanki)
        "due_date": "2026-06-10"
    },
    {
        "risk_title": "Backup System Failure Risk",
        "risk_description": "Automated database backup failed due to storage limits.",
        "risk_priority": "Critical",
        "risk_status": "In Progress",
        "risk_type": "Infrastructure",
        "risk_category": "Database",
        "assigned_to": 7,   # Piyush Chauhan (Employee)
        "created_by": 6,    # Admin (Sunil)
        "risk_allocation": 3,  # Manager (Sanya)
        "due_date": "2026-06-05"
    },
    {
        "risk_title": "Delayed Feature Deployment",
        "risk_description": "Production release delayed due to unresolved merge conflicts.",
        "risk_priority": "Medium",
        "risk_status": "Open",
        "risk_type": "Operational",
        "risk_category": "CI/CD",
        "assigned_to": 8,   # Mohit Malviya (Employee)
        "created_by": 5,
        "risk_allocation": 2,
        "due_date": "2026-06-15"
    },
    {
        "risk_title": "Customer Data Exposure Vulnerability",
        "risk_description": "Potential leakage of sensitive user data via API endpoint.",
        "risk_priority": "Critical",
        "risk_status": "Mitigated",
        "risk_type": "Compliance",
        "risk_category": "Data Security",
        "assigned_to": 3,   # Sanya (Employee role ignored logically, but ok for seed)
        "created_by": 6,
        "risk_allocation": 3,
        "due_date": "2026-06-01"
    },
    {
        "risk_title": "Server Overload During Peak Traffic",
        "risk_description": "High CPU usage detected during peak hours causing latency.",
        "risk_priority": "High",
        "risk_status": "Monitoring",
        "risk_type": "Infrastructure",
        "risk_category": "Scalability",
        "assigned_to": 4,
        "created_by": 2,
        "risk_allocation": 2,
        "due_date": "2026-06-20"
    },
    {
        "risk_title": "Third-Party API Downtime",
        "risk_description": "External payment API intermittently unavailable.",
        "risk_priority": "Medium",
        "risk_status": "Open",
        "risk_type": "External",
        "risk_category": "Dependency",
        "assigned_to": 7,
        "created_by": 1,
        "risk_allocation": 3,
        "due_date": "2026-06-25"
    },
    {
        "risk_title": "Phishing Attack on Employees",
        "risk_description": "Suspicious emails detected targeting staff credentials.",
        "risk_priority": "High",
        "risk_status": "In Progress",
        "risk_type": "Security",
        "risk_category": "Social Engineering",
        "assigned_to": 8,
        "created_by": 5,
        "risk_allocation": 2,
        "due_date": "2026-06-08"
    },
    {
        "risk_title": "Payment Gateway Integration Failure",
        "risk_description": "Transaction failures occurring in checkout process.",
        "risk_priority": "High",
        "risk_status": "Open",
        "risk_type": "Operational",
        "risk_category": "Payments",
        "assigned_to": 1,
        "created_by": 6,
        "risk_allocation": 3,
        "due_date": "2026-06-18"
    }
]

default_users = [
    {
        "user_name": "Dipesh Soni",
        "user_role": "Employee",
        "user_email": "dipesh@gmail.com",
        "user_password": "dipesh123"
    },
    {
        "user_name": "Mohit Solanki",
        "user_role": "Manager",
        "user_email": "mohit@gmail.com",
        "user_password": "mohit123"
    },
    {
        "user_name": "Sanya Singh Deora",
        "user_role": "Manager",
        "user_email": "sanya@gmail.com",
        "user_password": "sanya"
    },
    {
        "user_name": "Priyanjali Bhati",
        "user_role": "Employee",
        "user_email": "priyanjali@gmail.com",
        "user_password": "priyanjali123"
    },
    {
        "user_name": "Harshita Sharma",
        "user_role": "Admin",
        "user_email": "Harshita@gmail.com",
        "user_password": "harshita123"
    },
    {
        "user_name": "Sunil Choudhary",
        "user_role": "Admin",
        "user_email": "sunil@gmail.com",
        "user_password": "sunil123"
    },
    {
        "user_name": "Piyush Chauhan",
        "user_role": "Employee",
        "user_email": "piyush@gmail.com",
        "user_password": "piyush123"
    },
    {
        "user_name": "Mohit Malviya",
        "user_role": "Employee",
        "user_email": "mohitmalviya@gmail.com",
        "user_password": "mohit123"
    }
]

def addALL(db):
    for user in default_users:
        new_user = model.User(
            user_name = user["user_name"],
            user_role = user["user_role"],
            user_email = user["user_email"],
            user_password = Hash.bcryptPassword(user["user_password"])
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    for risk in default_risks:
        new_risk = model.Risk(
            risk_title= risk["risk_title"],
            risk_description= risk["risk_description"],
            risk_priority= risk["risk_priority"],
            risk_status= risk['risk_status'],
            risk_type= risk["risk_type"],
            risk_category= risk['risk_category'],
            created_by= risk['created_by'],
            risk_allocation= risk['risk_allocation'],
            assigned_to= risk['assigned_to'],
            due_date = risk['due_date']
        )

        db.add(new_risk)
        db.commit()
        db.refresh(new_risk)
    
    return "Default values added successfully. Now you can login and use this System."