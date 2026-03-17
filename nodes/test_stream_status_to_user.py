from nodes.stream_status_to_user import stream_status_to_user


def test_stream_status_to_user_imports():
    assert callable(stream_status_to_user)
