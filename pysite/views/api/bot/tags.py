# coding=utf-8

from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin

GET_SCHEMA = Schema([
    {
        Optional("tag_name"): str
    }
])

POST_SCHEMA = Schema([
    {
        "tag_name": str,
        "tag_content": str
    }
])

DELETE_SCHEMA = Schema([
    {
        "tag_name": str
    }
])


class TagsView(APIView, DBMixin):
    path = "/tags"
    name = "api.bot.tags"
    table_name = "tags"
    table_primary_key = "tag_name"

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        """
        Fetches tags from the database.

        - If tag_name is provided, it fetches
        that specific tag.

        - If tag_category is provided, it fetches
        all tags in that category.

        - If nothing is provided, it will
        fetch a list of all tag_names.

        Data must be provided as params.
        API key must be provided as header.
        """

        tag_name = None

        if params:
            tag_name = params[0].get("tag_name")

        if tag_name:
            data = self.db.get(self.table_name, tag_name) or {}
        else:
            data = self.db.pluck(self.table_name, "tag_name") or []

        return jsonify(data)

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, json_data):
        """
        If the tag_name doesn't exist, this
        saves a new tag in the database.

        If the tag_name already exists,
        this will edit the existing tag.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        json_data = json_data[0]

        tag_name = json_data.get("tag_name")
        tag_content = json_data.get("tag_content")

        self.db.insert(
            self.table_name,
            {
                "tag_name": tag_name,
                "tag_content": tag_content
            },
            conflict="update"  # If it exists, update it.
        )

        return jsonify({"success": True})

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, data):
        """
        Deletes a tag from the database.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        json = data[0]
        tag_name = json.get("tag_name")
        tag_exists = self.db.get(self.table_name, tag_name)

        if tag_exists:
            self.db.delete(
                self.table_name,
                tag_name
            )
            return jsonify({"success": True})

        return jsonify({"success": False})
