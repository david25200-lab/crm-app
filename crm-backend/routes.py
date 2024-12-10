from flask import Blueprint, request, jsonify
from models import db, Contact
from forms import ContactForm

main = Blueprint('main', __name__)

@main.route('/api/contacts', methods=['POST'])
def add_contact():
    form = ContactForm(data=request.get_json())
    if form.validate():
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201
    return jsonify({'error': form.errors}), 400
from flask import Blueprint, request, jsonify
from models import db, Contact
from flasgger import swag_from

main = Blueprint('main', __name__)

@main.route('/api/contacts', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all contacts',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}
                ]
            }
        }
    }
})
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([contact.to_dict() for contact in contacts])

@main.route('/api/contacts', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Contact',
                'required': ['name', 'email'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Jane Doe'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'jane@example.com'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Contact created successfully',
            'examples': {
                'application/json': {
                    'id': 2, 'name': 'Jane Doe', 'email': 'jane@example.com'
                }
            }
        }
    }
})
def add_contact():
    data = request.get_json()
    new_contact = Contact(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact.to_dict()), 201

@main.route('/api/contacts/<int:id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Contact',
                'required': ['name', 'email'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Jane Doe Updated'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'janeupdated@example.com'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Contact updated successfully',
            'examples': {
                'application/json': {
                    'id': 2, 'name': 'Jane Doe Updated', 'email': 'janeupdated@example.com'
                }
            }
        }
    }
})
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get(id)
    if contact:
        contact.name = data['name']
        contact.email = data['email']
        db.session.commit()
        return jsonify(contact.to_dict()), 200
    else:
        return jsonify({'message': 'Contact not found'}), 404

@main.route('/api/contacts/<int:id>', methods=['DELETE'])
@swag_from({
    'responses': {
        200: {
            'description': 'Contact deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Contact deleted successfully'
                }
            }
        },
        404: {
            'description': 'Contact not found',
            'examples': {
                'application/json': {
                    'message': 'Contact not found'
                }
            }
        }
    }
})
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    else:
        return jsonify({'message': 'Contact not found'}), 404
from flask import request, jsonify
from flask_login import login_user, logout_user, login_required

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200



