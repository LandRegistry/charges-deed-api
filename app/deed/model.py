from app.db import db, json_type
from sqlalchemy.sql import text


class Deed(db.Model):
    __tablename__ = 'deed'

    id = db.Column(db.Integer, primary_key=True)
    json_doc = db.Column(json_type)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all():
        return Deed.query.all()

    @staticmethod
    def get(id_):
        return Deed.query.filter_by(id=id_).first()

    @staticmethod
    def delete(id_):
        deed = Deed.query.filter_by(id=id_).first()

        if deed is None:
            return deed

        db.session.delete(deed)
        db.session.commit()

        return deed

    @staticmethod
    def matches(deed_id, borrower_id):
        conn = db.session.connection()

        sql = text("select "
                   "count(*) as count "
                   "from "
                   "(select "
                   "json_array_elements(json_doc -> 'operative-deed' -> "
                   "'borrowers') "
                   "as borrower from deed where deed_id = :deed_id) "
                   "as borrowers "
                   "where borrower ->> 'id' = :borrower_id")

        result = conn.execute(sql, deed_id=deed_id, borrower_id=borrower_id) \
            .fetchall()

        return deed_id == borrower_id
