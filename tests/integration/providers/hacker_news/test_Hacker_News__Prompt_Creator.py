from unittest                                                                                      import TestCase
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed    import Model__Hacker_News__Feed
from cbr_custom_news_feeds.providers.cyber_security.hacker_news.Hacker_News__Prompt_Creator        import Hacker_News__Prompt_Creator

class test_Hacker_News__Prompt_Creator(TestCase):

    def setUp(self):
        self.prompt_creator = Hacker_News__Prompt_Creator()

        self.article_1 = Model__Hacker_News__Article(
            title       = "Article 1 Title <script>alert('xss')</script>",
            description = "Description 1 &nbsp; with HTML",
            link        = "https://example.com/1",
            pub_date    = "Wed, 04 Dec 2024 22:53:00 +0530",
            author      = "info@thehackernews.com (John Doe)",
            image_url   = "https://example.com/image1.jpg"
        )

        self.article_2 = Model__Hacker_News__Article(
            title       = "Article 2 Title",
            description = "Description 2",
            link        = "https://example.com/2",
            pub_date    = "Wed, 04 Dec 2024 21:53:00 +0530",
            author      = "Jane Smith",
            image_url   = "https://example.com/image2.jpg"
        )

        self.sample_feed = Model__Hacker_News__Feed(
            title            = "The Hacker News",
            link             = "https://thehackernews.com",
            description      = "Most trusted cybersecurity news source",
            language         = "en-us",
            last_build_date  = "Thu, 05 Dec 2024 02:15:56 +0530",
            update_period    = "hourly",
            update_frequency = 1,
            articles         = [self.article_1, self.article_2]
        )

    # def test_create_prompt_analysis(self):
    #     with self.prompt_creator as _:                                                         # Test analysis prompt creation
    #         prompt = _.create_prompt_analysis(self.sample_feed, size=1)
    #
    #         assert "The Hacker News"                     in prompt                                                 # Check feed details included
    #         assert "Thu, 05 Dec 2024"                    in prompt
    #         assert "Article 1 Title"                     in prompt                                                 # Check article content
    #         assert ">alert('xss')"                   not in prompt                                               # Check HTML is cleaned
    #         assert "John Doe"                            in prompt                                                        # Check author is cleaned
    #         assert "info@thehackernews.com"          not in prompt
    #
    #         assert "current cybersecurity landscape"     in prompt                                 # Check analysis instructions
    #         assert "Key trends"                          in prompt
    #
    #         prompt_two_articles = _.create_prompt_analysis(self.sample_feed, size=2)           # Test size parameter
    #         assert "Article 2" in prompt_two_articles
    #         assert len(prompt_two_articles) > len(prompt)

    def test_create_prompt_schema(self):
        with self.prompt_creator as _:                                                         # Test schema prompt creation
            prompt = _.create_prompt_schema(self.sample_feed, size=2)

            assert "Hacker News schema with fields: title, description" in prompt              # Check schema description
            assert "2 articles" in prompt                                                      # Check article count

            assert "The Hacker News" in prompt                                                # Check feed metadata
            assert "Thu, 05 Dec 2024" in prompt

            assert "&nbsp;" not in prompt                                                     # Check text cleaning
            assert "<script>" not in prompt

    # def test_create_prompt_executive(self):
    #     with self.prompt_creator as _:                                                         # Test executive prompt creation
    #         prompt = _.create_prompt_executive(self.sample_feed, size=1)
    #
    #         assert "1. Article 1 Title" in prompt                                             # Check headline format
    #         assert "Description 1" not in prompt                                              # Check only titles included
    #         assert "cybersecurity news headlines" in prompt
    #
    #         prompt_two_articles = _.create_prompt_executive(self.sample_feed, size=2)          # Test size parameter
    #         assert "2. Article 2 Title" in prompt_two_articles

    def test_clean_text(self):
        with self.prompt_creator as _:                                                         # Test text cleaning functionality
            test_cases = [("<p>Test</p>"                        , "Test"              ),                        # HTML removal
                          ("Text &nbsp; with &quot;quotes&quot;", 'Text with "quotes"'),               # Entity replacement
                          ("Multiple     spaces"                , "Multiple spaces"   ),                       # Space normalization
                          ("<script>alert('xss')</script>"      , "alert('xss')"      )]                       # Script tag removal


            for input_text, expected in test_cases:
                assert _.clean_text(input_text) == expected

    def test_clean_author(self):
        with self.prompt_creator as _:                                                         # Test author cleaning functionality
            test_cases = [("info@example.com (John Doe)", "John Doe"                  ),                 # Email removal
                          ("Jane Smith"                 , "Jane Smith"                ),                 # Plain name
                          ("info@test.com Author Name"  , "info@test.com Author Name" ),                 # Email with name
                          ("(Author) Name"              , "Author Name"             )                   # Parentheses removal
]

            for input_text, expected in test_cases:
                assert _.clean_author(input_text) == expected