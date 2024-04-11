from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text
from base import db


class Complaint(db.Model):
    __tablename__ = 'Complaint'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(collation='utf8_bin'), nullable=False)
    flat_id = db.Column(db.ForeignKey('Flat.id', onupdate='CASCADE'), nullable=False, index=True)
    comp_type_id = db.Column(db.ForeignKey('TypeComplaint.id', onupdate='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)

    comp_type = db.relationship('TypeComplaint', primaryjoin='Complaint.comp_type_id == TypeComplaint.id', backref='complaints')
    flat = db.relationship('Flat', primaryjoin='Complaint.flat_id == Flat.id', backref='complaints')

    # def __init__(self, t, f, d, c):
    #     self.comp_type_id = t
    #     self.flat_id = f
    #     self.date = d
    #     self.comment = c


class Flat(db.Model):
    __tablename__ = 'Flat'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.ForeignKey('Owner.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    house_id = db.Column(db.ForeignKey('House.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    num = db.Column(db.Integer, nullable=False)

    house = db.relationship('House', primaryjoin='Flat.house_id == House.id', backref='flats')
    owner = db.relationship('Owner', primaryjoin='Flat.owner_id == Owner.id', backref='flats')


class House(db.Model):
    __tablename__ = 'House'

    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    photo = db.Column(db.String(200, 'utf8_bin'))
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    descr = db.Column(db.Text(collation='utf8_bin'), nullable=False)


class Owner(db.Model):
    __tablename__ = 'Owner'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    dob = db.Column(db.Date, nullable=False)


class Prof(db.Model):
    __tablename__ = 'Prof'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)


class Request(db.Model):
    __tablename__ = 'Request'

    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.ForeignKey('Specialist.id', onupdate='CASCADE'), nullable=False, index=True)
    flat_id = db.Column(db.ForeignKey('Flat.id', onupdate='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.Text(collation='utf8_bin'), nullable=False)

    flat = db.relationship('Flat', primaryjoin='Request.flat_id == Flat.id', backref='requests')
    spec = db.relationship('Specialist', primaryjoin='Request.spec_id == Specialist.id', backref='requests')

    def __init__(self, s, f, d, c):
        self.spec_id = s
        self.flat_id = f
        self.date = d
        self.comment = c


class Specialist(db.Model):
    __tablename__ = 'Specialist'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200, 'utf8_bin'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    prof_id = db.Column(db.ForeignKey('Prof.id', onupdate='CASCADE'), nullable=False, index=True)

    prof = db.relationship('Prof', primaryjoin='Specialist.prof_id == Prof.id', backref='specialists')


class TypeComplaint(db.Model):
    __tablename__ = 'TypeComplaint'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200, 'utf8_bin'), nullable=False)




t_comp_view = db.Table(
    'comp_view',
    db.Column('comment', db.Text),
    db.Column('date', db.Date),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('num', db.Integer),
    db.Column('house', db.String(200)),
    db.Column('fio', db.String(200)),
    db.Column('name', db.String(200))
)


t_flat_view = db.Table(
    'flat_view',
    db.Column('flat', db.String(213)),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('h_id', db.Integer, server_default=db.FetchedValue())
)


t_req_view = db.Table(
    'req_view',
    db.Column('date', db.Date),
    db.Column('id', db.Integer, server_default=db.FetchedValue()),
    db.Column('comment', db.Text),
    db.Column('num', db.Integer),
    db.Column('fio', db.String(200)),
    db.Column('spec', db.String(403)),
    db.Column('house', db.String(200))
)


t_spec_view = db.Table(
    'spec_view',
    db.Column('name', db.String(402)),
    db.Column('id', db.Integer, server_default=db.FetchedValue())
)
