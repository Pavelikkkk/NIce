from app import ma
from app.models import World, Player, Privilege, Mod, ModPack, ModPackAssociation

class WorldSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = World
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    mod_pack_id = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()
    mod_pack = ma.Nested('ModPackSchema', dump_only=True)
    player_count = ma.Integer(dump_only=True)

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    world_id = ma.auto_field()
    email = ma.auto_field()
    join_date = ma.auto_field()
    world = ma.Nested('WorldSchema', dump_only=True)

class PrivilegeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Privilege
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    player_id = ma.auto_field()
    description = ma.auto_field()
    player = ma.Nested('PlayerSchema', dump_only=True)

class ModSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mod
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    version = ma.auto_field()

class ModPackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ModPack
        load_instance = True
        include_fk = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    mods = ma.Nested('ModSchema', many=True)

class ModPackAssociationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ModPackAssociation
        load_instance = True
        include_fk = True

    mod_pack_id = ma.auto_field()
    mod_id = ma.auto_field()