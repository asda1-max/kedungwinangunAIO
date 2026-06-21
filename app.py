"""
Desa Kedungwinangun - Sistem Informasi Desa Digital
=================================================

Aplikasi web Flask untuk pengelolaan website desa dan layanan surat online.

Struktur Project:
    app.py           - Entry point utama
    config.py        - Konfigurasi dan konstanta
    models.py        - Database models dan helpers
    routes/          - Route handlers
        __init__.py
        public.py    - Route publik (beranda, berita)
        admin.py    - Route admin (kelola berita, config)
        user.py     - Route warga (register, login, permohonan)
        dinas.py    - Route dinas (verifikasi, approve surat)
    templates/       - Template HTML
    static/          - Asset statis

Run:
    python app.py
"""

from flask import Flask, jsonify
from os import environ, makedirs
from os.path import exists

from config import Config
from models import init_database

# ── Create Flask App ──────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# Create upload folder if not exists
makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


# ── Register Blueprints ───────────────────────────────────────────────
from routes import public_bp, admin_bp, user_bp, dinas_bp

app.register_blueprint(public_bp)    # Public routes: /, /berita, /berita/<id>
app.register_blueprint(admin_bp)      # Admin routes: /admin/*
app.register_blueprint(user_bp)       # User routes: /register, /login, /dashboard, /surat/*
app.register_blueprint(dinas_bp)      # Dinas routes: /dinas/*


# ── Error Handlers ────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return {"error": "Halaman tidak ditemukan"}, 404


@app.errorhandler(500)
def server_error(e):
    return {"error": "Terjadi kesalahan server"}, 500


# ── API Routes ────────────────────────────────────────────────────────

@app.route("/api/berita")
def api_berita():
    """API untuk mengambil semua berita (JSON)"""
    from models import get_all_berita
    return jsonify(get_all_berita())


# ── Health Check ────────────────────────────────────────────────────────

@app.route("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "app": "Desa Kedungwinangun"}


# ── Run Server ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize database on first run
    init_database()

    # Get port from environment or default to 5000
    port = int(environ.get('PORT', 5000))

    # Run development server
    app.run(
        debug=True,
        host='0.0.0.0',
        port=port
    )
