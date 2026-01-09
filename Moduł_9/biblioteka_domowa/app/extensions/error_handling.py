from flask import jsonify, make_response


def register_handlers(app):
    
    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({'error': 'Forbidden', 'status_code': 403}), 403)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)
