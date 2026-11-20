import requests
from bs4 import BeautifulSoup
import re
import json
import time
import urllib.parse

from baza_de_date import insert_products


class SpecExtractor:
    """Extrage automat brandul, memoria, 5G și bateria din titlul produsului"""

    BRANDS = [
        "Samsung", "Apple", "Xiaomi", "Motorola", "Google", "Huawei", "Honor", "OnePlus",
        "Lenovo", "ASUS", "HP", "Acer", "Dell", "MSI", "Gigabyte",
        "Garmin", "Amazfit", "Fitbit",
        "Sony", "JBL", "Bose", "Sennheiser", "Marshall", "Beats", "Skullcandy"
    ]

    @staticmethod
    def clean_price(raw_text):
        if not raw_text:
            return 0.0
        cleaned = re.sub(r"[^\d,\.]", "", str(raw_text))
        if "," in cleaned and "." in cleaned:
            cleaned = cleaned.replace(".", "").replace(",", ".")
        elif "," in cleaned:
            cleaned = cleaned.replace(",", ".")
        elif cleaned.count(".") == 1 and len(cleaned.split(".")[1]) == 3:
            cleaned = cleaned.replace(".", "")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    @staticmethod
    def extract_specs(title, category):
        title_lower = title.lower()

        # 1. Memorie / Stocare (GB)
        memory = 0
        if re.search(r"2\s*tb", title_lower):
            memory = 2048
        elif re.search(r"1\s*tb", title_lower):
            memory = 1024
        else:
            mem_matches = re.findall(r"(\d+)\s*gb", title_lower)
            if mem_matches:
                memory = max(int(m) for m in mem_matches)

        # 2. Conectivitate 5G
        has_5g = "5g" in title_lower

        # 3. Brand
        brand = "Necunoscut"
        for b in SpecExtractor.BRANDS:
            if b.lower() in title_lower:
                brand = b
                break

        if brand == "Necunoscut":
            if any(k in title_lower for k in ["iphone", "ipad", "macbook", "airpods", "apple watch"]):
                brand = "Apple"
            elif "galaxy" in title_lower:
                brand = "Samsung"

        # 4. Capacitate baterie orientativă (mAh)
        battery_defaults = {
            "Telefon": 5000 if ("pro" in title_lower or "ultra" in title_lower) else 4500,
            "Tabletă": 7500,
            "Smartwatch": 400,
            "Laptop": 5500,
            "Căști": 500,
        }
        battery = battery_defaults.get(category, 0)

        return brand, memory, has_5g, battery


class MultiStoreScraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    @classmethod
    def _extract_json_ld(cls, soup, base_url, category_name, default_rating=4.3):
        """Extrage produse din datele structurate Schema.org (JSON-LD) folosite de majoritatea magazinelor"""
        results = []
        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string:
                continue
            try:
                data = json.loads(script.string)
            except Exception:
                continue

            nodes = data if isinstance(data, list) else [data]
            expanded = []
            for node in nodes:
                if isinstance(node, dict):
                    if "@graph" in node and isinstance(node["@graph"], list):
                        expanded.extend(node["@graph"])
                    elif node.get("@type") == "ItemList" and isinstance(node.get("itemListElement"), list):
                        for elem in node["itemListElement"]:
                            if isinstance(elem, dict):
                                expanded.append(elem.get("item", elem))
                    else:
                        expanded.append(node)

            for item in expanded:
                if not isinstance(item, dict) or item.get("@type") != "Product":
                    continue

                name = str(item.get("name", "")).strip()
                offers = item.get("offers", {})
                if isinstance(offers, list) and offers:
                    offers = offers[0]
                if not isinstance(offers, dict):
                    continue

                price = SpecExtractor.clean_price(offers.get("price") or offers.get("lowPrice"))
                link = offers.get("url") or item.get("url") or ""
                if link and not link.startswith("http"):
                    link = urllib.parse.urljoin(base_url, link)

                if not name or price <= 0 or not link:
                    continue

                image = item.get("image", "")
                if isinstance(image, list) and image:
                    image = image[0]
                elif isinstance(image, dict):
                    image = image.get("url", "")

                rating = default_rating
                agg = item.get("aggregateRating")
                if isinstance(agg, dict) and agg.get("ratingValue"):
                    try:
                        rating = float(agg["ratingValue"])
                        if rating > 5:
                            rating = round(rating / 20, 1)
                    except ValueError:
                        pass

                brand, memory, has_5g, battery = SpecExtractor.extract_specs(name, category_name)
                results.append({
                    "name": name,
                    "category": category_name,
                    "brand": brand,
                    "price": price,
                    "rating": rating if rating > 0 else default_rating,
                    "memory": memory,
                    "battery": battery,
                    "5g": has_5g,
                    "image": str(image),
                    "url": link
                })
        return results

    @classmethod
    def _parse_generic_cards(cls, soup, base_url, category_name, card_sel, title_sel, price_sel, img_sel="img", default_rating=4.3):
        """Parser HTML de rezervă pentru magazinele care nu expun JSON-LD în lista de căutare"""
        results = []
        for card in soup.select(card_sel):
            title_elem = card.select_one(title_sel)
            price_elem = card.select_one(price_sel)
            if not title_elem or not price_elem:
                continue

            name = title_elem.get_text(strip=True)
            link = title_elem.get("href", "")
            if link and not link.startswith("http"):
                link = urllib.parse.urljoin(base_url, link)

            price = SpecExtractor.clean_price(price_elem.get_text(strip=True))
            if not name or price <= 0 or not link:
                continue

            img_elem = card.select_one(img_sel)
            image_url = ""
            if img_elem:
                image_url = img_elem.get("src") or img_elem.get("data-src") or ""
                if image_url and not image_url.startswith("http"):
                    image_url = urllib.parse.urljoin(base_url, image_url)

            brand, memory, has_5g, battery = SpecExtractor.extract_specs(name, category_name)
            results.append({
                "name": name,
                "category": category_name,
                "brand": brand,
                "price": price,
                "rating": default_rating,
                "memory": memory,
                "battery": battery,
                "5g": has_5g,
                "image": image_url,
                "url": link
            })
        return results

    # 1. eMAG
    @classmethod
    def scrape_emag(cls, query, category_name):
        url = f"https://www.emag.ro/search/{urllib.parse.quote(query)}"
        results = []
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.select(".card-item"):
                title_elem = card.select_one(".card-v2-title")
                price_elem = card.select_one(".product-new-price")
                if not title_elem or not price_elem:
                    continue

                name = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                price = SpecExtractor.clean_price(price_elem.get_text(strip=True))
                if price <= 0 or not link:
                    continue

                img_elem = card.select_one("img")
                image_url = img_elem.get("src", "") if img_elem else ""

                rating = 4.2
                star_elem = card.select_one(".star-rating-container")
                if star_elem and star_elem.has_attr("class"):
                    for c in star_elem["class"]:
                        if c.startswith("star-rating-"):
                            try:
                                rating = float(c.split("-")[-1])
                            except ValueError:
                                pass

                brand, memory, has_5g, battery = SpecExtractor.extract_specs(name, category_name)
                results.append({
                    "name": name,
                    "category": category_name,
                    "brand": brand,
                    "price": price,
                    "rating": rating,
                    "memory": memory,
                    "battery": battery,
                    "5g": has_5g,
                    "image": image_url,
                    "url": link
                })
        except Exception as e:
            print(f"   ⚠️ [eMAG] Eroare: {e}")
        return results


    # 2 & 3. ALTEX & MEDIA GALAXY (aceeași arhitectură)
    @classmethod
    def _extract_next_data_products(cls, data, found):
        if isinstance(data, dict):
            if "name" in data and ("price" in data or "regular_price" in data) and ("url_key" in data or "url" in data):
                found.append(data)
            for v in data.values():
                cls._extract_next_data_products(v, found)
        elif isinstance(data, list):
            for item in data:
                cls._extract_next_data_products(item, found)

    @classmethod
    def scrape_altex_family(cls, domain, store_name, query, category_name):
        base_url = f"https://{domain}"
        url = f"{base_url}/cauta/?q={urllib.parse.quote(query)}"
        results = []
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            next_script = soup.find("script", id="__NEXT_DATA__")
            if next_script and next_script.string:
                json_data = json.loads(next_script.string)
                raw_items = []
                cls._extract_next_data_products(json_data, raw_items)

                for item in raw_items:
                    name = item.get("name", "").strip()
                    price = SpecExtractor.clean_price(item.get("price") or item.get("regular_price"))
                    raw_url = item.get("url") or f"{base_url}/{item.get('url_key', '')}/cpd/{item.get('sku', '')}/"
                    if not raw_url.startswith("http"):
                        raw_url = base_url + raw_url
                    if not name or price <= 0:
                        continue

                    rating = float(item.get("rating_summary") or 4.3)
                    if rating > 5:
                        rating = round(rating / 20, 1)

                    image_url = item.get("image") or item.get("small_image") or ""
                    if image_url and not image_url.startswith("http"):
                        image_url = "https://lcdn.altex.ro" + image_url

                    brand, memory, has_5g, battery = SpecExtractor.extract_specs(name, category_name)
                    results.append({
                        "name": name,
                        "category": category_name,
                        "brand": brand,
                        "price": price,
                        "rating": rating if rating > 0 else 4.3,
                        "memory": memory,
                        "battery": battery,
                        "5g": has_5g,
                        "image": image_url,
                        "url": raw_url
                    })

            if not results:
                results = cls._extract_json_ld(soup, base_url, category_name, default_rating=4.3)
            if not results:
                results = cls._parse_generic_cards(
                    soup, base_url, category_name,
                    "li.Product, .Products-item", "a.Product-name, h2 a", ".Price-int"
                )
        except Exception as e:
            print(f"   ⚠️ [{store_name}] Eroare: {e}")
        return results


    # 4. FLANCO
    @classmethod
    def scrape_flanco(cls, query, category_name):
        base_url = "https://www.flanco.ro"
        url = f"{base_url}/catalogsearch/result/?q={urllib.parse.quote(query)}"
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results = cls._extract_json_ld(soup, base_url, category_name, default_rating=4.3)
            if not results:
                results = cls._parse_generic_cards(
                    soup, base_url, category_name,
                    ".product-item", "a.product-item-link", ".price"
                )
            return results
        except Exception as e:
            print(f"   ⚠️ [Flanco] Eroare: {e}")
            return []

    # 5. evoMAG
    @classmethod
    def scrape_evomag(cls, query, category_name):
        base_url = "https://www.evomag.ro"
        url = f"{base_url}/?sn.q={urllib.parse.quote(query)}"
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            return cls._parse_generic_cards(
                soup, base_url, category_name,
                ".product_grid_item", ".npi_name a", ".real_price", ".npi_image img", default_rating=4.4
            )
        except Exception as e:
            print(f"   ⚠️ [evoMAG] Eroare: {e}")
            return []

    # 6. PC GARAGE
    @classmethod
    def scrape_pcgarage(cls, query, category_name):
        base_url = "https://www.pcgarage.ro"
        url = f"{base_url}/cauta/{urllib.parse.quote(query)}"
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results = cls._extract_json_ld(soup, base_url, category_name, default_rating=4.5)
            if not results:
                results = cls._parse_generic_cards(
                    soup, base_url, category_name,
                    ".product_box", ".product_box_name a", ".pb-price, .price", default_rating=4.5
                )
            return results
        except Exception as e:
            print(f"   ⚠️ [PC Garage] Eroare: {e}")
            return []


    # 7. VEXIO
    @classmethod
    def scrape_vexio(cls, query, category_name):
        base_url = "https://www.vexio.ro"
        url = f"{base_url}/cautare/?q={urllib.parse.quote(query)}"
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results = cls._extract_json_ld(soup, base_url, category_name, default_rating=4.4)
            if not results:
                results = cls._parse_generic_cards(
                    soup, base_url, category_name,
                    ".product-box, .product-item", ".name a, .product-title a", ".price", default_rating=4.4
                )
            return results
        except Exception as e:
            print(f"   ⚠️ [Vexio] Eroare: {e}")
            return []

  
    # 8. CEL.ro
    @classmethod
    def scrape_cel(cls, query, category_name):
        base_url = "https://www.cel.ro"
        url = f"{base_url}/cauta/{urllib.parse.quote(query)}/"
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            results = cls._extract_json_ld(soup, base_url, category_name, default_rating=4.2)
            if not results:
                results = cls._parse_generic_cards(
                    soup, base_url, category_name,
                    ".productListing-tot", ".productTitle a", ".price", default_rating=4.2
                )
            return results
        except Exception as e:
            print(f"   ⚠️ [CEL.ro] Eroare: {e}")
            return []


if __name__ == "__main__":
    print("🚀 Scanez automat 8 magazine (eMAG, Altex, Media Galaxy, Flanco, evoMAG, PC Garage, Vexio, CEL.ro)...\n")

    categorii = [
        ("telefon mobil", "Telefon"),
        ("tableta", "Tabletă"),
        ("smartwatch", "Smartwatch"),
        ("laptop", "Laptop"),
        ("casti wireless", "Căști"),
    ]

    magazine = [
        ("eMAG", MultiStoreScraper.scrape_emag),
        ("Altex", lambda q, c: MultiStoreScraper.scrape_altex_family("altex.ro", "Altex", q, c)),
        ("Media Galaxy", lambda q, c: MultiStoreScraper.scrape_altex_family("mediagalaxy.ro", "Media Galaxy", q, c)),
        ("Flanco", MultiStoreScraper.scrape_flanco),
        ("evoMAG", MultiStoreScraper.scrape_evomag),
        ("PC Garage", MultiStoreScraper.scrape_pcgarage),
        ("Vexio", MultiStoreScraper.scrape_vexio),
        ("CEL.ro", MultiStoreScraper.scrape_cel),
    ]

    toate_produsele = []

    for query, category_name in categorii:
        print(f"🔎 Categorie: {category_name}")
        for store_name, scraper_fn in magazine:
            items = scraper_fn(query, category_name)
            print(f"   • {store_name}: {len(items)} produse")
            toate_produsele.extend(items)
            time.sleep(0.8)

    if toate_produsele:
        print(f"\n💾 Salvez în total {len(toate_produsele)} produse din toate magazinele în baza de date...")
        insert_products(toate_produsele)
        print("🎉 Gata! Acum aplicația compară automat toate magazinele și afișează strict cele mai bune oferte.")
    else:
        print("\n⚠️ Nu s-au putut extrage produse. Verifică conexiunea la internet.")
