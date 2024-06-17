from app import db

class Mod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    version = db.Column(db.String(20), nullable=False)

class ModPack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mods = db.relationship('Mod', secondary='mod_pack_association', backref=db.backref('mod_packs', lazy=True))

class ModPackAssociation(db.Model):
    mod_pack_id = db.Column(db.Integer, db.ForeignKey('mod_pack.id'), primary_key=True)
    mod_id = db.Column(db.Integer, db.ForeignKey('mod.id'), primary_key=True)

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    mod_pack_id = db.Column(db.Integer, db.ForeignKey('mod_pack.id'), nullable=True)
    mod_pack = db.relationship('ModPack', backref=db.backref('worlds', lazy=True))
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.String(255), nullable=False)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    world = db.relationship('World', backref=db.backref('players', lazy=True))
    email = db.Column(db.String(120), unique=True, nullable=True)
    join_date = db.Column(db.String(255), nullable=True)

class Privilege(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player', backref=db.backref('privileges', lazy=True, cascade='all, delete-orphan'))
    description = db.Column(db.String(255), nullable=True)