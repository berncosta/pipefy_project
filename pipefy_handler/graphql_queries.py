QUERY_PIPE = """
                    query {
                            {
                              pipe(id: %i) {
                                id
                                name
                                phases {
                                  id
                                  name
                                }
                              }
                            }
                    }
"""

QUERY_PHASE_GET_CARDS = """"""
QUERY_GET_PHASES = """"""
QUERY_CARD = """"""
QUERY_CARDS = """"""
QUERY_FIND_CARDS = """"""

QUERY_ALLCARDS = """
                        {
                            allCards(%s) {
                                pageInfo{
                                    hasNextPage
                                    endCursor
                                }
                                edges{
                                    node{
                                        id
                                        createdAt
                                        updated_at
                                        age
                                        current_phase{
                                            id
                                            name
                                        }
                                        current_phase_age
                                        assignees{
                                            id
                                            name
                                        }
                                        labels{
                                            id
                                            name
                                        }
                                        phases_history{
                                            phase{
                                                id
                                                name
                                            }
                                            firstTimeIn
                                            lastTimeIn
                                            lastTimeOut
                                        }
                                        fields{
                                            name
                                            value
                                            phase_field{
                                                phase{
                                                    id
                                                    name
                                                }
                                            }
                                            field{
                                                id
                                            }
                                        }
                                    }
                                }
                            }
                        }
"""

MUTATION_CREATE_CARD = """"""
MUTATION_UPDATE_CARD = """"""
MUTATION_UPDATE_CARDFIELD = """"""
MUTATION_UPDATE_FIELDS_VALUES = """"""
MUTATION_UPDATE_MOVE_TO_PHASE = """"""
MUTATION_DELETE_CARD = """"""
