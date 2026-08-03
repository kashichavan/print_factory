from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product, ProductOption, OptionValue, ProductVariant, PriceRule

class Command(BaseCommand):
    help = "Seed complete end-to-end Vistaprint storefront categories, products, images, and price rules"

    def handle(self, *args, **options):
        self.stdout.write("Seeding full Vistaprint catalog database...")

        # 1. Create Categories
        categories_info = [
            {"slug": "business-cards", "name": "Business Cards", "icon": "💳", "badge": "50+ Stocks", "desc": "Custom printed business cards with premium paper stocks, metallic foil, rounded corners, and instant bulk pricing."},
            {"slug": "packaging", "name": "Packaging & Boxes", "icon": "📦", "badge": "Custom Sizes", "desc": "Custom printed mailer boxes, product packaging, shipping bags, custom tape, and tissue paper."},
            {"slug": "apparel", "name": "Apparel & Merch", "icon": "👕", "badge": "No Min Order", "desc": "Custom printed T-shirts, polo shirts, executive hoodies, caps, and tote bags for corporate teams."},
            {"slug": "stationery", "name": "Marketing & Stationery", "icon": "📜", "badge": "High Resolution", "desc": "Letterheads, envelopes, tri-fold brochures, flyers, die-cut stickers, and rubber stamps."},
            {"slug": "signage", "name": "Signage & Displays", "icon": "🖼️", "badge": "Outdoor Durable", "desc": "Roll-up standees, acrylic lobby signs, vinyl banners, poster prints, and branded tablecloths."},
            {"slug": "gifting", "name": "Corporate Gifts", "icon": "🎁", "badge": "Laser Engraved", "desc": "Personalized employee welcome kits, insulated tumblers, leather journals, mugs, and executive pen sets."},
        ]

        category_map = {}
        for cdata in categories_info:
            cat, _ = Category.objects.get_or_create(
                slug=cdata["slug"],
                defaults={
                    "name": cdata["name"],
                    "icon": cdata["icon"],
                    "badge": cdata["badge"],
                    "description": cdata["desc"],
                    "is_active": True,
                }
            )
            category_map[cdata["slug"]] = cat

        # 2. Comprehensive Products List
        products_list = [
            # Business Cards
            {
                "cat": "business-cards", "slug": "standard-business-cards",
                "name": "Standard Business Cards", "badge": "Bestseller", "rating": "4.9", "reviews": 340, "base_price": Decimal("190.00"),
                "short": "Clean 300gsm matte or glossy paper cards for high-volume networking.",
                "desc": "Printed on high-density 300gsm premium paper stock. Ideal for everyday business networking and corporate teams.",
                "image": "images/trending-cards-perspective.jpg",
                "options": [
                    ("paper", "Paper Stock", [("Standard Matte (300gsm)", 0), ("Premium Glossy (350gsm)", 40), ("Velvet Soft-Touch", 120)]),
                    ("corners", "Corner Style", [("Standard Square", 0), ("4 Rounded Corners", 50)]),
                    ("sides", "Printing Sides", [("Front Only", 0), ("Front & Back", 100)]),
                ]
            },
            {
                "cat": "business-cards", "slug": "metallic-foil-business-cards",
                "name": "Metallic Gold & Silver Foil Cards", "badge": "3D Foil Stamping", "rating": "5.0", "reviews": 185, "base_price": Decimal("390.00"),
                "short": "3D elevated gold or silver foil accents on velvety 400gsm cardstock.",
                "desc": "Make an impression with metallic foil stamping. Choose gold, silver, or rose gold foil applied to logos.",
                "image": "images/trending-cards-perspective.jpg",
                "options": [
                    ("foil", "Foil Color", [("Gold Foil", 0), ("Silver Foil", 0), ("Rose Gold Foil", 50)]),
                    ("paper", "Paper Stock", [("Velvet Touch (400gsm)", 0), ("Ultra Black Board", 100)]),
                    ("corners", "Corner Style", [("Square", 0), ("Rounded", 50)]),
                ]
            },
            {
                "cat": "business-cards", "slug": "recycled-kraft-business-cards",
                "name": "Eco-Friendly Recycled Kraft Cards", "badge": "100% Recycled", "rating": "4.8", "reviews": 92, "base_price": Decimal("240.00"),
                "short": "100% recycled unbleached brown kraft paper with warm earthy texture.",
                "desc": "Organic, tactile, 350gsm recycled kraft paper cards designed for eco-conscious brands.",
                "image": "images/trending-packaging-perspective.jpg",
                "options": [
                    ("paper", "Kraft Type", [("Brown Eco Kraft (350gsm)", 0), ("White Organic Cotton", 60)]),
                    ("corners", "Corners", [("Square", 0), ("Rounded", 50)]),
                ]
            },
            {
                "cat": "business-cards", "slug": "velvet-touch-business-cards",
                "name": "Super Thick 600gsm Velvet Cards", "badge": "Heavyweight", "rating": "4.9", "reviews": 142, "base_price": Decimal("450.00"),
                "short": "Ultra-heavyweight 600gsm cardstock with a soft-touch matte finish.",
                "desc": "Double-thick 600gsm board featuring rich velvet soft-touch lamination.",
                "image": "images/trending-gifting-perspective.jpg",
                "options": [
                    ("finish", "Finish", [("Matte Velvet", 0), ("Spot UV Gloss Accent", 100)]),
                    ("corners", "Corners", [("Square", 0), ("Rounded", 50)]),
                ]
            },

            # Packaging & Boxes
            {
                "cat": "packaging", "slug": "custom-mailer-boxes",
                "name": "Custom Corrugated Mailer Boxes", "badge": "High Durability", "rating": "4.9", "reviews": 210, "base_price": Decimal("45.00"),
                "short": "Heavy-duty E-flute corrugated shipping boxes with full custom exterior printing.",
                "desc": "Protect products in transit while delivering an unforgettable unboxing experience. Easy fold assembly.",
                "image": "images/trending-packaging-perspective.jpg",
                "options": [
                    ("size", "Box Size", [("Small (6x4x2 in)", 0), ("Medium (9x6x3 in)", 25), ("Large (12x9x4 in)", 50)]),
                    ("print", "Print Option", [("Exterior Only", 0), ("Exterior & Interior", 30)]),
                ]
            },
            {
                "cat": "packaging", "slug": "matte-black-gift-boxes",
                "name": "Premium Rigid Magnetic Gift Boxes", "badge": "Luxury Box", "rating": "5.0", "reviews": 88, "base_price": Decimal("120.00"),
                "short": "Collapsible rigid magnetic closure boxes with foil embossed logo options.",
                "desc": "Luxurious magnetic flap gift box crafted from 1200gsm rigid cardboard. Perfect for high-end merch.",
                "image": "images/trending-packaging-perspective.jpg",
                "options": [
                    ("color", "Box Finish", [("Matte Black", 0), ("Pure White", 0), ("Kraft Brown", 10)]),
                    ("foil", "Logo Foil", [("Gold Foil Logo", 40), ("Silver Foil Logo", 40)]),
                ]
            },

            # Apparel & Merch
            {
                "cat": "apparel", "slug": "custom-polo-shirts",
                "name": "Custom Corporate Polo Shirts", "badge": "100% Bio-Washed Cotton", "rating": "4.9", "reviews": 175, "base_price": Decimal("350.00"),
                "short": "Breathable 220gsm pique cotton polo with custom embroidered or screen-printed logo.",
                "desc": "Professional polo shirts engineered for daily corporate wear. Double-needle stitched hems.",
                "image": "images/vp-apparel-hero.jpg",
                "options": [
                    ("color", "Shirt Color", [("Navy Blue", 0), ("Heather Grey", 0), ("Black", 0), ("White", 0)]),
                    ("size", "Size", [("Small", 0), ("Medium", 0), ("Large", 0), ("XL", 20), ("XXL", 40)]),
                    ("type", "Logo Style", [("Embroidered Chest Logo", 50), ("Screen Printed", 0)]),
                ]
            },
            {
                "cat": "apparel", "slug": "corporate-team-hoodies",
                "name": "Executive Fleece Team Hoodies", "badge": "320gsm Heavy Fleece", "rating": "4.9", "reviews": 115, "base_price": Decimal("790.00"),
                "short": "Cozy 320gsm cotton-fleece pullover hoodie with kangaroo pouch and custom print.",
                "desc": "Warm, durable fleece hoodies for tech startups and corporate teams. Soft brushed interior.",
                "image": "images/vp-apparel-hero.jpg",
                "options": [
                    ("color", "Color", [("Charcoal Grey", 0), ("Jet Black", 0), ("Navy", 0)]),
                    ("size", "Size", [("Medium", 0), ("Large", 0), ("XL", 30)]),
                ]
            },

            # Marketing & Stationery
            {
                "cat": "stationery", "slug": "tri-fold-brochures",
                "name": "Tri-Fold Marketing Brochures", "badge": "Full Color", "rating": "4.8", "reviews": 96, "base_price": Decimal("250.00"),
                "short": "Vibrant 170gsm glossy paper brochures with clean double fold panels.",
                "desc": "Communicate product services with high-density offset printed tri-fold brochures.",
                "image": "images/vp-stationery-hero.jpg",
                "options": [
                    ("paper", "Paper Weight", [("170gsm Glossy", 0), ("250gsm Premium Art Paper", 80)]),
                    ("fold", "Folding Style", [("Tri-Fold (Z-Fold)", 0), ("Bi-Fold (Half-Fold)", 0)]),
                ]
            },
            {
                "cat": "stationery", "slug": "die-cut-vinyl-stickers",
                "name": "Custom Die-Cut Vinyl Stickers", "badge": "Waterproof", "rating": "5.0", "reviews": 230, "base_price": Decimal("99.00"),
                "short": "Weatherproof vinyl stickers cut precisely to your custom logo shape.",
                "desc": "UV-resistant vinyl stickers that stick to laptops, water bottles, and packaging without peeling.",
                "image": "images/vp-stationery-hero.jpg",
                "options": [
                    ("finish", "Lamination", [("Glossy Waterproof", 0), ("Matte Soft Feel", 20), ("Holographic Laser", 50)]),
                    ("size", "Sticker Size", [("2x2 inches", 0), ("3x3 inches", 40), ("4x4 inches", 80)]),
                ]
            },

            # Signage & Displays
            {
                "cat": "signage", "slug": "roll-up-standee-banners",
                "name": "Roll-Up Standee Banners", "badge": "Includes Aluminum Stand", "rating": "4.9", "reviews": 164, "base_price": Decimal("850.00"),
                "short": "Portable 6x3 ft retractable banner with non-curl greyback banner media.",
                "desc": "Setup trade show displays in seconds. Sturdy aluminum base cassette with carrying bag included.",
                "image": "images/trending-signage-perspective.jpg",
                "options": [
                    ("size", "Banner Size", [("6x3 Feet (Standard)", 0), ("6x4 Feet (Wide)", 300)]),
                    ("media", "Media Type", [("Non-Curl Star Flex", 0), ("Premium Satin Fabric", 200)]),
                ]
            },
            {
                "cat": "signage", "slug": "edge-lit-acrylic-signboard",
                "name": "Edge-Lit Acrylic Lobby Signboard", "badge": "LED Architectural", "rating": "5.0", "reviews": 72, "base_price": Decimal("1450.00"),
                "short": "Illuminated laser-engraved acrylic board with brushed stainless steel standoffs.",
                "desc": "Modern architectural wall mounted signs for corporate reception areas and executive office suites.",
                "image": "images/trending-signage-perspective.jpg",
                "options": [
                    ("led", "Lighting", [("White LED Border", 0), ("Warm Amber LED", 0), ("RGB Color Shift", 250)]),
                    ("mount", "Hardware", [("Stainless Steel Standoffs", 0), ("Floating Black Frame", 200)]),
                ]
            },

            # Corporate Gifts
            {
                "cat": "gifting", "slug": "executive-onboarding-welcome-kit",
                "name": "Deluxe Employee Onboarding Gift Box", "badge": "Custom Gift Box", "rating": "5.0", "reviews": 140, "base_price": Decimal("1250.00"),
                "short": "Leather journal, insulated tumbler, metallic pen & gift box customized with employee name.",
                "desc": "Make new hires feel valued from day one with a curated onboarding merchandise box.",
                "image": "images/trending-gifting-perspective.jpg",
                "options": [
                    ("color", "Theme Color", [("Espresso Brown Leather", 0), ("Matte Midnight Black", 0), ("Navy & Gold", 50)]),
                    ("personalize", "Individual Name Engraving", [("Included Free", 0)]),
                ]
            },
            {
                "cat": "gifting", "slug": "laser-engraved-insulated-tumbler",
                "name": "Laser-Engraved Vacuum Tumbler (500ml)", "badge": "12hr Hot / 24hr Cold", "rating": "4.9", "reviews": 198, "base_price": Decimal("450.00"),
                "short": "Double-wall stainless steel travel mug with permanent precision laser logo engraving.",
                "desc": "Keep drinks hot or icy all day. Leakproof flip lid and sweat-free powder coating.",
                "image": "images/trending-gifting-perspective.jpg",
                "options": [
                    ("color", "Finish", [("Matte Black", 0), ("Brushed Steel", 0), ("Rose Gold", 30)]),
                ]
            },
        ]

        for pdata in products_list:
            cat = category_map.get(pdata["cat"])
            if not cat: continue

            product, created = Product.objects.get_or_create(
                slug=pdata["slug"],
                defaults={
                    "name": pdata["name"],
                    "category": cat,
                    "short_description": pdata["short"],
                    "description": pdata["desc"],
                    "base_price": pdata["base_price"],
                    "rating": Decimal(pdata["rating"]),
                    "review_count": pdata["reviews"],
                    "badge": pdata["badge"],
                    "image": pdata["image"],
                    "is_active": True,
                }
            )
            # Update fields if existed
            product.base_price = pdata["base_price"]
            product.image = pdata["image"]
            product.badge = pdata["badge"]
            product.save()

            # Options
            for opt_code, opt_name, vals in pdata["options"]:
                opt, _ = ProductOption.objects.get_or_create(
                    product=product,
                    code=opt_code,
                    defaults={"name": opt_name, "required": True}
                )
                for idx, (val_label, extra) in enumerate(vals, start=1):
                    OptionValue.objects.get_or_create(
                        option=opt,
                        code=val_label.lower().replace(" ", "_")[:20],
                        defaults={"label": val_label, "position": idx}
                    )

            # Price Tiers
            base_p = float(pdata["base_price"])
            tiers = [
                (1, base_p),
                (10, round(base_p * 0.95, 2)),
                (50, round(base_p * 0.85, 2)),
                (100, round(base_p * 0.75, 2)),
                (500, round(base_p * 0.60, 2)),
            ]
            for min_q, u_price in tiers:
                PriceRule.objects.get_or_create(
                    product=product,
                    minimum_quantity=min_q,
                    defaults={"unit_price": Decimal(str(u_price)), "is_active": True}
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded complete Vistaprint storefront catalog!"))
