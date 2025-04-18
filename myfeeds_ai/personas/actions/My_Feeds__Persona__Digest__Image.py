import requests, io
from PIL                                            import Image, ImageDraw, ImageFont, UnidentifiedImageError
from myfeeds_ai.personas.actions.My_Feeds__Persona  import My_Feeds__Persona
from osbot_utils.helpers.Local_Cache                import Local_Cache
from osbot_utils.helpers.safe_str.Safe_Str__Hash    import safe_str_hash
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.utils.Misc                         import bytes_to_base64, base64_to_bytes

URL__FONT__OPEN_SANS = 'https://cdn.jsdelivr.net/fontsource/fonts/open-sans@latest/latin-700-normal.ttf'

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

    def font(self, size=42):
        font_url      = URL__FONT__OPEN_SANS
        font_url_hash = safe_str_hash(font_url)
        if self.image_cache.has_key(font_url_hash):
            font_bytes_base_64 = self.image_cache.get(font_url_hash)
            font_bytes         = base64_to_bytes(font_bytes_base_64)
        else:
            font_bytes = requests.get(font_url, timeout=10).content
            font_bytes_base_64 = bytes_to_base64(font_bytes)
            self.image_cache.add(font_url_hash, font_bytes_base_64)
        return ImageFont.truetype(io.BytesIO(font_bytes), size)


    def generate_digest_cover(self, title                           ,  # e.g. "CISO CYBERSECURITY DIGEST"
                                    sub_title                       ,  # e.g. "March 19 – 26, 2025"
                                    palette_bg  = "#101214"         ,  # dark background
                                    out_path    = "digest_cover.png",
                                    canvas_size = (1400, 800)       ):

        images = self.articles__images()
        margin = 20
        cols = min(max(len(images), 3), 6)  # clamp 3‑6
        cell_w = (canvas_size[0] - margin * (cols + 1)) // cols
        cell_h = canvas_size[1] - margin * 2
        resample = Image.Resampling.LANCZOS


        # -----------------------------------------------------------------------
        canvas = Image.new("RGBA", canvas_size, palette_bg)

        # bring in images -------------------------------------------------------
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

        f_title   = self.font(74)
        f_subtitle = self.font(55)

        # center text
        tw, th = draw.textbbox((0, 0), title, font=f_title)[2:]
        sw, sh = draw.textbbox((0, 0), sub_title, font=f_subtitle)[2:]
        draw.text(((canvas_size[0] - tw) // 2, 20), title, font=f_title, fill="white")
        draw.text(((canvas_size[0] - sw) // 2, 20 + th + 10), sub_title, font=f_subtitle, fill="silver")

        output_buffer = io.BytesIO()
        canvas.convert("RGB").save(output_buffer, format="PNG")
        image_bytes = output_buffer.getvalue()
        return image_bytes
        #canvas.convert("RGB").save(out_path, quality=95)
        #return out_path

