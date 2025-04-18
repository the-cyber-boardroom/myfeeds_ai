import base64

import requests, io, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, UnidentifiedImageError
from myfeeds_ai.personas.actions.My_Feeds__Persona  import My_Feeds__Persona
from osbot_utils.helpers.Local_Cache                import Local_Cache
from osbot_utils.helpers.safe_str.Safe_Str__Hash    import safe_str_hash
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes


class My_Feeds__Persona__Digest__Image(Type_Safe):
    persona     : My_Feeds__Persona = None
    image_cache : Local_Cache                                                               # todo: change this cache to be based on Virtual_Storage (so that we can also easily save it to S3)

    def __init__(self, **kwargs):
        self.image_cache = Local_Cache(cache_name='My_Feeds__Persona__Digest__Image')
        super().__init__(**kwargs)

    def articles(self):
        return self.persona.persona_digest().digest_articles.articles

    def articles__images(self):
        images = []
        for image_url in self.articles__images__urls():
            image = self.image(image_url)
            if image:
                images.append(image)
        return images

    def articles__images__urls(self):
        images__urls = []
        for article in self.articles():
            images__urls.append(article.article_image_link_url)
        return images__urls

    def image(self, image_url):
        image_url_hash = safe_str_hash(image_url)
        if self.image_cache.has_key(image_url_hash):
            image__base_64 = self.image_cache.get(image_url_hash)
            image_bytes    = base64_to_bytes(image__base_64)
        else:
            image_bytes    = requests.get(image_url, timeout=10).content
            image__base_64 = bytes_to_base64(image_bytes)
            self.image_cache.add(image_url_hash, image__base_64)


        try:
            image_png   = Image.open(io.BytesIO(image_bytes))                   # PIL.PngImageFile
            image       = image_png.convert("RGBA")                            # PIL.Image.Image
            return image
        except UnidentifiedImageError as error:
            print(f'failed to load image: {image_url} : {error}')


    def generate_digest_cover(self, image_urls                      ,  # 3‑6 article_image_link_url strings
                                    title                           ,  # e.g. "CISO CYBERSECURITY DIGEST"
                                    sub_title                       ,  # e.g. "March 19 – 26, 2025"
                                    palette_bg  = "#101214"         ,  # dark background
                                    out_path    = "digest_cover.png",
                                    canvas_size = (1400, 800)       ):

        # --- helpers -----------------------------------------------------------
        def fetch(url):
            # simple http -> Pillow Image   (production: add caching / retries)
            return Image.open(io.BytesIO(requests.get(url, timeout=10).content)).convert("RGBA")

        margin = 20
        cols = min(max(len(image_urls), 3), 6)  # clamp 3‑6
        cell_w = (canvas_size[0] - margin * (cols + 1)) // cols
        cell_h = canvas_size[1] - margin * 2
        resample = Image.Resampling.LANCZOS

        # -----------------------------------------------------------------------
        canvas = Image.new("RGBA", canvas_size, palette_bg)

        # bring in images -------------------------------------------------------
        images = [fetch(u) for u in image_urls]
        for idx, im in enumerate(images):
            ratio = min(cell_w / im.width, cell_h / im.height)
            thumb = im.resize((int(im.width * ratio), int(im.height * ratio)), resample)
            holder = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 255))
            offset = ((cell_w - thumb.width) // 2, (cell_h - thumb.height) // 2)
            holder.paste(thumb, offset)
            x = margin + idx * (cell_w + margin)
            canvas.paste(holder, (x, margin))

        # translucent top bar for text -----------------------------------------
        bar_h = 140
        overlay = Image.new("RGBA", (canvas_size[0], bar_h), (0, 0, 0, 180))
        canvas.paste(overlay, (0, 0), overlay)

        draw = ImageDraw.Draw(canvas)
        try:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            f_title = ImageFont.truetype(font_path, 54)
            f_subtitle = ImageFont.truetype(font_path, 32)
        except IOError:  # fallback if font not available
            f_title = f_subtitle = ImageFont.load_default()

        # center text
        tw, th = draw.textbbox((0, 0), title, font=f_title)[2:]
        sw, sh = draw.textbbox((0, 0), sub_title, font=f_subtitle)[2:]
        draw.text(((canvas_size[0] - tw) // 2, 20), title, font=f_title, fill="white")
        draw.text(((canvas_size[0] - sw) // 2, 20 + th + 10), sub_title, font=f_subtitle, fill="silver")

        canvas.convert("RGB").save(out_path, quality=95)
        return out_path

