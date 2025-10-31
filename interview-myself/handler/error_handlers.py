from tools.api_response import api_response


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return api_response(404, "请求的资源未找到", None)
