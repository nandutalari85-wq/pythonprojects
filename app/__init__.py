import os
from pathlib import Path
from flask import Flask, render_template
from app.config import config_by_name
from app.models import db


def create_app(config_name=None):
    """
    Application factory pattern.
    Configures database, blueprints, static assets, and custom error handlers.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development").lower()

    app = Flask(__name__)
    config_obj = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_obj)

    # Ensure charts output directory exists
    charts_dir = app.config.get("CHARTS_DIR")
    if charts_dir:
        Path(charts_dir).mkdir(parents=True, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.upload import upload_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(api_bp)

    # Register global HTTP error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html", error=e), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html", error=e), 500

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template("errors/500.html", custom_message="Uploaded file exceeds the maximum 5MB limit."), 413

    # Add custom Jinja filters for formatting
    @app.template_filter("number_format")
    def number_format_filter(value):
        if value is None or value == "":
            return "N/A"
        try:
            val = float(value)
            return f"{val:,.2f}"
        except (ValueError, TypeError):
            return str(value)

    return app
