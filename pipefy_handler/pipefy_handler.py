import json
import time
import requests
import pandas as pd
import numpy as np

from . import graphql_queries


# classe para tratar com a API do Pipefy

class pipefyHandler:
    def __init__(self, auth_token, pipe_id):
        self.api_url = "https://api.pipefy.com/graphql"
        self.api_headers = {"Authorization": auth_token, "Content-Type": "application/json"}
        self.pipe_id = pipe_id

    def get_pipe_data(self):
        return None

    def get_all_cards_as_pandas(self):
        pages_list = self.get_cards_all_pages(graphql_queries.QUERY_ALLCARDS, 'allCards')
        df = self.get_cards_list_as_pandas_df(pages_list)
        return df

    def get_phase_cards_as_pandas(self, phase_id):

        # TO_DO must include phase_id as a parameter to 'get_cards_all_pages'

        pages_list = self.get_cards_all_pages(graphql_queries.QUERY_PHASE_GET_CARDS, 'phase')
        df = self.get_cards_list_as_pandas_df(pages_list)
        return df

    def get_cards_list_as_pandas_df(self, pages_list):
        """based on a list of pages, return a pandas dataframe where each entry is a card"""

        # flatten pages_list into cards_list
        cards_list = []
        for page in pages_list:
            for card in page:
                cards_list.append(card)

        # get a first df with custom fields in a json column 'fields'
        first_df = pd.json_normalize(cards_list)

        # prepare to open column 'fields'
        fields = first_df['fields'].values
        fields_list = [{'index': i, 'fields': fields[i]} for i in range(len(fields))]

        # open column 'fields' in a new df
        fields_df = pd.json_normalize(fields_list, record_path=['fields'], meta=['index'])

        # prepare to pivot as the new df is a name/value table
        fields_df['phase.name'] = fields_df['phase_field.phase.name'] + "_" + fields_df['name']
        fields_df.drop(['phase_field.phase.name', 'name'], axis=1, inplace=True)

        # pivot and concat the tables as a single table
        fields_df_p = fields_df.pivot(index='index', columns='phase.name', values='value')
        df = pd.concat([first_df, fields_df_p], axis=1)

        return df

    def get_cards_all_pages(self, query_string, query_type):
        """returns a list of pages, where each page is a list of cards"""

        payload = query_string % ('pipeId:' + str(self.pipe_id) + ',first:50')
        body = {'query': payload}

        pages_list = []
        response = self.get_cards_page(body, query_type)
        pages_list.append(response[0])
        has_next_page = response[1]

        while has_next_page:
            payload = query_string % ('pipeId:' + str(self.pipe_id) + ',first:50,after:"' + str(response[2]) + '"')
            body = {'query': payload}
            response = self.get_cards_page(body, query_type)
            pages_list.append(response[0])
            has_next_page = response[1]

        return pages_list

    def get_cards_page(self, body, query_type):
        response = self.pipefy_request(json.dumps(body))
        print(response)
        response_dict = json.loads(response.text)
        edges = response_dict['data'][query_type]['edges']

        cards_list = []
        for e in edges:
            cards_list.append(e['node'])

        has_next_page = response_dict['data'][query_type]['pageInfo']['hasNextPage']
        end_cursor = response_dict['data'][query_type]['pageInfo']['endCursor']

        return [cards_list, has_next_page, end_cursor]

    def pipefy_request(self, payload, retries=3):
        """Requisição padrão para a API do Pipefy, com retentativas"""

        response = None
        had_success = False
        while retries > 0:
            try:
                response = requests.post(self.api_url, data=payload, headers=self.api_headers)
                if response.status_code == 200:
                    retries = 0
                    had_success = True
                elif response.status_code == 400:
                    retries = 0
                    had_success = True
                else:
                    retries += -1
                    time.sleep(15)
            except Exception as ex:
                print(ex)
                retries += -1
                time.sleep(15)

        if not had_success:
            print('Esgotadas as tentativas')
            return response

        return response

    def get_phase_cards(self, phase_id):
        return None

    def create_card(self, field_dict):
        return None

    def update_card_field(self, card_id, field, value):
        return None

    def update_card_fields(self, card_id, field_dict):
        return None

    def update_multiple_cards(self, cards_dict):
        return None

    def delete_card(self, card_id):
        return None

    def update_card_label(self, card_id, label_id):
        return None

    def update_card_assignee(self, card_id, assignee_id):
        return None

    def move_card_to_phase(self, card_id, phase_id):
        return None
