from collections import defaultdict
import peewee

db = peewee.SqliteDatabase("todo_app.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Card(BaseModel):
    id = peewee.CharField(primary_key=True, unique=True)
    name = peewee.CharField()

    @staticmethod
    def get_all():
        """
        {
            <card_id> :{
                "name" : string,
                "items" : [
                    {
                        "id" : int,
                        "name" : string,
                        "completed" " boolean
                    }
                ]
            }
        }
        """
        cards = Card.select(
            Card.id.alias('card_id'), Card.name.alias('card_name')
        ).dicts()
        items = Item.select(
            Card.id.alias('card_id'), Item.id, Item.name, Item.completed
        ).join(Card).dicts()
        ret = defaultdict(dict)
        for card in cards:
            card_id = card['card_id']
            ret[card_id]['name'] = card['card_name']
            ret[card_id]['items'] = []
        for item in items:
            if "id" in item:
                ret[item['card_id']]['items'].append(
                    {
                        "id": item['id'],
                        "name": item['name'],
                        "completed": item['completed']
                    }
                )
                print(ret)
        return ret

class Item(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField()
    completed = peewee.BooleanField(default=False)
    card = peewee.ForeignKeyField(Card, backref='items')