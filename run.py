from app import create_app, db
from app.models import Mod, ModPack, ModPackAssociation, World, Player, Privilege
from datetime import datetime

def populate_db():
    app = create_app()
    with app.app_context():
        mod_names = ['Mod1', 'Mod2', 'Mod3']
        for name in mod_names:
            if not Mod.query.filter_by(name=name).first():
                mod = Mod(name=name, version='1.0')
                db.session.add(mod)
        db.session.commit()

        mod_pack_names = ['ModPack1', 'ModPack2', 'ModPack3']
        for name in mod_pack_names:
            if not ModPack.query.filter_by(name=name).first():
                mod_pack = ModPack(name=name)
                db.session.add(mod_pack)
        db.session.commit()

        mod_pack1 = ModPack.query.filter_by(name='ModPack1').first()
        mod_pack2 = ModPack.query.filter_by(name='ModPack2').first()
        mod_pack3 = ModPack.query.filter_by(name='ModPack3').first()

        mod1 = Mod.query.filter_by(name='Mod1').first()
        mod2 = Mod.query.filter_by(name='Mod2').first()
        mod3 = Mod.query.filter_by(name='Mod3').first()

        associations = [
            (mod_pack1, mod1),
            (mod_pack1, mod2),
            (mod_pack2, mod2),
            (mod_pack2, mod3),
            (mod_pack3, mod1),
            (mod_pack3, mod3)
        ]

        for mod_pack, mod in associations:
            if not ModPackAssociation.query.filter_by(mod_pack_id=mod_pack.id, mod_id=mod.id).first():
                association = ModPackAssociation(mod_pack_id=mod_pack.id, mod_id=mod.id)
                db.session.add(association)
        db.session.commit()

        world_names = ['World1', 'World2', 'World3']
        for name in world_names:
            if not World.query.filter_by(name=name).first():
                world = World(name=name, mod_pack_id=mod_pack1.id, description='Description1', created_at=datetime.now())
                db.session.add(world)
        db.session.commit()

        player_names = ['Player1', 'Player2', 'Player3']
        for name in player_names:
            if not Player.query.filter_by(username=name).first():
                player = Player(username=name, world_id=1, email=f'{name}@example.com', join_date=datetime.now())
                db.session.add(player)
        db.session.commit()

        privilege_names = ['Privilege1', 'Privilege2', 'Privilege3', 'Privilege4', 'Privilege5', 'Privilege6']
        player1 = Player.query.filter_by(username='Player1').first()
        player2 = Player.query.filter_by(username='Player2').first()
        player3 = Player.query.filter_by(username='Player3').first()

        for i, name in enumerate(privilege_names):
            player = [player1, player1, player2, player2, player3, player3][i]
            if not Privilege.query.filter_by(name=name, player_id=player.id).first():
                privilege = Privilege(name=name, player_id=player.id, description=f'Description{i+1}')
                db.session.add(privilege)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    populate_db()
    app.run(debug=True)