from graphene_extensions.utils.selectors import strip_relay_selectors


def test_strip_relay_selectors():
    selector = {
        'pizzas': {
            'edges': {
                'node': {
                    'id': None,
                    'fields': {
                        'id': None,
                        'relay_fields': {
                            'edges': {
                                'node': {
                                    'id': None,
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    stripped_selector = strip_relay_selectors(selector)
    assert stripped_selector == {
        'pizzas': {
            'id': None,
            'fields': {
                'id': None,
                'relay_fields': {
                    'id': None,
                }
            }
        }
    }
