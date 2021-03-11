from transformations import catalog


def test_required_fields():
    for feature_group in catalog.feature_groups:
        assert feature_group.name
        assert feature_group.key
        assert feature_group.input_entity
        assert feature_group.output_entity
