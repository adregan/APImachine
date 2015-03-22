from marshmallow import Schema, fields

""" Define your collections' schemas here for validation and marshalling
"""

class TestSchema(Schema):
    id = fields.String()
    title = fields.String(default="Untitled")
    type = fields.Select(
        choices=["fruit", "vegetable", "meat"],
        default="fruit"
    )
    updateddate = fields.LocalDateTime()
