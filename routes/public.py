"""
Public Routes
Berisi route-route yang dapat diakses publik (tanpa login)
"""

from flask import Blueprint, render_template, redirect, url_for
from models import (
    get_desa_info,
    get_all_berita,
    get_berita_by_id,
    get_config,
)
from config import NAV_LINKS, MAPS_EMBED_URL, DUSUN_DATA

public_bp = Blueprint('public', __name__)


def get_desa_info_with_maps():
    """Get desa info with maps URL"""
    info = get_desa_info()
    info['maps_embed_url'] = MAPS_EMBED_URL
    info['dusun'] = DUSUN_DATA
    return info


@public_bp.route("/")
def index():
    """Halaman utama / Beranda"""
    desa_info = get_desa_info_with_maps()
    berita_list = get_all_berita()

    # Get config values
    max_unggulan = int(get_config("berita_unggulan_tampil", 3))
    max_berita = int(get_config("berita_tampil_di_beranda", 6))

    # Featured carousel - berita UNGGULAN saja
    featured_list = [b for b in berita_list if b.get('unggulan') == 1][:max_unggulan]

    # Grid berita - berita terbaru (tidak termasuk featured)
    featured_ids = [b['id'] for b in featured_list]
    grid_berita = [b for b in berita_list if b['id'] not in featured_ids][:max_berita]

    # Config untuk template
    show_maps = get_config("tampilkan_maps", "1") == "1"
    show_stats = get_config("tampilkan_statistik", "1") == "1"
    show_dusun = get_config("tampilkan_daftar_dusun", "1") == "1"
    show_hero = get_config("tampilkan_hero", "1") == "1"
    show_views = get_config("berita_tampilkan_views", "1") == "1"
    show_tanggal = get_config("berita_tampilkan_tanggal", "1") == "1"

    return render_template(
        "index.html",
        desa=desa_info,
        nav_links=NAV_LINKS,
        featured_list=featured_list,
        berita_list=grid_berita,
        show_maps=show_maps,
        show_stats=show_stats,
        show_dusun=show_dusun,
        show_hero=show_hero,
        show_views=show_views,
        show_tanggal=show_tanggal,
    )


@public_bp.route("/berita")
def berita():
    """Halaman daftar berita"""
    desa_info = get_desa_info_with_maps()
    berita_list = get_all_berita()
    max_berita = int(get_config("berita_tampil_di_halaman", 12))
    berita_list = berita_list[:max_berita]
    show_views = get_config("berita_tampilkan_views", "1") == "1"
    show_tanggal = get_config("berita_tampilkan_tanggal", "1") == "1"

    return render_template(
        "berita.html",
        desa=desa_info,
        nav_links=[{**n, "active": n["label"] == "Berita"} for n in NAV_LINKS],
        berita_list=berita_list,
        show_views=show_views,
        show_tanggal=show_tanggal,
    )


@public_bp.route("/berita/<int:berita_id>")
def detail_berita(berita_id):
    """Halaman detail berita"""
    desa_info = get_desa_info_with_maps()
    artikel = get_berita_by_id(berita_id)
    if not artikel:
        return "Berita tidak ditemukan", 404
    show_views = get_config("berita_tampilkan_views", "1") == "1"
    show_tanggal = get_config("berita_tampilkan_tanggal", "1") == "1"

    return render_template(
        "detail_berita.html",
        desa=desa_info,
        nav_links=[{**n, "active": n["label"] == "Berita"} for n in NAV_LINKS],
        artikel=artikel,
        show_views=show_views,
        show_tanggal=show_tanggal,
    )


@public_bp.route("/surat")
def surat_info():
    """Halaman info layanan surat"""
    desa_info = get_desa_info_with_maps()
    return render_template(
        "surat_info.html",
        desa=desa_info,
        nav_links=[{**n, "active": n["label"] == "Surat"} for n in NAV_LINKS],
    )


@public_bp.route("/layanan")
def layanan():
    """Halaman daftar layanan"""
    desa_info = get_desa_info_with_maps()
    return render_template(
        "layanan.html",
        desa=desa_info,
        nav_links=[{**n, "active": n["label"] == "Layanan"} for n in NAV_LINKS],
    )
