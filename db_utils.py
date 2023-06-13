from pymongo import MongoClient, UpdateMany
import functools
from inspect import getmembers, ismethod

from Config import GLOBAL_CONFIG

client = MongoClient(GLOBAL_CONFIG.MONGO_URL)
my_db = client[GLOBAL_CONFIG.DB_NAME]
my_collection = my_db[GLOBAL_CONFIG.COLLECTION_NAME]


def persist_user(user):
    if not GLOBAL_CONFIG.DB_ENABLED:
        return
    existing_user = my_collection.find_one({"username": user.username})

    if existing_user is None:
        my_collection.insert_one(user.to_json())
        print("User added successfully.")
    else:
        my_collection.update_one(
            {"username": user.username},
            {"$set": user.to_json()}
        )
        print("User updated successfully.")


def update_project_methods(cls):
    if not GLOBAL_CONFIG.DB_ENABLED:
        return cls

    methods = [
        method_name
        for method_name, val in getmembers(cls)
        if method_name.startswith("set") or method_name.startswith("add") or method_name.startswith("edit") or method_name.startswith("remove")
    ]

    # Apply the update_project decorator to each method
    for method_name in methods:
        original_method = getattr(cls, method_name)
        decorated_method = decorator_project_update(original_method)
        setattr(cls, method_name, decorated_method)

    return cls


def decorator_project_update(func):
    def wrapper_update(*args, **kwargs):
        print("updating project in db")
        val = func(*args, **kwargs)
        self = args[0]
        # Create a list to store update operations
        update_operations = []

        # Iterate over the users and update the project based on its ID
        users = my_collection.find({})
        for user in users:
            project_id = str(self.id)

            # Check if the user has the project in their projects dictionary
            if project_id in user['projects']:
                # Update the project in the user's projects dictionary
                user['projects'][project_id] = self.to_json()

                # Create the update operation
                update_operation = UpdateMany(
                    {"_id": user["_id"]},
                    {"$set": {"projects": user['projects']}}
                )

                update_operations.append(update_operation)

        # Perform the bulk update
        if update_operations:
            my_collection.bulk_write(update_operations)

        return val

    return wrapper_update


