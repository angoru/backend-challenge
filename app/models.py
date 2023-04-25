from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise


class Channels(models.Model):
    """
    The Channel model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False)
    plugin_class = fields.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


Channel_Pydantic = pydantic_model_creator(Channels, name="Channel")
ChannelIn_Pydantic = pydantic_model_creator(
    Channels, name="ChannelIn", exclude_readonly=True
)


class Topics(models.Model):
    """
    The Topic model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=False)
    channel = fields.ForeignKeyField("models.Channels", related_name="topics")

    def __str__(self):
        return self.name


Tortoise.init_models(["app.models"], "models")
Topic_Pydantic = pydantic_model_creator(Topics, name="Topic")
TopicIn_Pydantic = pydantic_model_creator(Topics, name="TopicIn", exclude_readonly=True)
