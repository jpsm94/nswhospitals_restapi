from flask import Flask, g, jsonify, make_response
from flask_restplus import Api, Resource, fields
import sqlite3
from os import path

app = Flask(__name__)
api = Api(app, version='1.0', title='Data Service for NSW Hospitals',
          description='This is a Flask-Restplus data service that provides APIs for searching hospitals in NSW',
          )

#Database helper
ROOT = path.dirname(path.realpath(__file__))
def connect_db():
    sql = sqlite3.connect(path.join(ROOT, "NSW_HOSPITALS.sqlite"))
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def get_return_values(details):
    return_values = []

    for detail in details:
        detail_dict = {}
        detail_dict['Name'] = detail['Name']
        address_dict = {}
        address_dict['StreetAddress'] = detail['StreetAddress']
        address_dict['Suburb'] = detail['Suburb']
        address_dict['Postcode'] = detail['Postcode']
        address_dict['State'] = detail['State']
        address_dict['Country'] = detail['Country']
        detail_dict['Address'] = address_dict
        geoloc_dict = {}
        geoloc_dict['Latitude'] = detail['Latitude']
        geoloc_dict['Longitude'] = detail['Longitude']
        detail_dict['Geolocation'] = geoloc_dict
        contact_dict = {}
        contact_dict['Email'] = '' if detail['Email'] is None else detail['Email']
        contact_dict['Fax'] = '' if detail['Fax'] is None else detail['Fax']
        contact_dict['Website'] = '' if detail['Website'] is None else detail['Website']
        detail_dict['ContactInfo'] = contact_dict
        detail_dict['LocalHealthDistrict'] = detail['LocalHealthDistrict']
        detail_dict['EmergencyDept'] = detail['EmergencyDept']

        return_values.append(detail_dict)

    return return_values

@api.route('/hospitals')
class HospitalAll(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieves all NSW Hospitals')
    def get(self):
        db = get_db()
        details_cur = db.execute('select * from NSW_HOSPITALS')
        details = details_cur.fetchall()

        return_values = get_return_values(details)

        return make_response(jsonify(return_values), 200)


@api.route('/hospitals/<string:SUBURB>', methods=['GET'])
class HospitalBySuburb(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieves hospitals in the specified suburb')
    def get(self, SUBURB):
        db = get_db()
        details_cur = db.execute(
            'select * from NSW_HOSPITALS where Suburb = ? COLLATE NOCASE', [SUBURB])
        details = details_cur.fetchall()

        return_values = get_return_values(details)

        return make_response(jsonify(return_values), 200)

@api.route('/hospitals/<int:POSTCODE>', methods=['GET'])
class HospitalByPostcode(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieves hospitals in the specified postcode')
    def get(self, POSTCODE):
        db = get_db()
        details_cur = db.execute(
            'select * from NSW_HOSPITALS where Postcode = ? COLLATE NOCASE', [POSTCODE])
        details = details_cur.fetchall()

        return_values = get_return_values(details)

        return make_response(jsonify(return_values), 200)

@api.route('/hospitals/<string:LOCALHEALTHDISTRICT>', methods=['GET'])
class HospitalByLHD(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieves hospitals in the specified local health district')
    def get(self, LOCALHEALTHDISTRICT):
        db = get_db()
        details_cur = db.execute(
            'select * from NSW_HOSPITALS where LocalHealthDistrict = ? COLLATE NOCASE', [LOCALHEALTHDISTRICT])
        details = details_cur.fetchall()

        return_values = get_return_values(details)

        return make_response(jsonify(return_values), 200)        

@api.route('/localhealthdistricts', methods=['GET'])
class LHDAll(Resource):
    @api.response(200, 'SUCCESSFUL: Contents successfully loaded')
    @api.response(204, 'NO CONTENT: No content in database')
    @api.doc(description='Retrieves a list of local health districts')
    def get(self):
        db = get_db()
        details_cur = db.execute(
            'select distinct(LocalHealthDistrict) from NSW_HOSPITALS order by Name')
        details = details_cur.fetchall()

        return_values = [detail['LocalHealthDistrict'] for detail in details]

        return make_response(jsonify(return_values), 200)                

if __name__ == '__main__':
    app.run()    