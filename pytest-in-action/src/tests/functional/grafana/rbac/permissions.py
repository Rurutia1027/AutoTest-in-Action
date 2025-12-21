RBAC_MATRIX = {
    "Admin": {
        "dashboard": {"create", "read", "update", "delete"},
        "folder": {"create", "read", "update", "delete"},
        "datasource": {"create", "read", "update", "delete"},
    },
    "Editor": {
        "dashboard": {"create", "read", "update", "delete"},
        "folder": {"create", "read", "update"},
        "datasource": {"read"},
    },
    "Viewer": {
        "dashboard": {"read"},
        "folder": {"read"},
        "datasource": {"read"},
    },
}