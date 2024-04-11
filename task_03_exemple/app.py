from flask import Flask, redirect, request, render_template
from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from models import House, Complaint, Request, Flat, TypeComplaint, Specialist
from base import db, app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', buildings=House.query.all())


@app.route('/comp')
def comp():
    return render_template('comp.html', comps=Complaint.query.all())


@app.route('/req')
def req():
    return render_template('req.html', reqs=Request.query.all())


@app.route('/req/<int:id>', methods=['GET', 'POST'])
def some_req(id):
    if request.method == 'POST':
        method = request.form["_method"]
        if method == 'DELETE':
            db.session.delete(Request.query.filter_by(id=id).first())
            db.session.commit()
        elif method == 'PUT':
            req = Request.query.filter_by(id=id).first()
            req.spec_id = request.form["spec"]
            req.date = request.form["date"]
            req.comment = request.form["comment"]
            req.flat_id = request.form["flat"]
            db.session.commit()
        return redirect("/req")
    else:
        return render_template("edit_req.html", flats=Flat.query.all(),
                                                 specs=Specialist.query.all(),
                                                 req=Request.query.filter_by(id=id).first())

@app.route('/comp/<int:id>', methods=['GET', 'POST'])
def some_comp(id):
    if request.method == 'POST':
        method = request.form["_method"]
        if method == 'DELETE':
            db.session.delete(Complaint.query.filter_by(id=id).first())
            db.session.commit()
        elif method == 'PUT':
            comp = Complaint.query.filter_by(id=id).first()
            comp.comp_type_id = request.form["type"]
            comp.date = request.form["date"]
            comp.comment = request.form["comment"]
            comp.flat_id = request.form["flat"]
            db.session.commit()
        return redirect("/comp")
    else:
        return render_template("edit_comp.html", flats=Flat.query.all(),
                                                 types=TypeComplaint.query.all(),
                                                 comp=Complaint.query.filter_by(id=id).first())

@app.route('/comp/new', methods=['GET', 'POST'])
def add_comp():
    if request.method == 'POST':
        db.session.add(Complaint(request.form["type"], request.form["flat"], request.form["date"], request.form["comment"]))
        db.session.commit()
        return redirect("/comp")
    else:
        return render_template("add_comp.html", flats=Flat.query.all(),
                                                types=TypeComplaint.query.all())

@app.route('/req/new', methods=['GET', 'POST'])
def add_req():
    if request.method == 'POST':
        db.session.add(Request(request.form["spec"], request.form["flat"], request.form["date"], request.form["comment"]))
        db.session.commit()
        return redirect("/req")
    else:
        return render_template("add_req.html",  flats=Flat.query.all(),
                                                specs=Specialist.query.all())

@app.route('/house/<int:id>/req/new', methods=['GET'])
def add_req_h(id):
        return render_template("add_req.html",  flats=Flat.query.filter_by(house_id=id),
                                                specs=Specialist.query.all())

@app.route('/house/<int:id>/comp/new', methods=['GET'])
def add_comp_h(id):
        return render_template("add_comp.html", flats=Flat.query.filter_by(house_id=id),
                                                types=TypeComplaint.query.all())

if __name__ == "__main__":
    app.run()
