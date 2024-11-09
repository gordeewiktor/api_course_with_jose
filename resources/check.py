from flask import jsonify
from flask_smorest import Blueprint
from sqlalchemy import inspect
from db import db

blp = Blueprint("DatabaseCheck", __name__, description="Database verification operations")

@blp.route("/check-column")
def check_column():
    inspector = inspect(db.engine)
    columns = inspector.get_columns("items_tags")
    column_names = [column['name'] for column in columns]
    
    # Check if 'item_id' exists in the columns
    if 'item_id' in column_names:
        return jsonify({"exists": True, "columns": column_names}), 200
    else:
        return jsonify({"exists": False, "columns": column_names}), 404