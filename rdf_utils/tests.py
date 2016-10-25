import json
import unittest
from obeu_graph import OBEUGraph
from stm import STM


class TestSTMMethods(unittest.TestCase):
    def setUp(self):
        self.response = json.loads("""{
          "head": {
            "link": [],
            "vars": [
              "s",
              "p",
              "dim"
            ]
          },
          "results": {
            "bindings": [
              {
                "dim": {
                  "type": "uri",
                  "value": "http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1000"
                },
                "p": {
                  "type": "uri",
                  "value": "http://www.w3.org/2004/02/skos/core#broader"
                },
                "s": {
                  "type": "uri",
                  "value": "http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1020"
                }
              },
              {
                "dim": {
                  "type": "uri",
                  "value": "http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1000"
                },
                "p": {
                  "type": "uri",
                  "value": "http://www.w3.org/2004/02/skos/core#broader"
                },
                "s": {
                  "type": "uri",
                  "value": "http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1066"
                }
              }
            ]
          }
        }""")

    def test_parse_response(self):
        # simulate the output of get_data by just loading a string and
        # jsonifying it

        real_result = STM.parse_response(self.response, 's', 'p', 'dim')
        expected_result = [
            {
                's': 'http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1020',
                'p': 'http://www.w3.org/2004/02/skos/core#broader',
                'dim': 'http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1000'
            },
            {
                's': 'http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1066',
                'p': 'http://www.w3.org/2004/02/skos/core#broader',
                'dim': 'http://data.openbudgets.eu/resource/codelist/aemterhierarchie_bonn/1000'
            }
        ]
        self.assertEqual(real_result, expected_result)

    def test_parse_response_gen(self):
        self.assertEqual(
            type(STM.parse_response_gen(self.response, 's', 'p', 'dim')), \
            type((x for x in []))
        )

if __name__ == '__main__':
    unittest.main()
