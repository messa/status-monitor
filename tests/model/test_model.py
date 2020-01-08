from status_monitor.model import Model


def test_create_model(engine):
    class Configuration:
        pass
    conf = Configuration()
    model = Model(conf=conf, engine=engine)
    assert model.sessions
    assert model.users
