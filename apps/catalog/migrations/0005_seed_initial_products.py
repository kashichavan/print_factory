from decimal import Decimal
from django.db import migrations

def seed_catalog_data(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Product = apps.get_model("catalog", "Product")

    categories_data = [
        ("Apparel & Merch", "apparel", "Custom printed T-shirts, polo shirts, executive hoodies, caps, and tote bags for corporate teams.", "No Min Order", "👕"),
        ("Apparel & T-Shirts", "tshirt", "Custom printed Polo T-shirts, Round Neck Tees, and Corporate Hoodies.", "POPULAR", "👕"),
        ("Business Cards", "business-cards", "Premium Matte, Gloss, Rounded Corner, and Foil Business Cards.", "BESTSELLER", "💳"),
        ("Corporate Gifts", "gifting", "Personalized employee welcome kits, insulated tumblers, leather journals, mugs, and executive pen sets.", "Laser Engraved", "🎁"),
        ("ID Cards & Accessories", "id-card", "PVC Corporate ID Cards, Custom Printed Lanyards, and Badge Holders.", "ESSENTIAL", "🎴"),
        ("Marketing & Stationery", "stationery", "Letterheads, envelopes, tri-fold brochures, flyers, die-cut stickers, and rubber stamps.", "High Resolution", "📜"),
        ("Packaging & Boxes", "packaging", "Custom printed mailer boxes, product packaging, shipping bags, custom tape, and tissue paper.", "Custom Sizes", "📦"),
        ("Signage & Displays", "signage", "Roll-up standees, acrylic lobby signs, vinyl banners, poster prints, and branded tablecloths.", "Outdoor Durable", "🖼️")
    ]

    cat_map = {}
    for name, slug, desc, badge, icon in categories_data:
        cat, _ = Category.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "description": desc,
                "badge": badge,
                "icon": icon,
                "is_active": True,
            }
        )
        cat_map[slug] = cat

    products_data = [
        ("Custom Premium Polo T-Shirt", "custom-polo-tshirt", "tshirt", "print", "100% Combed Cotton 220gsm Polo with Custom Logo Embroidery.", "Elevate your corporate branding with premium embroidered Polo T-Shirts. Breathable fabric, vibrant colors, and durable stitching.", "499.00", "4.9", 142, "Bestseller", ""),
        ("PVC Corporate ID Card + Custom Lanyard Kit", "pvc-corporate-id-card", "id-card", "print", "High-definition dual-sided PVC ID cards with 16mm satin lanyard.", "Durable, water-resistant PVC ID cards printed with ultra-sharp digital dye-sublimation. Includes custom satin lanyard with safety breakaway clip.", "99.00", "4.8", 98, "Popular", ""),
        ("Standard Matte Business Cards", "standard-matte-business-cards", "business-cards", "print", "Classic 350gsm matte laminated cards with sharp precision print.", "Premium Vistaprint-style business cards printed on 350gsm art card stock with velvety smooth matte lamination.", "190.00", "5.0", 310, "Top Seller", ""),
        ("Standard Business Cards", "standard-business-cards", "business-cards", "print", "Clean 300gsm matte or glossy paper cards for high-volume networking.", "Printed on high-density 300gsm premium paper stock. Ideal for everyday business networking and corporate teams.", "190.00", "4.9", 340, "Bestseller", "images/trending-cards-perspective.jpg"),
        ("Metallic Gold & Silver Foil Cards", "metallic-foil-business-cards", "business-cards", "print", "3D elevated gold or silver foil accents on velvety 400gsm cardstock.", "Make an impression with metallic foil stamping. Choose gold, silver, or rose gold foil applied to logos.", "390.00", "5.0", 185, "3D Foil Stamping", "images/trending-cards-perspective.jpg"),
        ("Eco-Friendly Recycled Kraft Cards", "recycled-kraft-business-cards", "business-cards", "print", "100% recycled unbleached brown kraft paper with warm earthy texture.", "Organic, tactile, 350gsm recycled kraft paper cards designed for eco-conscious brands.", "240.00", "4.8", 92, "100% Recycled", "images/trending-packaging-perspective.jpg"),
        ("Super Thick 600gsm Velvet Cards", "velvet-touch-business-cards", "business-cards", "print", "Ultra-heavyweight 600gsm cardstock with a soft-touch matte finish.", "Double-thick 600gsm board featuring rich velvet soft-touch lamination.", "450.00", "4.9", 142, "Heavyweight", "images/trending-gifting-perspective.jpg"),
        ("Custom Corrugated Mailer Boxes", "custom-mailer-boxes", "packaging", "print", "Heavy-duty E-flute corrugated shipping boxes with full custom exterior printing.", "Protect products in transit while delivering an unforgettable unboxing experience. Easy fold assembly.", "45.00", "4.9", 210, "High Durability", "images/trending-packaging-perspective.jpg"),
        ("Premium Rigid Magnetic Gift Boxes", "matte-black-gift-boxes", "packaging", "print", "Collapsible rigid magnetic closure boxes with foil embossed logo options.", "Luxurious magnetic flap gift box crafted from 1200gsm rigid cardboard. Perfect for high-end merch.", "120.00", "5.0", 88, "Luxury Box", "images/trending-packaging-perspective.jpg"),
        ("Custom Corporate Polo Shirts", "custom-polo-shirts", "apparel", "print", "Breathable 220gsm pique cotton polo with custom embroidered or screen-printed logo.", "Professional polo shirts engineered for daily corporate wear. Double-needle stitched hems.", "350.00", "4.9", 175, "100% Bio-Washed Cotton", "images/vp-apparel-hero.jpg"),
        ("Executive Fleece Team Hoodies", "corporate-team-hoodies", "apparel", "print", "Cozy 320gsm cotton-fleece pullover hoodie with kangaroo pouch and custom print.", "Warm, durable fleece hoodies for tech startups and corporate teams. Soft brushed interior.", "790.00", "4.9", 115, "320gsm Heavy Fleece", "images/vp-apparel-hero.jpg"),
        ("Tri-Fold Marketing Brochures", "tri-fold-brochures", "stationery", "print", "Vibrant 170gsm glossy paper brochures with clean double fold panels.", "Communicate product services with high-density offset printed tri-fold brochures.", "250.00", "4.8", 96, "Full Color", "images/vp-stationery-hero.jpg"),
        ("Custom Die-Cut Vinyl Stickers", "die-cut-vinyl-stickers", "stationery", "print", "Weatherproof vinyl stickers cut precisely to your custom logo shape.", "UV-resistant vinyl stickers that stick to laptops, water bottles, and packaging without peeling.", "99.00", "5.0", 230, "Waterproof", "images/vp-stationery-hero.jpg"),
        ("Roll-Up Standee Banners", "roll-up-standee-banners", "signage", "print", "Portable 6x3 ft retractable banner with non-curl greyback banner media.", "Setup trade show displays in seconds. Sturdy aluminum base cassette with carrying bag included.", "850.00", "4.9", 164, "Includes Aluminum Stand", "images/trending-signage-perspective.jpg"),
        ("Edge-Lit Acrylic Lobby Signboard", "edge-lit-acrylic-signboard", "signage", "print", "Illuminated laser-engraved acrylic board with brushed stainless steel standoffs.", "Modern architectural wall mounted signs for corporate reception areas and executive office suites.", "1450.00", "5.0", 72, "LED Architectural", "images/trending-signage-perspective.jpg"),
        ("Deluxe Employee Onboarding Gift Box", "executive-onboarding-welcome-kit", "gifting", "print", "Leather journal, insulated tumbler, metallic pen & gift box customized with employee name.", "Make new hires feel valued from day one with a curated onboarding merchandise box.", "1250.00", "5.0", 140, "Custom Gift Box", "images/trending-gifting-perspective.jpg"),
        ("Laser-Engraved Vacuum Tumbler (500ml)", "laser-engraved-insulated-tumbler", "gifting", "print", "Double-wall stainless steel travel mug with permanent precision laser logo engraving.", "Keep drinks hot or icy all day. Leakproof flip lid and sweat-free powder coating.", "450.00", "4.9", 198, "12hr Hot / 24hr Cold", "images/trending-gifting-perspective.jpg")
    ]

    for name, slug, cat_slug, ptype, sdesc, desc, bprice, rat, rcnt, badge, img in products_data:
        cat = cat_map.get(cat_slug)
        if cat:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": cat,
                    "product_type": ptype,
                    "short_description": sdesc,
                    "description": desc,
                    "base_price": Decimal(bprice),
                    "rating": Decimal(rat),
                    "review_count": rcnt,
                    "badge": badge,
                    "image": img,
                    "is_active": True,
                }
            )

def remove_catalog_data(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_product_catalog_pro_is_acti_1a8de5_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_catalog_data, remove_catalog_data),
    ]
