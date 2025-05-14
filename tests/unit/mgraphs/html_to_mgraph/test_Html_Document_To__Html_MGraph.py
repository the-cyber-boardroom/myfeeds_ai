from unittest                                                        import TestCase
from myfeeds_ai.mgraphs.html_to_mgraph.Html_Document_To__Html_MGraph import Html_Document_To__Html_MGraph
from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Screenshot       import Html_MGraph__Screenshot__Config
from osbot_utils.helpers.html.Html__To__Html_Document                import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document          import Schema__Html_Document
from osbot_utils.utils.Env                                           import load_dotenv


class test_Html_Document_To__Html_MGraph(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.html          = GET("https://docs.diniscruz.ai")
    #     cls.html = GET("https://www.linkedin.com")

    def setUp(self):
        self.html          = HTML__EXAMPLE__WITH__FORM
        self.title         = "Html Graph"
        self.html_document = Html__To__Html_Document(html=self.html).convert()
        self.html_to_graph = Html_Document_To__Html_MGraph(html_document=self.html_document)
        self.create_png    = False

    def tearDown(self):
        if self.create_png:
            #pprint(self.html_to_graph.html_mgraph.data().stats())
            load_dotenv()
            with Html_MGraph__Screenshot__Config() as _:
                _.target_file          = f"{self.__class__.__name__}.png"
                _.graph.title          = self.title
                #_.graph.layout_engine = MGraph__Export__Dot__Layout__Engine.FDP
                _.print_dot_code      = False
                #_.graph.node_sep       = 0.1
                #_.graph.rank_sep        = 0.1
                #_.graph.spring_constant = 0.25
                self.html_to_graph.create_screenshot(config=_)

    def test__init__(self):
        with self.html_to_graph as _:
            assert type(_)         is Html_Document_To__Html_MGraph
            assert len(self.html)  == 421
            assert _.html_document        == self.html_document
            assert type(_.html_document)  is Schema__Html_Document

    def test_convert(self):
        #self.create_png = True
        with self.html_to_graph as _:
            #target= "https://docs.diniscruz.ai"                 # doesn't work (with full colors)
            #target = "https://www.google.com"
            #target = "https://www.apple.com"
            #_.html = HTML__EXAMPLE__WITH__PARAGRAPHS
            #_.html = HTML__EXAMPLE__WITH__NESTED_LISTS
            #_.html = HTML__EXAMPLE__WITH__BOOTSTRAP
            # _.html  = GET("https://thegrafter.com/about")
            # self.title = "https://thegrafter.com/about"
            #_.html = GET("https://www.apple.com")
            #_.html = GET("https://www.google.com")
            #_.html = GET(target)
            #self.title = target
            _.convert()
            assert type(_.html_document) is Schema__Html_Document
            #pprint(_.html__dict)


    def test_convert__to__html_schema(self):
        with self.html_to_graph as _:
            #_.html = GET("https://docs.diniscruz.ai")
            _.convert__to__html_schema()
            assert type(_.html_document) is Schema__Html_Document

    def test_convert__simple_html(self):
        html               = HTML__EXAMPLE__WITH__PARAGRAPHS
        html_document      = Html__To__Html_Document      (html          = html         ).convert()
        self.html_to_graph = Html_Document_To__Html_MGraph(html_document = html_document)
        with self.html_to_graph as _:
            _.convert()


HTML__EXAMPLE__WITH__JUST_BODY = """\
<html>
    <body>        
    </body>
</html>"""

HTML__EXAMPLE__WITH__PARAGRAPHS = """\
<html>
    <body>
        <p>hello</p>
        <p>world</p>
    </body>
</html>"""


HTML__EXAMPLE__WITH__ATTRIBUTES = """\
<html>
    <body>
        <div>
            <p class="greeting">Hello</p>
            <p id="planet">World</p>
        </div>
    </body>
</html>
"""

HTML__EXAMPLE__WITH__LINK_AND_IMAGE = """\
<html>
    <body>
        <p><a href="https://example.com">Hello</a></p>
        <p><img src="world.jpg" alt="World"></p>
    </body>
</html>"""

HTML__EXAMPLE__WITH__FORM = """\
<html>
    <head>
        <title>Html example with Form</title>
    </head>
    <body>
        <h1>Contact Us</h1>
        <form>
            <p>Name: <input type="text" name="name"></p>
            <p>Email: <input type="email" name="email"></p>
            <p>Message:</p>
            <p><textarea name="message"></textarea></p>
            <p><input type="submit" value="Send"></p>
        </form>
    </body>
</html>
"""

HTML__EXAMPLE__WITH__NESTED_LISTS = """\
<html>
    <body>
        <h1>Topics</h1>
        <section>
            <h2>Fruits</h2>
            <ul>
                <li>Apple</li>
                <li>Banana</li>
                <li>Cherry</li>
            </ul>
        </section>
        <section>
            <h2>Vegetables</h2>
            <ul>
                <li>Carrot</li>
                <li>Peas</li>
                <li>Spinach</li>
            </ul>
        </section>
    </body>
</html>
"""


HTML__EXAMPLE__WITH__BOOTSTRAP = """\
<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Simple Bootstrap 5 Webpage</title>
      <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
              rel="stylesheet"
              integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
              crossorigin="anonymous"/>
    </head>
    <body>

      <!-- Navigation -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Webpage Name</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Features</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Pricing</a>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!-- Jumbotron / Hero -->
      <div class="p-5 mb-4 bg-light rounded-3">
        <div class="container-fluid py-5">
          <h1 class="display-5 fw-bold">Welcome to Our Website!</h1>
          <p class="col-md-8 fs-4">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
          <button class="btn btn-primary btn-lg" type="button">Example button</button>
        </div>
      </div>

      <!-- Footer -->
      <footer class="py-3 my-4">
        <ul class="nav justify-content-center border-bottom pb-3 mb-3">
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Home</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Features</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Pricing</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">FAQs</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">About</a></li>
        </ul>
        <p class="text-center text-muted">© 2023 Company, Inc</p>
      </footer>

      <!-- Bootstrap JS -->
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
              integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    </body>
</html>"""