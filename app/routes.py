from flask import Blueprint, request, jsonify
from app import db
from app.models import World, Player, Privilege, ModPackAssociation, ModPack, Mod
from app.schemas import WorldSchema, PlayerSchema, PrivilegeSchema, ModSchema, ModPackSchema, ModPackAssociationSchema
from app.auth import auth

bp = Blueprint('api', __name__)

world_schema = WorldSchema()
worlds_schema = WorldSchema(many=True)

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

privilege_schema = PrivilegeSchema()
privileges_schema = PrivilegeSchema(many=True)
mod_schema = ModSchema()
mods_schema = ModSchema(many=True)

mod_pack_schema = ModPackSchema()
mod_packs_schema = ModPackSchema(many=True)

mod_pack_association_schema = ModPackAssociationSchema()
mod_pack_associations_schema = ModPackAssociationSchema(many=True)

@bp.route('/mods', methods=['GET'])
@auth.login_required
def get_mods():
    mods = Mod.query.all()
    return jsonify(mods_schema.dump(mods))

@bp.route('/mods', methods=['POST'])
@auth.login_required
def create_mod():
    data = request.json
    new_mod = Mod(name=data['name'], version=data['version'])
    db.session.add(new_mod)
    db.session.commit()
    return jsonify(mod_schema.dump(new_mod)), 201

@bp.route('/mods/<int:mod_id>', methods=['PUT'])
@auth.login_required
def update_mod(mod_id):
    data = request.json
    mod = Mod.query.get_or_404(mod_id)
    if 'name' in data:
        mod.name = data['name']
    if 'version' in data:
        mod.version = data['version']
    db.session.commit()
    return jsonify(mod_schema.dump(mod))

@bp.route('/mods/<int:mod_id>', methods=['DELETE'])
@auth.login_required
def delete_mod(mod_id):
    mod = Mod.query.get_or_404(mod_id)
    db.session.delete(mod)
    db.session.commit()
    return '', 204

@bp.route('/mod-packs', methods=['GET'])
@auth.login_required
def get_mod_packs():
    mod_packs = ModPack.query.all()
    return jsonify(mod_packs_schema.dump(mod_packs))

@bp.route('/mod-packs', methods=['POST'])
@auth.login_required
def create_mod_pack():
    data = request.json
    new_mod_pack = ModPack(name=data['name'])
    db.session.add(new_mod_pack)
    db.session.commit()
    return jsonify(mod_pack_schema.dump(new_mod_pack)), 201

@bp.route('/mod-packs/<int:mod_pack_id>', methods=['PUT'])
@auth.login_required
def update_mod_pack(mod_pack_id):
    data = request.json
    mod_pack = ModPack.query.get_or_404(mod_pack_id)
    if 'name' in data:
        mod_pack.name = data['name']
    db.session.commit()
    return jsonify(mod_pack_schema.dump(mod_pack))

@bp.route('/mod-packs/<int:mod_pack_id>', methods=['DELETE'])
@auth.login_required
def delete_mod_pack(mod_pack_id):
    mod_pack = ModPack.query.get_or_404(mod_pack_id)
    db.session.delete(mod_pack)
    db.session.commit()
    return '', 204

@bp.route('/mod-pack-associations', methods=['GET'])
@auth.login_required
def get_mod_pack_associations():
    mod_pack_associations = ModPackAssociation.query.all()
    return jsonify(mod_pack_associations_schema.dump(mod_pack_associations))

@bp.route('/mod-pack-associations', methods=['POST'])
@auth.login_required
def create_mod_pack_association():
    data = request.json
    new_mod_pack_association = ModPackAssociation(mod_pack_id=data['mod_pack_id'], mod_id=data['mod_id'])
    db.session.add(new_mod_pack_association)
    db.session.commit()
    return jsonify(mod_pack_association_schema.dump(new_mod_pack_association)), 201

@bp.route('/mod-pack-associations/<int:mod_pack_id>/<int:mod_id>', methods=['DELETE'])
@auth.login_required
def delete_mod_pack_association(mod_pack_id, mod_id):
    association = ModPackAssociation.query.filter_by(mod_pack_id=mod_pack_id, mod_id=mod_id).first_or_404()
    db.session.delete(association)
    db.session.commit()
    return '', 204

@bp.route('/worlds', methods=['GET'])
@auth.login_required
def get_worlds():
    worlds = World.query.all()
    return jsonify(worlds_schema.dump(worlds))

@bp.route('/worlds', methods=['POST'])
@auth.login_required
def create_world():
    data = request.json
    new_world = World(
        name=data['name'],
        mod_pack_id=data.get('mod_pack_id'),
        description=data.get('description'),
        created_at=data.get('created_at')
    )
    db.session.add(new_world)
    db.session.commit()
    return jsonify(world_schema.dump(new_world)), 201

@bp.route('/worlds/<int:world_id>', methods=['PUT'])
@auth.login_required
def update_world(world_id):
    data = request.json
    world = World.query.get_or_404(world_id)
    if 'name' in data:
        world.name = data['name']
    if 'mod_pack_id' in data:
        world.mod_pack_id = data['mod_pack_id']
    if 'description' in data:
        world.description = data['description']
    if 'created_at' in data:
        world.created_at = data['created_at']
    db.session.commit()
    return jsonify(world_schema.dump(world))

@bp.route('/worlds/<int:world_id>', methods=['DELETE'])
@auth.login_required
def delete_world(world_id):
    world = World.query.get_or_404(world_id)
    db.session.delete(world)
    db.session.commit()
    return '', 204

@bp.route('/players', methods=['GET'])
@auth.login_required
def get_players():
    players = Player.query.all()
    return jsonify(players_schema.dump(players))

@bp.route('/players', methods=['POST'])
@auth.login_required
def create_player():
    data = request.json
    new_player = Player(
        username=data['username'],
        world_id=data['world_id'],
        email=data.get('email'),
        join_date=data.get('join_date')
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify(player_schema.dump(new_player)), 201

@bp.route('/players/<int:player_id>', methods=['PUT'])
@auth.login_required
def update_player(player_id):
    data = request.json
    player = Player.query.get_or_404(player_id)
    if 'username' in data:
        player.username = data['username']
    if 'world_id' in data:
        player.world_id = data['world_id']
    if 'email' in data:
        player.email = data['email']
    if 'join_date' in data:
        player.join_date = data['join_date']
    db.session.commit()
    return jsonify(player_schema.dump(player))

@bp.route('/players/<int:player_id>', methods=['DELETE'])
@auth.login_required
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return '', 204

@bp.route('/privileges', methods=['GET'])
@auth.login_required
def get_privileges():
    privileges = Privilege.query.all()
    return jsonify(privileges_schema.dump(privileges))

@bp.route('/privileges', methods=['POST'])
@auth.login_required
def create_privilege():
    data = request.json
    new_privilege = Privilege(
        name=data['name'],
        player_id=data['player_id'],
        description=data.get('description')
    )
    db.session.add(new_privilege)
    db.session.commit()
    return jsonify(privilege_schema.dump(new_privilege)), 201

@bp.route('/privileges/<int:privilege_id>', methods=['PUT'])
@auth.login_required
def update_privilege(privilege_id):
    data = request.json
    privilege = Privilege.query.get_or_404(privilege_id)
    if 'name' in data:
        privilege.name = data['name']
    if 'player_id' in data:
        privilege.player_id = data['player_id']
    if 'description' in data:
        privilege.description = data['description']
    db.session.commit()
    return jsonify(privilege_schema.dump(privilege))

@bp.route('/privileges/<int:privilege_id>', methods=['DELETE'])
@auth.login_required
def delete_privilege(privilege_id):
    privilege = Privilege.query.get_or_404(privilege_id)
    db.session.delete(privilege)
    db.session.commit()
    return '', 204



@bp.route('/players-with-privilege-count', methods=['GET'])
@auth.login_required
def get_players_with_privilege_count():
    players = db.session.query(Player, db.func.count(Privilege.id).label('privilege_count')) \
                        .outerjoin(Privilege) \
                        .group_by(Player.id) \
                        .all()
    result = [{**player_schema.dump(player), 'privilege_count': privilege_count} for player, privilege_count in players]
    return jsonify(result)


@bp.route('/worlds-with-player-count', methods=['GET'])
@auth.login_required
def get_worlds_with_player_count():
    worlds = db.session.query(World, db.func.count(Player.id).label('player_count')) \
                       .outerjoin(Player) \
                       .group_by(World.id) \
                       .all()
    result = [{**world_schema.dump(world), 'player_count': player_count} for world, player_count in worlds]
    return jsonify(result)


@bp.route('/modpacks-with-mod-count', methods=['GET'])
@auth.login_required
def get_modpacks_with_mod_count():
    modpacks = db.session.query(ModPack, db.func.count(ModPackAssociation.mod_id).label('mod_count')) \
                         .outerjoin(ModPackAssociation) \
                         .group_by(ModPack.id) \
                         .all()
    result = [{**mod_pack_schema.dump(modpack), 'mod_count': mod_count} for modpack, mod_count in modpacks]
    return jsonify(result)


@bp.route('/worlds-with-modpack-info', methods=['GET'])
@auth.login_required
def get_worlds_with_modpack_info():
    worlds = db.session.query(World, ModPack, db.func.count(ModPackAssociation.mod_id).label('mod_count')) \
                       .outerjoin(ModPack) \
                       .outerjoin(ModPackAssociation) \
                       .group_by(World.id, ModPack.id) \
                       .all()
    result = [{**world_schema.dump(world), 'modpack': mod_pack_schema.dump(modpack), 'mod_count': mod_count} for world, modpack, mod_count in worlds]
    return jsonify(result)